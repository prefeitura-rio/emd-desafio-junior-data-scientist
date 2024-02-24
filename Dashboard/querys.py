import basedosdados as bd
# import pandas as pd

project_id = "dadosrio"
neighborhood_path = "datario.dados_mestres.bairro"
main_path = "datario.administracao_servicos_publicos.chamado_1746"
events_path = "datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos"


def apply_query(query):
  return bd.read_sql(query, billing_project_id= project_id)

# QUESTÃO 3 - Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia? ✅

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
df = apply_query(location_query)
print(df.values)