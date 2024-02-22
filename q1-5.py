import basedosdados as bd


query = "SELECT * FROM `datario.administracao_servicos_publicos.chamado_1746` LIMIT 10;"
query2 = "SELECT * FROM `datario.dados_mestres.bairro` LIMIT 10;"
query3 = "SELECT * FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` LIMIT 10;"




# QUESTÃO 1
query1 = "SELECT COUNT(*) AS total_chamados_abertos FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE DATE(data_inicio) = '2023-04-01';"

df = bd.read_sql(query1, billing_project_id= "dadosrio")

print(df.head())