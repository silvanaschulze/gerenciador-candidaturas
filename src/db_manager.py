import sqlite3

DB_PATH = "candidaturas.db"

# Função genérica para conectar ao banco de dados
def conectar_banco():
    """
    Cria e retorna uma conexão com o banco de dados definido em DB_PATH.
    """
    return sqlite3.connect(DB_PATH)

# Função para verificar duplicação
def verificar_duplicado(tabela, criterios, valores):
    """
    Verifica se um registro já existe no banco de dados com base em uma tabela e critérios fornecidos.
    
    Args:
        tabela (str): O nome da tabela no banco de dados.
        criterios (list): Lista de colunas a serem verificadas.
        valores (list): Lista de valores correspondentes aos critérios.

    Returns:
        bool: True se o registro já existir, False caso contrário.
    """
    conexao = conectar_banco()
    try:
        cursor = conexao.cursor()
        query = f"SELECT * FROM {tabela} WHERE " + " AND ".join([f"{coluna} = ?" for coluna in criterios])
        cursor.execute(query, valores)
        return cursor.fetchone() is not None
    finally:
        conexao.close()


def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # Criar tabela candidaturas
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

        # Criar tabela etapas
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

          # Salvar as alterações
        conexao.commit()

        # Verificar se as tabelas foram criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        tabelas_existentes = [tabela[0] for tabela in tabelas]

        if "candidaturas" in tabelas_existentes and "etapas" in tabelas_existentes:
            print("Tabelas candidaturas e etapas criadas/verificadas com sucesso!")
        else:
            print("Erro: Tabelas não foram criadas corretamente.")

    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    
    finally:
        conexao.commit()
        conexao.close()




    #Adicionar candidaturas

def adicionar_candidatura(data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback):
    """
    Adiciona uma nova candidatura ao banco de dados, se ela não for duplicada.
    """
    conexao = conectar_banco()  # Usa a função genérica para abrir conexão
    try:
        # Verificar duplicação usando a função verificar_duplicado
        if verificar_duplicado("candidaturas", ["data_candidatura", "email_enviado", "status_envio"], 
                               [data_candidatura, email_enviado, status_envio]):
            print("Candidatura já existe! Não será adicionada novamente.")
            return False  # Retorna False se a candidatura for duplicada
        else:
            # Inserir a nova candidatura
            cursor = conexao.cursor()
            cursor.execute("""
            INSERT INTO candidaturas (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback)
            VALUES (?, ?, ?, ?, ?)
            """, (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback))
            conexao.commit()
            print("Candidatura adicionada com sucesso!")
            return True  # Retorna True se a inserção for bem-sucedida
    except Exception as e:
        print(f"Erro ao adicionar candidatura: {e}")
        return False  # Retorna False se ocorrer um erro
    finally:
        conexao.close()


def pesquisar_candidaturas(criterio=None, valor=None):
    """
    Pesquisa candidaturas no banco de dados com base em um critério e valor específicos.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Validar se o critério fornecido é válido
    colunas_validas = ["data_candidatura", "email_enviado", "status_envio", "data_feedback", "resposta_feedback"]
    if criterio and criterio not in colunas_validas:
        raise ValueError(f"Critério inválido: {criterio}. Os critérios válidos são: {colunas_validas}")

    try:
        # Montar a consulta SQL com base nos critérios
        if criterio and valor:
            query = f"SELECT * FROM candidaturas WHERE {criterio} = ?"
            cursor.execute(query, (valor,))
        else:
            cursor.execute("SELECT * FROM candidaturas")

        resultado = cursor.fetchall()
        return resultado

    except sqlite3.Error as e:
        print(f"Erro ao pesquisar candidaturas: {e}")
        return []

    finally:
        conexao.close()


def listar_candidaturas():
    """
    Lista todas as candidaturas no banco de dados.
    """
    try:
        with conectar_banco() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM candidaturas")
            resultados = cursor.fetchall()
            return resultados
    except sqlite3.Error as e:
        print(f"Erro ao listar candidaturas: {e}")
        return []

def atualizar_registro(tabela, colunas_valores, criterio, valor):
    if not colunas_valores:
        print("Nenhuma coluna fornecida para atualizar.")
        return

    """
    Atualiza um registro no banco de dados com base em critérios fornecidos.
    
    Args:
        tabela (str): Nome da tabela a ser atualizada.
        colunas_valores (dict): Dicionário com colunas e seus novos valores.
        criterio (str): Coluna usada para filtrar o registro a ser atualizado.
        valor (any): Valor usado no critério.

    Returns:
        None
    """
    conexao = conectar_banco()
    try:
        cursor = conexao.cursor()
        colunas = ", ".join([f"{coluna} = ?" for coluna in colunas_valores.keys()])
        query = f"UPDATE {tabela} SET {colunas} WHERE {criterio} = ?"
        valores = list(colunas_valores.values()) + [valor]
        cursor.execute(query, valores)
        conexao.commit()
        print(f"Registro na tabela '{tabela}' atualizado com sucesso.")
        print(f"Colunas atualizadas: {colunas_valores}")
        print(f"Critério: {criterio} = {valor}")
       
    except sqlite3.Error as e:
        print(f"Erro ao atualizar registro na tabela {tabela}: {e}")
    finally:
        conexao.close()



def editar_candidatura(candidatura_id, data_candidatura=None, email_enviado=None, status_envio=None, data_feedback=None, resposta_feedback=None):
    """
    Atualiza uma candidatura com base nos parâmetros fornecidos.
    """
    # Montar os valores que serão atualizados
    valores = {}
    if data_candidatura:
        valores["data_candidatura"] = data_candidatura
    if email_enviado:
        valores["email_enviado"] = email_enviado
    if status_envio:
        valores["status_envio"] = status_envio
    if data_feedback:
        valores["data_feedback"] = data_feedback
    if resposta_feedback:
        valores["resposta_feedback"] = resposta_feedback

    # Se houver valores a serem atualizados, chamar a função genérica
    if valores:
        atualizar_registro("candidaturas", valores, "id", candidatura_id)

    else:
        print("Nenhuma informação foi fornecida para atualizar a candidatura.")

#Funcao para ADICIONAR as Etapas.
def adicionar_etapa(candidatura_id, etapa_numero, data, resultado):
    """
    Adiciona uma etapa a uma candidatura, se ela não for duplicada.
    """
    if verificar_duplicado("etapas", ["candidatura_id", "etapa_numero"], [candidatura_id, etapa_numero]):
        print(f"Etapa {etapa_numero} para a candidatura {candidatura_id} já existe! Não será adicionada novamente.")
    else:
        conexao = conectar_banco()
        try:
            cursor = conexao.cursor()
            cursor.execute("""
            INSERT INTO etapas (candidatura_id, etapa_numero, data, resultado)
            VALUES(?, ?, ?, ?)
            """, (candidatura_id, etapa_numero, data, resultado))
            conexao.commit()
            print(f"Etapa {etapa_numero} adicionada com sucesso!")
        finally:
            conexao.close()


 #Funcao para editar um etapa
def editar_etapa(etapa_id, data=None, resultado=None):
    """
    Atualiza uma etapa com base nos parâmetros fornecidos.
    """
    # Montar os valores que serão atualizados
    valores = {}
    if data:
        valores["data"] = data
    if resultado:
        valores["resultado"] = resultado

    # Se houver valores a serem atualizados, chamar a função genérica
    if valores:
      atualizar_registro("etapas", valores, "id", etapa_id)

    else:
        print("Nenhuma informação foi fornecida para atualizar a etapa.")


def excluir_candidatura(id_candidatura):
    """
    Exclui uma candidatura e suas etapas associadas do banco de dados.
    """
    conexao = conectar_banco()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM etapas WHERE candidatura_id = ?", (id_candidatura,))
        cursor.execute("DELETE FROM candidaturas WHERE id = ?", (id_candidatura,))
        conexao.commit()
        print(f"Candidatura {id_candidatura} e etapas associadas excluídas com sucesso!")
        return True  # Retorna True se a exclusão for bem-sucedida
    except Exception as e:
        print(f"Erro ao excluir candidatura: {e}")
        return False  # Retorna False se ocorrer um erro
    finally:
        conexao.close()


# Funcao para EXCLUIR etapas
def excluir_etapa(etapa_id):
    """
    Exclui uma etapa do banco de dados pelo ID.
    """
    try:
        with conectar_banco() as conexao:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM etapas WHERE id = ?", (etapa_id,))
            conexao.commit()
            print(f"Etapa {etapa_id} excluída com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir a etapa {etapa_id}: {e}")
