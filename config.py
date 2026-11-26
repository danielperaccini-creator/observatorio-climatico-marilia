from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CIDADE = "Marília/SP"
LATITUDE = -22.21389
LONGITUDE = -49.94583
INICIO = "2026-10-01"
FIM = "2026-10-30"
FUSO = "America/Sao_Paulo"
MODELO = "era5"
API = "https://archive-api.open-meteo.com/v1/archive"
VARIAVEIS = ["temperature_2m_min", "temperature_2m_max", "precipitation_sum"]
DADOS = RAIZ / "dados"
ORIGINAL = DADOS / "originais" / "open_meteo.json"
METADADOS = DADOS / "originais" / "metadados.json"
BANCO = DADOS / "clima.duckdb"
EVIDENCIAS = RAIZ / "docs" / "evidencias"


def parametros():
    return {
        "latitude": LATITUDE, "longitude": LONGITUDE,
        "start_date": INICIO, "end_date": FIM,
        "daily": ",".join(VARIAVEIS), "timezone": FUSO,
        "temperature_unit": "celsius", "precipitation_unit": "mm",
        "models": MODELO,
    }
