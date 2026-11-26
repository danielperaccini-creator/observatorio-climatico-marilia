import hashlib
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import API, FUSO, METADADOS, ORIGINAL, parametros


def coletar():
    sessao = requests.Session()
    tentativas = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    sessao.mount("https://", HTTPAdapter(max_retries=tentativas))
    try:
        resposta = sessao.get(API, params=parametros(), timeout=(10, 60))
        resposta.raise_for_status()
        conteudo = resposta.json()
        if conteudo.get("error") or "daily" not in conteudo:
            raise ValueError("A API não retornou os dados diários esperados.")
        instante = datetime.now(ZoneInfo(FUSO))
        bruto = resposta.content
        metadados = {
            "coletado_em": instante.isoformat(), "url": resposta.url,
            "parametros": parametros(), "status_http": resposta.status_code,
            "sha256": hashlib.sha256(bruto).hexdigest(),
            "bytes": len(bruto), "dias_recebidos": len(conteudo["daily"]["time"]),
            "coordenadas_retornadas": {
                "latitude": conteudo["latitude"], "longitude": conteudo["longitude"],
                "elevacao_m": conteudo.get("elevation"),
            },
            "natureza": "Reanálise ERA5 disponibilizada pela Open-Meteo; não é medição de estação local.",
        }
        ORIGINAL.parent.mkdir(parents=True, exist_ok=True)
        historico = ORIGINAL.parent / "historico"
        historico.mkdir(exist_ok=True)
        nome = instante.strftime("%Y%m%dT%H%M%S%f")
        (historico / f"{nome}.json").write_bytes(bruto)
        (historico / f"{nome}_metadados.json").write_text(
            json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
        ORIGINAL.write_bytes(bruto)
        METADADOS.write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"HTTP {resposta.status_code} | {metadados['dias_recebidos']} dias | {len(bruto)} bytes")
        print(f"Coleta: {metadados['coletado_em']} | modelo ERA5")
        print(f"JSON preservado: dados/originais/open_meteo.json | SHA-256 {metadados['sha256']}")
        return metadados
    finally:
        sessao.close()


if __name__ == "__main__":
    coletar()
