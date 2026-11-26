# Observatório Climático Local - Marília/SP

Projeto Integrador Extensionista II · Tecnologia em Banco de Dados  
Daniel Ricardo S. Peraccini

Repositório público: [danielperaccini-creator/observatorio-climatico-marilia](https://github.com/danielperaccini-creator/observatorio-climatico-marilia). As [sete issues](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues) têm responsável e critério de conclusão; uma cópia das tarefas está em `docs/escopo-1/AE2-2/issues.md`.

## Objetivo e público

Organizar os dados históricos de temperatura e precipitação de Marília em uma consulta simples. O público previsto são moradores que organizam atividades ao ar livre. A proposta é ajudar esse público a entender a variação das temperaturas e da chuva no período analisado, sem transformar o histórico em previsão.

Não foram realizadas entrevistas nem devolutiva à comunidade nesta etapa. A necessidade é uma proposta de trabalho a ser validada com o público.

## Recorte

- Localidade: Marília/SP, Brasil. Ponto de referência: latitude -22.21389 e longitude -49.94583 (WGS84).
- Período: **01/10/2026 a 30/10/2026**, inclusive, com 30 dias consecutivos. Não inclui o dia 31.
- Fuso: `America/Sao_Paulo`.
- Fonte: [API histórica Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api), modelo `era5`.
- Variáveis: temperatura mínima diária a 2 m (°C), temperatura máxima diária a 2 m (°C) e precipitação acumulada diária (mm).
- Uma tabela principal: `clima_diario`; uma linha por cidade e data; chave primária composta `(cidade, data)`.

As coordenadas foram conferidas no [serviço de geocodificação Open-Meteo](https://geocoding-api.open-meteo.com/v1/search?name=Marilia&count=5&language=pt&countryCode=BR). A API meteorológica retorna as coordenadas da célula de grade efetivamente utilizada; elas estão preservadas nos metadados.

## Entregas e estágio atual

| Entrega | Documento | Conteúdo |
| --- | --- | --- |
| AE1 - implementação | `docs/escopo-1/AE2/AE1_Implementacao.pdf` | Relatório de 4 páginas, coleta, tratamento, banco, SQL e evidências. |
| AE2 - desenho da solução (AE2-2) | `docs/escopo-1/AE2-2/AE2_Desenho_da_Solucao.pdf` | Dicionário v1, modelo lógico, plano de qualidade, análise, diagrama, wireframe e tarefas. |

O primeiro enunciado tem o título AE1, mas cita AE2 no corpo e sugere a pasta `AE2`. Por isso, a pasta segue a sugestão e o arquivo mantém AE1 na identificação. O segundo é identificado no enunciado como AE2-2. Ambos usam o mesmo recorte. Não há documento de planejamento anterior a estes arquivos; o escopo está formalizado em `docs/escopo-1/AE1/planejamento.md`.

O desenho v1 registra as decisões da solução. A implementação dessas decisões também está disponível nesta entrega, incluindo o painel. A apresentação à comunidade e o registro de feedback continuam previstos para uma etapa posterior.

## Como executar

Requer Python 3.12 ou superior. Abra o terminal nesta pasta. No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe coleta.py
.\.venv\Scripts\python.exe banco.py
.\.venv\Scripts\python.exe analise.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

No Linux/macOS, use `.venv/bin/python` no lugar de `.\.venv\Scripts\python.exe`. Não é necessário ativar o ambiente. A coleta requer internet, usa Requests com timeout e tentativas para erros transitórios. O painel lê o banco pronto, em modo somente leitura, e não refaz a coleta a cada interação.

O banco e o JSON da execução estão incluídos. Para conferir a entrega sem depender da API, instale as dependências e execute somente `banco.py`, `analise.py` e o painel, nessa ordem. Uma nova execução de `coleta.py` atualiza o arquivo de entrada e preserva uma cópia datada da nova resposta original e seus metadados. Versões históricas da fonte podem mudar.

Os caminhos são resolvidos pela localização dos scripts. A tabela é criada com tipos explícitos e PK; a carga usa transação e `ON CONFLICT ... DO UPDATE`. Repetir `banco.py` mantém os mesmos 30 registros, sem duplicar linhas. O processo bloqueia carga de outro recorte sobre esta configuração.

## Perguntas e indicadores

| Pergunta | Cálculo | Unidade | Resultado da coleta entregue |
| --- | --- | --- | --- |
| Qual foi a maior temperatura máxima e em qual data? | `MAX(temperatura_max)` e todas as datas empatadas | °C | 32,5 °C em 08/10/2026 |
| Qual foi a menor temperatura mínima e em qual data? | `MIN(temperatura_min)` e todas as datas empatadas | °C | 12,3 °C em 19/10/2026 |
| Qual foi a precipitação acumulada nos 30 dias? | `SUM(precipitacao)` | mm | 166,4 mm em 30/30 dias válidos |

Cada KPI exige 30 valores presentes na variável correspondente. Se houver ausência, o banco preserva `NULL` e o painel informa indicador indisponível, sem apresentar uma soma parcial como total do período. Zero de precipitação é preservado como valor da fonte. O arquivo `consultas.sql` traz as três perguntas, a série diária e a conferência da cobertura.

## Organização

```text
coleta.py           coleta e preservação da resposta
banco.py            validação e carga no DuckDB
analise.py          execução do SQL e exportação dos resultados
app.py              painel Streamlit: três KPIs, dois gráficos e tabela
config.py           localidade, datas e parâmetros
consultas.sql       cinco consultas comentadas
requirements.txt    dependências da aplicação
testes/             verificações da qualidade e dos resultados
dados/
  originais/        JSON original, metadados e histórico datado
  clima.duckdb      banco pronto para consulta
  clima_tratado.csv registros tratados
docs/
  escopo-1/AE1/     escopo e critérios de sucesso
  escopo-1/AE2/     relatório de implementação
  escopo-1/AE2-2/   desenho, diagrama e wireframe
  evidencias/       validação, cargas, testes e resultados SQL
```

## Verificações

```powershell
.\.venv\Scripts\python.exe banco.py
.\.venv\Scripts\python.exe banco.py
.\.venv\Scripts\python.exe -m unittest discover -s testes -v
```

A evidência `docs/evidencias/cargas.jsonl` registra contagens antes e depois das cargas; `qualidade.json` registra a última validação. Os testes conferem duplicidade, falta de um dia, unidade incorreta, valores inválidos, ausência preservada, bloqueio de KPI incompleto e comparação independente dos indicadores SQL com o JSON original. Os dados alterados pelos testes ficam em memória e não substituem a base entregue.

## Limitações e cuidados

A ERA5 é uma reanálise que combina observações e modelagem. O ponto retornado representa uma célula espacial, não uma estação no endereço indicado nem todos os bairros de Marília. Os 30 dias não permitem definir normal climatológica, demonstrar mudança climática ou prever dias futuros. Não foram coletados umidade, sensação térmica, horários de eventos, alagamentos ou dados pessoais; não há base para concluir sobre esses temas.

O painel será apresentado com explicação dos extremos, do acumulado e das unidades. O entendimento do público deverá ser confirmado na devolutiva. Qualquer registro identificável, foto ou fala depende de autorização; a preferência será registrar apenas uma síntese anônima. Não há fotos, depoimentos ou resultados de participação inventados.

## Fonte e atribuição

Open-Meteo. [Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api). Dados de reanálise ERA5, Copernicus Climate Change Service/ECMWF, distribuídos pela Open-Meteo sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Consulta realizada em 26/11/2026. URL completa, modelo, parâmetros, instante, coordenadas retornadas e hash SHA-256 estão em `dados/originais/metadados.json`.

Referências técnicas: [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/), [pandas](https://pandas.pydata.org/docs/), [DuckDB](https://duckdb.org/docs/stable/clients/python/overview), [Streamlit](https://docs.streamlit.io/).
