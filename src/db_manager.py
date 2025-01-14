import sqlite3
import urllib.parse

DB_PATH = "candidaturas.db"

VALID_STATUSES = ["Enviado", "Pendente", "Arquivada", "Aguardando Retorno"]

"""
    Gera um link para abrir o local da entrevista no Google Maps.
    """
def gerar_link_google_maps(local_entrevista):
    base_url = "https://www.google.com/maps/search/?api=1&query="
    return base_url + urllib.parse.quote(local_entrevista)

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
            metodo_entrevista TEXT,
            local_entrevista TEXT,
            link_google_maps TEXT
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


#Adiciona as colunas 'local_entrevista' e 'link_google_maps' na tabela 'candidaturas', se ainda não existirem.

def atualizar_tabela_candidaturas():
    
    conexao = conectar_banco()
    try:
        cursor = conexao.cursor()
        # Adicionar a coluna 'local_entrevista' se não existir
        cursor.execute("PRAGMA table_info(candidaturas)")
        colunas = [info[1] for info in cursor.fetchall()]
        
        if "local_entrevista" not in colunas:
            cursor.execute("ALTER TABLE candidaturas ADD COLUMN local_entrevista TEXT")
            print("Coluna 'local_entrevista' adicionada com sucesso!")
        
        if "link_google_maps" not in colunas:
            cursor.execute("ALTER TABLE candidaturas ADD COLUMN link_google_maps TEXT")
            print("Coluna 'link_google_maps' adicionada com sucesso!")

        conexao.commit()
    except Exception as e:
        print(f"Erro ao atualizar a tabela 'candidaturas': {e}")
    finally:
        conexao.close()

# Chamar a função para garantir que a tabela está atualizada
atualizar_tabela_candidaturas()


# Gera um link para adicionar um evento ao Google Agenda.

def gerar_link_google_agenda(titulo, data_inicio, data_fim, descricao, local):
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE" 
    param = {
        "text" : titulo,
        "dates" : f"{data_fim}/{data_fim}",
        "details": descricao,
        "location": local,
    }
    return base_url + "&" + urllib.parse.urlencode(param)

    #Adicionar candidaturas
    

def adicionar_candidatura(data_candidatura, email_enviado, status_envio, data_feedback=None, resposta_feedback=None, local_entrevista=None):
    """
    Adiciona uma nova candidatura ao banco de dados, se ela não for duplicada.
    """
    # Verificar campos obrigatórios
    if not data_candidatura or not email_enviado or not status_envio:
        print("Os campos 'data_candidatura', 'email_enviado' e 'status_envio' são obrigatórios.")
        return False

    # Verificar se o status é válido
    if status_envio not in VALID_STATUSES:
        print(f"Status inválido: {status_envio}. Use um dos seguintes: {', '.join(VALID_STATUSES)}")
        return False

    # Gerar link do Google Maps, se o local for fornecido
    link_google_maps = None
    if local_entrevista:
        link_google_maps = gerar_link_google_maps(local_entrevista)

    # Exibir dados da candidatura antes de inserir
    print(f"Adicionando candidatura: data={data_candidatura}, email={email_enviado}, status={status_envio}, local={local_entrevista}")

    conexao = conectar_banco()  # Conectar ao banco de dados
    try:
        cursor = conexao.cursor()

        # Verificar duplicação
        if verificar_duplicado("candidaturas", ["data_candidatura", "email_enviado", "status_envio"], 
                               [data_candidatura, email_enviado, status_envio]):
            print("Candidatura já existe! Não será adicionada novamente.")
            return False  # Retorna False se for duplicada

        # Inserir a nova candidatura no banco de dados
        cursor.execute("""
            INSERT INTO candidaturas (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback, local_entrevista, link_google_maps)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_candidatura, email_enviado, status_envio, data_feedback, resposta_feedback, local_entrevista, link_google_maps))
        print(f"Candidatura adicionada: data={data_candidatura}, email={email_enviado}, status={status_envio}")

    # Salvar alterações no banco
        conexao.commit()
        print("Candidatura adicionada com sucesso!")
        return True  # Retorna True se a inserção for bem-sucedida
    except Exception as e:
        print(f"Erro ao adicionar candidatura: {e}")
        return False  # Retorna False se ocorrer um erro
    finally:
        conexao.close()  # Fecha a conexão com o banco
       


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
    Retorna todas as candidaturas do banco de dados.
    """
    conexao = conectar_banco()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM candidaturas")  # A consulta deve retornar todos os registros
        resultados = cursor.fetchall()
        print("Candidaturas retornadas pelo banco de dados:", resultados)  # Para depuração
        return resultados
    finally:
        conexao.close()


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
