## Chamados do 1746 em grandes eventos
#### Utilize a tabela de Chamados do 1746 e a tabela de Ocupação Hoteleira em Grandes Eventos no Rio para as perguntas de 6-10. Para todas as perguntas considere o subtipo de chamado "Perturbação do sossego".

# 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?
# 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

main_path = "datario.administracao_servicos_publicos.chamado_1746"
hotels_path = "datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos"
project_id = "dadosrio"

# Questão 6 - Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

import basedosdados as bd


subtype_count_query = f"""
SELECT
  COUNT (*) 
FROM
  {main_path}
WHERE
  DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
  AND subtipo = 'Perturbação do sossego';
"""

df = bd.read_sql(subtype_count_query, billing_project_id= project_id)
# print(f"Quantidade de chamados abertos com subtipo Perturbaç!ao do sossego {df}")

# Questão 7 - Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).

specific_ocurrences_by_event = f"""
SELECT
  c.*
FROM
  {main_path} AS c
JOIN
  {hotels_path} AS e
ON
  DATE(c.data_inicio) BETWEEN DATE(e.data_inicial)
  AND DATE(e.data_final)
WHERE
  c.subtipo = 'Perturbação do sossego'
  AND e.evento IN ('Reveillon',
    'Carnaval',
    'Rock in Rio');
"""

df = bd.read_sql(specific_ocurrences_by_event, billing_project_id= project_id)
# print(f"Seleção de chamados abertos com subtipo Perturbação do sossego durante os eventos especificados: {df}")


# Questão 8 - Quantos chamados desse subtipo foram abertos em cada evento?

quantity_ocurrences_by_event = f"""
SELECT
  e.evento,
  COUNT(*) AS total_chamados
FROM
  {main_path} AS c
JOIN
  {hotels_path} AS e
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

df = bd.read_sql(quantity_ocurrences_by_event, billing_project_id= project_id)
print(f"Quantidade de chamados abertos com subtipo Perturbação do sossego para cada evento específico: {df}")
