# Escopo do Observatório Climático Local

Responsável: Daniel Ricardo S. Peraccini  
Curso: Tecnologia em Banco de Dados  
Local: Marília/SP  
Data de formalização: 26/11/2026

## Problema e necessidade proposta

As informações meteorológicas históricas precisam ser organizadas para que moradores que organizam atividades ao ar livre consigam consultar os extremos de temperatura e a chuva de um período sem ler arquivos técnicos. A necessidade será validada com o público em uma futura devolutiva. Não houve levantamento de campo nesta etapa.

## Objetivo

Coletar, validar, armazenar e apresentar 30 dias de dados históricos de Marília em indicadores, dois gráficos e uma tabela de consulta, com fonte e limites explícitos.

Recorte: 01 a 30/10/2026; coordenadas WGS84 -22.21389, -49.94583; fuso America/Sao_Paulo; modelo ERA5 da API histórica Open-Meteo. Variáveis: mínima e máxima a 2 m em °C e precipitação diária em mm. O dia 31 não faz parte do recorte.

## Perguntas

1. Qual foi a maior temperatura máxima e em quais dias ocorreu?
2. Qual foi a menor temperatura mínima e em quais dias ocorreu?
3. Qual foi a precipitação acumulada nos 30 dias?

KPIs: máximo das máximas, mínimo das mínimas e soma das precipitações; apresentar datas dos extremos e exigir 30/30 valores válidos por indicador. Visuais: série de linhas de mínimas e máximas; barras da precipitação diária; tabela dos 30 dias.

## Critérios de sucesso

- Receber e preservar o JSON real, com parâmetros e instante de coleta.
- Obter exatamente 30 datas consecutivas distintas para uma localidade.
- Validar as unidades, os tipos e as relações entre variáveis; registrar ausências sem imputação automática.
- Garantir que a reexecução da carga mantenha 30 linhas.
- Produzir três consultas e indicadores que confiram com o JSON original.
- Disponibilizar dois gráficos, tabela, fonte, unidades e limitações no painel.
- Permitir que outra pessoa reproduza a base a partir do README.
- Na etapa comunitária futura, verificar se o público identifica os extremos e distingue histórico de previsão, registrando dúvidas e ajustes sem expor dados pessoais.

## Responsabilidade e continuidade

Daniel será responsável pela coleta, tratamento, banco, consultas, documentação e preparação da apresentação. Não há planejamento anterior disponibilizado; este documento formaliza o escopo comum das duas atividades, sem atribuir ao trabalho datas ou etapas anteriores não registradas. A avaliação de entendimento e o feedback da comunidade dependem da devolutiva futura.
