import basedosdados as bd

main_path = "datario.administracao_servicos_publicos.chamado_1746"
neighborhood_path = "datario.dados_mestres.bairro"
events_path = "datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos"
project_id = "dadosrio"

def apply_query(query):
  return bd.read_sql(query, billing_project_id= project_id)


# QUESTÃO 1 - Quantos chamados foram abertos no dia 01/04/2023? ✅
quantity_query = f"""
SELECT
  COUNT(*) AS total_chamados_abertos
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01';
"""

df = apply_query(quantity_query)

print(f"\n\nO número total de chamados abertos em 2023-04-01 foi: {df.values[0]}\n\n")


# QUESTÃO 2 - Qual o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023? ✅

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

# df = apply_query(order_by_type_query)

# print(f"\n\n O tipo de chamado com maior número de ocorrências foi: {df}\n\n")

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
# df = apply_query(location_query)

# print(f"\n\n O nome dos 3 bairros com maior número de ocorrências é: {df}\n\n")

# QUESTÃO 4 - Qual o nome da subprefeitura com mais chamados abertos nesse dia? ✅

query_subprefecture = f"""
SELECT subprefeitura
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

# df = apply_query(query_subprefecture)
# print(f"O nome da subprefeitura com maior ocorrência neste dia: {df}")

# QUESTÃO 5 - Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece? ✅

null_query = f"""
SELECT *
FROM {main_path} AS c
LEFT JOIN {neighborhood_path} AS b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01' AND b.id_bairro IS NULL;
"""

# df = apply_query(null_query)
# print(f"Ocorrência não associada à bairro ou subprefeitura: {df}")

# Vários fatores podem justificar não ter prefeitura ou bairro associado, como falta de informações ao preencher ou ao não mapeamento, mas este em específico trata-se de um chamado do tipo "Ônibus" (como mostrado na query a seguir), uma verificação de ar condicionado, então, ao meu ver, não faz sentido ter um bairro associado, já que o ônibus pode percorrer vários bairros.


# Verificando o tipo de ocorrência que não foi associado à bairros e subprefeituras
type_query = f"""
SELECT tipo, status
FROM {main_path} AS c
LEFT JOIN {neighborhood_path} AS b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01' AND b.id_bairro IS NULL;
"""

# df = bd.read_sql(type_query, billing_project_id= project_id)
# print(f"Tipo de ocorrência não associada à bairro ou subprefeitura: {df}")


# QUESTÃO 6 - Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)? ✅

subtype_count_query = f"""
SELECT
  COUNT (*) 
FROM
  {main_path}
WHERE
  DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
  AND subtipo = 'Perturbação do sossego';
"""

# df = apply_query(subtype_count_query)
# print(f"Quantidade de chamados abertos com subtipo Perturbaç!ao do sossego {df}")

# QUESTÃO 7 - Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio). ✅

specific_ocurrences_by_event = f"""
SELECT
  c.*
FROM
  {main_path} AS c
JOIN
  {events_path} AS e
ON
  DATE(c.data_inicio) BETWEEN DATE(e.data_inicial)
  AND DATE(e.data_final)
WHERE
  c.subtipo = 'Perturbação do sossego'
  AND e.evento IN ('Reveillon',
    'Carnaval',
    'Rock in Rio');
"""

# df = apply_query(specific_ocurrences_by_event)
# print(f"Seleção de chamados abertos com subtipo Perturbação do sossego durante os eventos especificados: {df}")


# QUESTÃO 8 - Quantos chamados desse subtipo foram abertos em cada evento? ✅

quantity_ocurrences_by_event = f"""
SELECT
  e.evento,
  COUNT(*) AS total_chamados
FROM
  {main_path} AS c
JOIN
  {events_path} AS e
ON
  DATE(c.data_inicio) BETWEEN DATE(e.data_inicial)
  AND DATE(e.data_final)
WHERE
  c.subtipo = 'Perturbação do sossego'
  AND e.evento IN ('Reveillon',
    'Carnaval',
    'Rock in Rio')
GROUP BY
  e.evento;
"""

# df = apply_query(quantity_ocurrences_by_event)
# print(f"Quantidade de chamados abertos com subtipo Perturbação do sossego para cada evento específico: {df}")


# QUESTÃO 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?  ✅

bigger_mean_query = f"""
SELECT
  e.evento,
  COUNT(*) / TIMESTAMP_DIFF(DATE(MAX(c.data_inicio)), DATE(MIN(c.data_inicio)), DAY) AS media_diaria_chamados
FROM
  {main_path} AS c
JOIN
  {events_path} AS e
ON
  DATE(c.data_inicio) BETWEEN DATE(e.data_inicial)
  AND DATE(e.data_final)
WHERE
  c.subtipo = 'Perturbação do sossego'
  AND e.evento IN ('Reveillon',
    'Carnaval',
    'Rock in Rio')
GROUP BY
  e.evento
ORDER BY
  media_diaria_chamados DESC
LIMIT
  1;
""" 

# df = apply_query(bigger_mean_query)
# print(f"Maior média diária de chamados abertos com subtipo Perturbação do sossego para os eventos especificados: {df}")


# QUESTÃO 10 - Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023. ✅

comparisons_query = f"""
  -- Média diária durante os eventos específicos
WITH
  media_diaria_eventos AS (
  SELECT
    e.evento,
    COUNT(*) / TIMESTAMP_DIFF(DATE(MAX(c.data_inicio)), DATE(MIN(c.data_inicio)), DAY) AS media_diaria_chamados_evento
  FROM
    {main_path} AS c
  JOIN
    {events_path} AS e
  ON
    DATE(c.data_inicio) BETWEEN DATE(e.data_inicial)
    AND DATE(e.data_final)
  WHERE
    c.subtipo = 'Perturbação do sossego'
    AND e.evento IN ('Reveillon',
      'Carnaval',
      'Rock in Rio')
  GROUP BY
    e.evento ),
  -- Média diária durante todo o período
  media_diaria_total AS (
  SELECT
    COUNT(*) / TIMESTAMP_DIFF('2023-12-31', '2022-01-01', DAY) AS media_diaria_chamados_total
  FROM
    {main_path} AS c
  WHERE
    c.subtipo = 'Perturbação do sossego'
    AND DATE(c.data_inicio) BETWEEN '2022-01-01'
    AND '2023-12-31' )
    
  -- Combinando as médias diárias durante os eventos específicos com a média diária total
SELECT
  'Média Diária Durante Eventos' AS tipo_media,
  evento,
  media_diaria_chamados_evento AS media_diaria_chamados
FROM
  media_diaria_eventos
UNION ALL
SELECT
  'Média Diária Total' AS tipo_media,
  NULL,
  media_diaria_chamados_total
FROM
  media_diaria_total;
"""

# df = apply_query(comparisons_query)
# print(f"Comparações solicitadas: {df}")