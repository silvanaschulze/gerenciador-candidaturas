from db_manager import criar_tabelas, adicionar_candidatura, listar_candidaturas, pesquisar_candidaturas 

# Criar tabelas no banco de dados
criar_tabelas()



# adicionar_candidatura("20-12-2024", "empresa1@example.com", "Enviado", "25-12-2024", "Pendente")
adicionar_candidatura(
    "20-12-2024", "empresa1@example.com", "Enviado", "25-12-2024", "Pendente"
)
print("comente o primeiro teste")

#lista Candidaturas
candidaturas = listar_candidaturas()
print("Lista de Candidaturas:")
for candidatura in candidaturas:
    print(candidatura)



# Pesquisar candidaturas com status "Enviado"
resultados = pesquisar_candidaturas("status_envio", "Enviado")
print("Candidaturas com status 'Enviado':")
for r in resultados:
    print(r)