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
