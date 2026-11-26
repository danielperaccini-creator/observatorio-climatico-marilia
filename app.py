import duckdb
import pandas as pd
import streamlit as st

from config import BANCO, CIDADE, FIM, INICIO

st.set_page_config(page_title="Observatório Climático Local | Marília", layout="wide")
st.title("Observatório Climático Local")
st.subheader(CIDADE)
st.write("Período histórico: 01/10/2026 a 30/10/2026 · 30 dias")
st.write("Temperaturas e chuva para apoiar a leitura do tempo por moradores que organizam atividades ao ar livre.")

if not BANCO.exists():
    st.info("Prepare o banco antes de abrir o painel: execute coleta.py e depois banco.py.")
    st.stop()

con = duckdb.connect(str(BANCO), read_only=True)
try:
    df = con.execute("""SELECT data, temperatura_min, temperatura_max, precipitacao
        FROM clima_diario WHERE cidade = ? AND data BETWEEN ? AND ? ORDER BY data""",
        [CIDADE, INICIO, FIM]).df()
finally:
    con.close()

if len(df) != 30:
    st.error("O banco não contém os 30 dias esperados. Confira a carga.")
    st.stop()

def formato(valor, unidade):
    return "Indisponível" if pd.isna(valor) else f"{valor:.1f}".replace(".", ",") + " " + unidade

cols = st.columns(3)
for col, campo, titulo, operacao, unidade in [
    (cols[0], "temperatura_max", "Maior temperatura máxima", "max", "°C"),
    (cols[1], "temperatura_min", "Menor temperatura mínima", "min", "°C"),
    (cols[2], "precipitacao", "Precipitação acumulada", "sum", "mm"),
]:
    completo = df[campo].notna().sum() == 30
    valor = getattr(df[campo], operacao)() if completo else None
    col.metric(titulo, formato(valor, unidade))
    if not completo:
        col.caption(f"Cobertura: {df[campo].notna().sum()}/30 dias. Indicador não calculado.")
    elif campo != "precipitacao":
        datas = df.loc[df[campo] == valor, "data"].dt.strftime("%d/%m/%Y")
        col.caption("Ocorrência: " + ", ".join(datas))

st.subheader("Temperaturas diárias (°C)")
temperaturas = df.rename(columns={"data": "Data", "temperatura_min": "Mínima (°C)", "temperatura_max": "Máxima (°C)"})
st.line_chart(temperaturas, x="Data", y=["Mínima (°C)", "Máxima (°C)"])
st.subheader("Precipitação diária (mm)")
chuva = df.rename(columns={"data": "Data", "precipitacao": "Precipitação (mm)"})
st.bar_chart(chuva, x="Data", y="Precipitação (mm)")
st.subheader("Consulta dos registros")
exibicao = df.rename(columns={"data": "Data", "temperatura_min": "Mínima (°C)",
    "temperatura_max": "Máxima (°C)", "precipitacao": "Precipitação (mm)"})
st.dataframe(exibicao, hide_index=True)
st.download_button("Baixar registros em CSV", df.to_csv(index=False).encode("utf-8-sig"),
    file_name="clima_marilia_outubro_2026.csv", mime="text/csv")
st.caption("Fonte: Open-Meteo Historical Weather API · reanálise ERA5 (Copernicus/ECMWF) · temperaturas a 2 m · °C e mm.")
st.markdown("[Documentação da fonte](https://open-meteo.com/en/docs/historical-weather-api)")
st.info("São estimativas históricas de uma célula de grade. A chuva pode variar entre bairros. "
        "Os 30 dias não representam o clima típico da cidade e não permitem prever o tempo. "
        "Para decidir sobre uma atividade futura, consulte previsões e alertas oficiais atualizados.")
