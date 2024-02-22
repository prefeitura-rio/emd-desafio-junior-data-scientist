import basedosdados as bd

main_path = "datario.administracao_servicos_publicos.chamado_1746"
neighborhood_path = "datario.dados_mestres.bairro"

# Questão 1 - Quantos chamados foram abertos no dia 01/04/2023? ✅
quantity_query = f"""
SELECT
  COUNT(*) AS total_chamados_abertos
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01';
"""

df = bd.read_sql(quantity_query, billing_project_id= "dadosrio")

# print(f"\n\nO número total de chamados abertos em 2023-04-01 foi: {df}\n\n")


# Questão 2 - Qual o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023? ✅

order_by_type_query = f"""
SELECT
  tipo,
  COUNT(*) AS total_ocorrencias
FROM
  {main_path}
GROUP BY
  tipo
ORDER BY
  total_ocorrencias DESC
LIMIT
  1;
"""

df = bd.read_sql(order_by_type_query, billing_project_id= "dadosrio")
# print(f"\n\n O tipo de chamado com maior número de ocorrências foi: {df}\n\n")

# Questão 3 - Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

location_query = f"""
SELECT nome 
FROM {neighborhood_path} 
WHERE id_bairro IN (
    SELECT id_bairro
    FROM (
        SELECT id_bairro, COUNT(*) AS recorrencia_bairro 
        FROM {main_path} 
        WHERE DATE(data_inicio) = '2023-04-01'
        GROUP BY id_bairro 
        ORDER BY recorrencia_bairro DESC 
        LIMIT 3
    )
);
"""
df = bd.read_sql(location_query, billing_project_id= "dadosrio")

# print(f"\n\n O nome dos 3 bairros com maior número de ocorrências é: {df}\n\n")

# Questão 4 - Qual o nome da subprefeitura com mais chamados abertos nesse dia?

query_subprefecture = f"""
SELECT nome, subprefeitura
FROM {neighborhood_path}
WHERE id_bairro IN (
    SELECT id_bairro
    FROM (
        SELECT id_bairro, COUNT(*) AS recorrencia_bairro 
        FROM {main_path}
        WHERE DATE(data_inicio) = '2023-04-01'
        GROUP BY id_bairro 
        ORDER BY recorrencia_bairro DESC 
        LIMIT 1
    )
);
"""

df = bd.read_sql(query_subprefecture, billing_project_id= "dadosrio")
# print(f"O nome do bairro e da subprefeitura com maior ocorrência neste dia: {df}")

# Questão 5 - Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

null_query = f"""
SELECT *
FROM {main_path} AS c
LEFT JOIN {neighborhood_path} AS b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01' AND b.id_bairro IS NULL;
"""

df = bd.read_sql(null_query, billing_project_id= "dadosrio")
# print(f"Ocorrência não associada à bairro ou subprefeitura: {df}")

# Vários fatores podem justificar não ter prefeitura ou bairro associado, como falta de informações ao preencher ou ao não mapeamento, mas este em específico trata-se de um chamado do tipo "Ônibus" (como mostrado na query a seguir), uma verificação de ar condicionado, então, ao meu ver, não faz sentido ter um bairro associado, já que o ônibus pode percorrer vários bairros.

type_query = f"""
SELECT tipo, status
FROM {main_path} AS c
LEFT JOIN {neighborhood_path} AS b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01' AND b.id_bairro IS NULL;
"""

df = bd.read_sql(type_query, billing_project_id= "dadosrio")
print(f"Tipo de ocorrência não associada à bairro ou subprefeitura: {df}")