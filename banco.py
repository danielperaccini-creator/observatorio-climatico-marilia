import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import duckdb
import numpy as np
import pandas as pd

from config import (BANCO, CIDADE, DADOS, EVIDENCIAS, FIM, FUSO, INICIO,
                    LATITUDE, LONGITUDE, METADADOS, ORIGINAL, parametros)

COLUNAS = {
    "temperature_2m_min": "temperatura_min",
    "temperature_2m_max": "temperatura_max",
    "precipitation_sum": "precipitacao",
}


def tratar(conteudo):
    diario = conteudo.get("daily", {})
    unidades = conteudo.get("daily_units", {})
    esperadas = {"time": "iso8601", "temperature_2m_min": "°C",
                 "temperature_2m_max": "°C", "precipitation_sum": "mm"}
    if any(unidades.get(c) != u for c, u in esperadas.items()):
        raise ValueError("Unidades ausentes ou incompatíveis com o dicionário.")
    if conteudo.get("timezone") != FUSO:
        raise ValueError("O fuso da resposta difere da configuração.")
    campos = ["time", *COLUNAS]
    if any(not isinstance(diario.get(c), list) for c in campos):
        raise ValueError("A resposta não contém todos os vetores diários.")
    if len({len(diario[c]) for c in campos}) != 1:
        raise ValueError("Os vetores da resposta têm tamanhos diferentes.")
    df = pd.DataFrame({c: diario[c] for c in campos}).rename(columns={"time": "data", **COLUNAS})
    if not df["data"].map(lambda x: isinstance(x, str) and len(x) == 10).all():
        raise ValueError("Há datas vazias ou fora do formato AAAA-MM-DD.")
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="raise")
    if df["data"].duplicated().any():
        raise ValueError("Há datas duplicadas. Verifique o JSON antes da carga.")
    esperado = pd.date_range(INICIO, FIM, freq="D")
    if len(df) != 30 or set(df["data"]) != set(esperado):
        raise ValueError("A resposta não cobre exatamente os 30 dias do recorte.")
    for c in COLUNAS.values():
        df[c] = pd.to_numeric(df[c], errors="raise").astype("float64")
        if np.isinf(df[c]).any():
            raise ValueError(f"Valor infinito em {c}.")
    if (df["temperatura_min"] > df["temperatura_max"]).any():
        raise ValueError("Há temperatura mínima superior à máxima.")
    if (df["precipitacao"] < 0).any():
        raise ValueError("Há precipitação negativa.")
    # Esses limites servem para revisão da carga, não para classificar o clima.
    for c in ["temperatura_min", "temperatura_max"]:
        if ((df[c] < -10) | (df[c] > 50)).any():
            raise ValueError(f"{c} fora de -10 a 50 °C: conferir a fonte antes de carregar.")
    if (df["precipitacao"] > 500).any():
        raise ValueError("Precipitação acima de 500 mm/dia: conferir a fonte antes de carregar.")
    df.insert(0, "cidade", CIDADE)
    df.insert(2, "latitude", LATITUDE)
    df.insert(3, "longitude", LONGITUDE)
    return df.sort_values("data").reset_index(drop=True)


def carregar():
    bruto = ORIGINAL.read_bytes()
    meta = json.loads(METADADOS.read_text(encoding="utf-8"))
    if hashlib.sha256(bruto).hexdigest() != meta["sha256"]:
        raise ValueError("O hash do JSON não confere com o registro da coleta.")
    if meta["parametros"] != parametros():
        raise ValueError("O JSON pertence a outro recorte. Execute coleta.py.")
    df = tratar(json.loads(bruto))
    DADOS.mkdir(parents=True, exist_ok=True)
    EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(BANCO))
    try:
        con.execute("BEGIN TRANSACTION")
        con.execute("""
            CREATE TABLE IF NOT EXISTS clima_diario (
                cidade VARCHAR NOT NULL,
                data DATE NOT NULL,
                latitude DOUBLE NOT NULL,
                longitude DOUBLE NOT NULL,
                temperatura_min DOUBLE,
                temperatura_max DOUBLE,
                precipitacao DOUBLE,
                PRIMARY KEY (cidade, data),
                CHECK (temperatura_min IS NULL OR temperatura_max IS NULL OR temperatura_min <= temperatura_max),
                CHECK (precipitacao IS NULL OR precipitacao >= 0)
            )
        """)
        con.register("dados_tratados", df)
        antes = con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0]
        con.execute("""
            INSERT INTO clima_diario
            SELECT cidade, CAST(data AS DATE), latitude, longitude,
                   temperatura_min, temperatura_max, precipitacao FROM dados_tratados
            ON CONFLICT (cidade, data) DO UPDATE SET
                latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude,
                temperatura_min = EXCLUDED.temperatura_min,
                temperatura_max = EXCLUDED.temperatura_max,
                precipitacao = EXCLUDED.precipitacao
        """)
        depois = con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0]
        if depois != 30:
            raise ValueError("O banco precisa conter somente os 30 registros da localidade definida.")
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()
    df.to_csv(DADOS / "clima_tratado.csv", index=False, date_format="%Y-%m-%d")
    qualidade = {
        "executado_em": datetime.now(ZoneInfo(FUSO)).isoformat(),
        "registros_antes": antes, "registros_depois": depois,
        "periodo": [INICIO, FIM], "datas_distintas": int(df["data"].nunique()),
        "duplicidades": int(df.duplicated(["cidade", "data"]).sum()),
        "ausentes": {c: int(df[c].isna().sum()) for c in COLUNAS.values()},
        "checagens_estruturais": "aprovadas",
        "decisao_ausencias": "Preservar NULL; não imputar zero. KPIs exigem 30 valores válidos.",
        "sha256_original": meta["sha256"],
    }
    (EVIDENCIAS / "qualidade.json").write_text(json.dumps(qualidade, ensure_ascii=False, indent=2), encoding="utf-8")
    with (EVIDENCIAS / "cargas.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(qualidade, ensure_ascii=False) + "\n")
    print(json.dumps(qualidade, ensure_ascii=False, indent=2))
    print(df.head(5).to_string(index=False))
    return qualidade


if __name__ == "__main__":
    carregar()
