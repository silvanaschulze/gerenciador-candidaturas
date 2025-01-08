import sys
import os

# Adiciona o diretório principal ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from db_manager import adicionar_candidatura, excluir_candidatura, listar_candidaturas

class TestDBManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração inicial antes de todos os testes."""
        cls.banco_teste = "banco_teste.db"
        # Configuração inicial do banco de dados de teste (se aplicável)

    def setUp(self):
        """Executa antes de cada teste."""
        # Limpar dados ou reiniciar tabelas para cada teste
        candidaturas = listar_candidaturas()
        for c in candidaturas:
            if c[2] == "empresa@email.com":
                excluir_candidatura(c[0])

    def test_adicionar_candidatura(self):
        """Teste para a função adicionar_candidatura."""
        resultado = adicionar_candidatura(
            "2025-01-06", "empresa@email.com", "Enviado",
            "2025-01-10", "Aguardando feedback"
        )
        self.assertTrue(resultado)
        candidaturas = listar_candidaturas()
        self.assertIn("empresa@email.com", [c[2] for c in candidaturas])

    def test_excluir_candidatura(self):
        """Teste para a função excluir_candidatura."""
        adicionar_candidatura(
            "2025-01-06", "empresa@email.com", "Pendente",
            "2025-01-06", "Sem feedback"
        )
        candidaturas = listar_candidaturas()
        id_para_excluir = None
        for c in candidaturas:
            if c[2] == "empresa@email.com":
                id_para_excluir = c[0]

        self.assertIsNotNone(id_para_excluir)

        resultado = excluir_candidatura(id_para_excluir)
        self.assertTrue(resultado)
        candidaturas_atualizadas = listar_candidaturas()
        self.assertNotIn("empresa@email.com", [c[2] for c in candidaturas_atualizadas])

    @classmethod
    def tearDownClass(cls):
        """Executa após todos os testes."""
        pass

if __name__ == "__main__":
    unittest.main()
