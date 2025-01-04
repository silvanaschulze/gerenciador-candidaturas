import sqlite3

# Conectar (ou criar) ao banco de dados
conexao = sqlite3.connect("candidaturas.db")

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Apagar a tabela candidaturas, se já existir
cursor.execute("DROP TABLE IF EXISTS candidaturas")


# Criar a tabela para armazenar as candidaturas
cursor.execute("""
CREATE TABLE candidaturas (
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

# Apagar tabela de etapas, se ela existir
cursor.execute(" DROP TABLE IF EXISTS etapas")
#Criar a tabela etapas
cursor.execute("""
CREATE TABLE etapas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidatura_id INTEGER NOT NULL,
    etapa_numero INTEGER NOT NULL,
    data TEXT NOT NULL,
    resultado TEXT NOT NULL,
    FOREIGN KEY (candidatura_id) REFERENCES candidaturas (id)
)
""")

# Salvar alterações e fechar a conexão
conexao.commit()
conexao.close()


"""
Apos a criacao das tabelas acima, vamos criar funcoes que permitem: Adicionar candidaturas, Adicionar
etapas relacionada a uma candidatura, Listar as candidaturas, Listar as estapas de uma candidatura.
"""

#Funcao para ADICIONAR  as Candidaturas.
def adicionar_candidatura (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback):
    conexao= sqlite3.connect("candidaturas.db")
    cursor= conexao.cursor()

    cursor.execute("""
    INSERT INTO candidaturas (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback)
    values (?, ?, ? ,?, ?)
""", (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback ))
    
    conexao.commit()
    conexao.close()
print("Candidatura adicionada com sucesso!")

#Funcao para ADICIONAR as Etapas.
def adicionar_etapa (candidatura_id, etapa_numero, data, resultado):
    conexao= sqlite3.connect("candidaturas.db")
    cursor=conexao.cursor()

    cursor.execute("""
    INSERT INTO etapas (candidatura_id, etapa_numero, data, resultado)
    VALUES(?, ?, ?, ?)
    """, (candidatura_id, etapa_numero, data, resultado))

    conexao.commit()
    conexao.close()
    print(f"Etapas {etapa_numero} adicionada a candidatura {candidatura_id} com sucesso! ")

#Funcao para LISTAR as candidaturas
def listar_candidaturas():
    conexao= sqlite3.connect("candidaturas.db")
    cursor= conexao.cursor()

    cursor.execute("SELECT * FROM candidaturas")
    resultados = cursor.fetchall()

    for linha in resultados:
        print(linha)

    conexao.close()

#Funcao para LISTAR as etapas
def listar_etapas(candidatura_id):
    conexao = sqlite3.connect("candidaturas.db")
    cursor= conexao.cursor()

    cursor.execute("""
    SELECT etapa_numero, data, resultado
    FROM etapas
    WHERE candidatura_id = ?
    ORDER BY etapa_numero
    """, (candidatura_id,))

    resultados = cursor.fetchall()
    conexao.close()
    print(f"Etapas da candidatura {candidatura_id}:")
    for etapas in resultados:
        print(f"Etapas {etapas[0]}: Data: {etapas[1]}, Resultados: {etapas[2]}")

# Adicionar uma Candidatura
adicionar_candidatura( 
    "20-12-2024", 
    "empresa@example.com", 
    "Enviado", 
    "25-12-2024", 
    "Pendente"
)


#Adicionar etapas para candidatura 1
adicionar_etapa( 1, 1, "10-01-2025", "Aprovado")
adicionar_etapa(1,2, "15-01-2025", "Reprovado")

#listar todas as candidaturas
listar_candidaturas()

#Listar as etapas de candidatura 1
listar_etapas(1)

#Criar uma funcao que permita atualizar as informacoes de uma candidatura especifica
def editar_candidatura(candidatura_id, data_candidatura=None, email_enviado=None, status_envio=None, data_feedback=None, resposta_feedback=None):
    conexao= sqlite3.connect("candidaturas.db")
    cursor=conexao.cursor()

#Atualizar apenas os campos fornecidos
    if data_candidatura:
        cursor.execute("UPDATE candidaturas SET data_candidatura = ? WHERE id = ? ", (data_candidatura, candidatura_id))
    if email_enviado:
        cursor.execute("UPDATE candidaturas SET email_enviado = ? WHERE id = ?", (email_enviado, candidatura_id))
    if status_envio:
        cursor.execute("UPDATE candidaturas SET status_envio = ? WHERE id = ?", (status_envio, candidatura_id))    
    if data_feedback:
        cursor.execute("UPDATE candidaturas SET data_feedback = ? WHERE id = ?", (data_feedback, candidatura_id))
    if resposta_feedback:
        cursor.execute("UPDATE candidaturas SET resposta_feedback = ? WHERE id = ?", (resposta_feedback, candidatura_id))
    
    conexao.commit()
    conexao.close()
    print(f"Candidatura {candidatura_id} atualizada com sucesso!!")

#Funcao para editar um etapa
def editar_etapa(etapa_id, data=None, resultado=None):
    conexao = sqlite3.connect("candidaturas.db")
    cursor= conexao.cursor()

    if data:
        cursor.execute("UPDATE etapas SET data = ? WHERE id = ?", (data, etapa_id))
    if resultado:
        cursor.execute("UPDATE etapas SET resultado = ? WHERE id = ?", (resultado, etapa_id))

    conexao.commit()
    conexao.close()
    print(f"Etapa {etapa_id} atualizada com sucesso!")

#Funcao para EXCLUIR candidatura
def excluir_candidatura(candidatura_id):
    conexao= sqlite3.connect("candidaturas.db")
    cursor=conexao.cursor()
# Exckuir etapas associadas a candidatura
    cursor.execute(" DELETE FROM etapas WHERE candidatura_id = ?", (candidatura_id,))
# Excluir a candidatua
    cursor.execute("DELETE FROM candidaturas WHERE id = ?", (candidatura_id,))

    conexao.commit()
    conexao.close()
    print(f"Candidatura {candidatura_id} e etapas associadas excluídas com sucesso!")

# Funcao para EXCLIUR etapas
def excluir_etapa(etapa_id):
    conexao= sqlite3.connect("candidaturas.db")
    cursor = conexao.cursor()
# Excluir a etapa
    cursor.execute("DELETE FROM etapas WHERE id = ?", (etapa_id,))
    conexao.commit()
    conexao.close()
    print(f"Etapa {etapa_id} excluída com sucesso!")

#AREA DE TESTES
# Testar edição de uma candidatura
editar_candidatura(1, status_envio="Atualizado", resposta_feedback="Aceito")

# Testar edição de uma etapa
editar_etapa(1, data="12-01-2025", resultado="Aprovado com Mérito")

# Testar exclusão de uma etapa
excluir_etapa(2)

# Testar exclusão de uma candidatura (inclui exclusão de etapas associadas)
excluir_candidatura(1)

