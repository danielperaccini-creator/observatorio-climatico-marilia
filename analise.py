import json

import duckdb

from config import BANCO, EVIDENCIAS, RAIZ


def analisar():
    EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(BANCO), read_only=True)
    resultados = {}
    try:
        sql = (RAIZ / "consultas.sql").read_text(encoding="utf-8")
        for i, consulta in enumerate(sql.split(";"), start=1):
            if not consulta.strip():
                continue
            df = con.execute(consulta).df()
            df.to_csv(EVIDENCIAS / f"consulta_{i}.csv", index=False)
            resultados[f"consulta_{i}"] = json.loads(df.to_json(orient="records", date_format="iso"))
            print(f"\nConsulta {i}\n{df.to_string(index=False)}")
    finally:
        con.close()
    (EVIDENCIAS / "resultados.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultados


if __name__ == "__main__":
    analisar()
