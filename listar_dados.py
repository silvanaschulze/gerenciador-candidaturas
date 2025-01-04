import sqlite3

def listar_dados(db_path):
    try:
        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM candidaturas")
        resultados = cursor.fetchall()
        print(f"Dados do banco de dados: {db_path}")
        for linha in resultados:
            print(linha)
        conexao.close()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados {db_path}: {e}")

# Bancos para comparar
listar_dados("/Users/silvanaschulze/Desktop/Projetos/Gerenciador_Candidatura/db/candidaturas.db")
listar_dados("/Users/silvanaschulze/projeto_candidaturas/candidaturas.db")

