-- Q1. Qual foi a maior temperatura máxima e em quais dias ela ocorreu?
SELECT data, temperatura_max AS maior_temperatura_c
FROM clima_diario
WHERE temperatura_max = (SELECT MAX(temperatura_max) FROM clima_diario)
  AND (SELECT COUNT(temperatura_max) FROM clima_diario) = 30
ORDER BY data;

-- Q2. Qual foi a menor temperatura mínima e em quais dias ela ocorreu?
SELECT data, temperatura_min AS menor_temperatura_c
FROM clima_diario
WHERE temperatura_min = (SELECT MIN(temperatura_min) FROM clima_diario)
  AND (SELECT COUNT(temperatura_min) FROM clima_diario) = 30
ORDER BY data;

-- Q3. Qual foi a precipitação acumulada nos 30 dias?
SELECT CASE WHEN COUNT(precipitacao) = 30 THEN ROUND(SUM(precipitacao), 2) END
           AS precipitacao_acumulada_mm,
       COUNT(precipitacao) AS dias_com_valor, COUNT(*) AS dias_no_banco
FROM clima_diario;

-- Série diária usada nos dois gráficos e na tabela do painel.
SELECT data, temperatura_min, temperatura_max, precipitacao
FROM clima_diario ORDER BY data;

-- Conferência da chave primária e da cobertura.
SELECT cidade, COUNT(*) AS registros, COUNT(DISTINCT data) AS datas_distintas,
       MIN(data) AS inicio, MAX(data) AS fim,
       COUNT(*) - COUNT(temperatura_min) AS min_ausentes,
       COUNT(*) - COUNT(temperatura_max) AS max_ausentes,
       COUNT(*) - COUNT(precipitacao) AS precipitacao_ausentes
FROM clima_diario GROUP BY cidade;
