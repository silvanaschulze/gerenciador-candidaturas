import sqlite3

DB_PATH = "candidaturas.db"

def criar_tabelas():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidaturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_candidatura TEXT NOT NULL,
        email_enviado TEXT NOT NULL,
        status_envio TEXT NOT NULL,
        data_feedback TEXT,
        resposta_feedback TEXT,
        status_resposta TEXT,
        data_entrevista TEXT,
        metodo_entrevista TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS etapas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidatura_id INTEGER NOT NULL,
        etapa_numero INTEGER NOT NULL,
        data TEXT NOT NULL,
        resultado TEXT NOT NULL,
        FOREIGN KEY (candidatura_id) REFERENCES candidaturas (id)
    )
    """)

    conexao.commit()
    conexao.close()
    print("Tabelas criadas com sucesso!")

def adicionar_candidatura (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback):
    conexao= sqlite3.connect(DB_PATH)
    cursor= conexao.cursor()

# Verificar se a candidatura já existe
    cursor.execute("""
    SELECT * FROM candidaturas
    WHERE data_candidatura = ? AND email_enviado = ? AND status_envio = ?
    """, (data_candidatura, email_enviado, status_envio))
    
    if cursor.fetchone():
        print("Candidatura já existe! Não será adicionada novamente.")
    else:
        cursor.execute("""
        INSERT INTO candidaturas (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback)
        VALUES (?, ?, ?, ?, ?)
        """, (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback))
        conexao.commit()
        print("Candidatura adicionada com sucesso!")
    
    conexao.close()

def pesquisar_candidaturas(criterio=None, valor =None):
    conexao=sqlite3.connect(DB_PATH)
    cursor=conexao.cursor()


 # Montar a consulta SQL com base nos critérios
    if criterio and valor:
        query = f"SELECT * FROM candidaturas WHERE {criterio} = ?"
        cursor.execute(query, (valor,))
    else:
        cursor.execute("SELECT * FROM candidaturas")
    
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def listar_candidaturas():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM candidaturas")
    resultados = cursor.fetchall()
    conexao.close()
    return resultados