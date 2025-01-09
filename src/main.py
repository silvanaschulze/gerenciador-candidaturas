from db_manager import criar_tabelas, adicionar_candidatura, listar_candidaturas, pesquisar_candidaturas, atualizar_registro, atualizar_tabela_candidaturas

# Criar tabelas no banco de dados
criar_tabelas()
atualizar_tabela_candidaturas()

atualizar_registro(
    "candidaturas",
    {"status_envio": "Aprovado", "data_feedback": "2025-01-10"},
    "id",
    1
)


# Adicionar uma candidatura
adicionar_candidatura(
    "2025-01-10",
    "teste1@example.com",
    "Arquivada",
    local_entrevista="Rua Exemplo, 123, São Paulo, SP"
)


# Listar candidaturas
candidaturas = listar_candidaturas()
print("Lista de Candidaturas:")
for candidatura in candidaturas:
    print(candidatura)

# Pesquisar candidaturas
resultados = pesquisar_candidaturas("status_envio", "Enviado")
print("Candidaturas com status 'Enviado':")
for r in resultados:
    print(r)


