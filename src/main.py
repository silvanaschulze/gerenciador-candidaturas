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

print("\nAdicionando uma nova candidatura com o status 'Arquivada'...")
adicionar_candidatura(
    data_candidatura="2025-01-15",
    email_enviado="teste4@example.com",
    status_envio="Arquivada",
    local_entrevista="Rua Teste, 456, Rio de Janeiro, RJ"
)

print("\nAdicionando uma nova candidatura com o status 'Aguardando Retorno'...")
adicionar_candidatura(
    data_candidatura="2025-01-16",
    email_enviado="teste5@example.com",
    status_envio="Aguardando Retorno",
    local_entrevista="Av. Brasil, 789, São Paulo, SP"
)


# Listar candidaturas
candidaturas = listar_candidaturas()
print("Lista de Candidaturas:")
for candidatura in candidaturas:
    print(candidatura)

print("\nListando todas as candidaturas...")
candidaturas = listar_candidaturas()
for candidatura in candidaturas:
    print(candidatura)

# Exibir o link do Google Maps de uma candidatura
print("\nExibindo link do Google Maps para a última candidatura...")
ultima_candidatura = candidaturas[-1]  # Pegando o último registro
if ultima_candidatura[-1]:  # O link do Google Maps está na última coluna
    print(f"Link do Google Maps: {ultima_candidatura[-1]}")
else:
    print("Nenhum local definido para esta candidatura.")

# Pesquisar candidaturas
resultados = pesquisar_candidaturas("status_envio", "Enviado")
print("Candidaturas com status 'Enviado':")
for r in resultados:
    print(r)


