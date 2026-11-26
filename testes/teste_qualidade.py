import copy
import json
import unittest
from decimal import Decimal

import duckdb

from banco import tratar
from config import BANCO, ORIGINAL


class QualidadeTest(unittest.TestCase):
    def setUp(self):
        self.original = json.loads(ORIGINAL.read_text(encoding="utf-8"))

    def alterar(self, campo, posicao, valor):
        dados = copy.deepcopy(self.original)
        dados["daily"][campo][posicao] = valor
        return dados

    def test_recorte_completo(self):
        self.assertEqual(len(tratar(self.original)), 30)

    def test_data_duplicada(self):
        with self.assertRaises(ValueError):
            tratar(self.alterar("time", 1, self.original["daily"]["time"][0]))

    def test_dia_ausente(self):
        dados = copy.deepcopy(self.original)
        for vetor in dados["daily"].values():
            vetor.pop()
        with self.assertRaises(ValueError):
            tratar(dados)

    def test_chuva_negativa(self):
        with self.assertRaises(ValueError):
            tratar(self.alterar("precipitation_sum", 0, -1))

    def test_minima_acima_da_maxima(self):
        with self.assertRaises(ValueError):
            tratar(self.alterar("temperature_2m_min", 0, 49))

    def test_texto_em_coluna_numerica(self):
        with self.assertRaises((ValueError, TypeError)):
            tratar(self.alterar("precipitation_sum", 0, "sem dado"))

    def test_nulo_preservado_sem_virar_zero(self):
        df = tratar(self.alterar("precipitation_sum", 0, None))
        self.assertTrue(df["precipitacao"].isna().iloc[0])

    def test_unidade_incorreta(self):
        dados = copy.deepcopy(self.original)
        dados["daily_units"]["precipitation_sum"] = "inch"
        with self.assertRaises(ValueError):
            tratar(dados)

    def test_infinito(self):
        with self.assertRaises(ValueError):
            tratar(self.alterar("temperature_2m_max", 0, float("inf")))

    def test_kpi_incompleto_nao_usa_soma_parcial(self):
        con = duckdb.connect()
        try:
            con.execute("CREATE TABLE clima_diario (precipitacao DOUBLE)")
            con.execute("INSERT INTO clima_diario SELECT CASE WHEN range = 0 THEN NULL ELSE 1 END FROM range(30)")
            valor = con.execute("SELECT CASE WHEN COUNT(precipitacao) = 30 THEN SUM(precipitacao) END FROM clima_diario").fetchone()[0]
            self.assertIsNone(valor)
        finally:
            con.close()

    def test_conferencia_independente_json_e_sql(self):
        diario = self.original["daily"]
        esperado = (max(diario["temperature_2m_max"]), min(diario["temperature_2m_min"]),
                    sum(Decimal(str(v)) for v in diario["precipitation_sum"]))
        con = duckdb.connect(str(BANCO), read_only=True)
        try:
            obtido = con.execute("SELECT MAX(temperatura_max), MIN(temperatura_min), ROUND(SUM(precipitacao), 2) FROM clima_diario").fetchone()
            self.assertEqual(obtido[:2], esperado[:2])
            self.assertEqual(Decimal(str(obtido[2])), esperado[2])
            self.assertEqual(con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0], 30)
        finally:
            con.close()


if __name__ == "__main__":
    unittest.main()
