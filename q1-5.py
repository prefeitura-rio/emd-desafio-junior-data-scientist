
# 1. Quantos chamados foram abertos no dia 01/04/2023? ✅
# 2. Qual o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023?
# 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?
# 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?
# 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?



import basedosdados as bd

main_path = "datario.administracao_servicos_publicos.chamado_1746"

# Question 1
quantity_query = f"SELECT COUNT(*) AS total_chamados_abertos FROM {main_path} WHERE DATE(data_inicio) = '2023-04-01';"

df = bd.read_sql(quantity_query, billing_project_id= "dadosrio")

# print(f"\n\nO número total de chamados abertos em 2023-04-01 foi: {df}\n\n")


# Question 2

order_by_type_query = f"SELECT tipo, COUNT(*) AS total_ocorrencias FROM {main_path} GROUP BY tipo ORDER BY total_ocorrencias DESC LIMIT 1;"

df = bd.read_sql(order_by_type_query, billing_project_id= "dadosrio")
print(df)