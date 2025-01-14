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
    #Limpa o banco de dados antes de cada teste."""
        candidaturas = listar_candidaturas()  # Retorna todas as candidaturas no banco
        for c in candidaturas:
            excluir_candidatura(c[0])  # Exclui cada candidatura pelo ID

    
    def test_adicionar_candidatura(self):
#Teste para a função adicionar_candidatura."""
    # Adicionar candidatura 1
        resultado = adicionar_candidatura(
        "2025-01-06", "empresa@email.com", "Enviado",
        "2025-01-10", "Aguardando feedback"
    )
        self.assertTrue(resultado, "Erro ao adicionar a candidatura com email 'empresa@email.com'.")

    # Adicionar candidatura 2
        resultado_arquivada = adicionar_candidatura(
        "2025-01-20", "teste6@example.com", "Arquivada",
        local_entrevista="Rua Nova, 123, Curitiba, PR"
    )
        self.assertTrue(resultado_arquivada, "Erro ao adicionar a candidatura com email 'teste6@example.com'.")

    # Verificar as candidaturas adicionadas
        candidaturas = listar_candidaturas()
        print("Candidaturas retornadas pelo teste test_adicionar_candidatura:", candidaturas)
        self.assertIn("empresa@email.com", [c[2] for c in candidaturas],
                  "Erro: O email 'empresa@email.com' não foi encontrado na lista de candidaturas.")
        self.assertIn("teste6@example.com", [c[2] for c in candidaturas],
                  "Erro: O email 'teste6@example.com' não foi encontrado na lista de candidaturas.")



    def test_adicionar_candidatura_novo_status(self):
    #Teste para a adição de candidaturas com os novos status 'Arquivada' e 'Aguardando Retorno'."""
    # Adicionar uma candidatura com o status 'Arquivada'
        resultado_arquivada = adicionar_candidatura(
            "20-02-2025",
            "teste6@example.com",
            "Arquivada",
            local_entrevista="Rua Cruz abreu, 55, Fortaleza, CE"
    )
        self.assertTrue(resultado_arquivada, "Erro: A candidatura com o status 'Arquivada' não foi adicionada.")
        candidaturas = listar_candidaturas()

        
    # Adicionar uma candidatura com o status 'Aguardando Retorno'
        resultado_aguardando = adicionar_candidatura(
              "25-01-23",
              "teste7@example.com",
              "Aguardando Retorno",
             local_entrevista="Rua Capital Gustavo, 123 , Fortaleza, CE"
    )
        self.assertTrue(resultado_aguardando)

    # Listar candidaturas e verificar se os emails estão presentes
        candidaturas = listar_candidaturas()
        print("Candidaturas retornadas pelo teste:", candidaturas)  # Depuração

        self.assertIn("teste6@example.com", [c[2] for c in candidaturas],"Erro: O email 'teste6@example.com' não foi encontrado na lista de candidaturas.")
        self.assertIn("teste7@example.com", [c[2] for c in candidaturas])


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
