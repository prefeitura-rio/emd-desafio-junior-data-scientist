import basedosdados as bd
project_id = "dadosrio"


def apply_query(query):
  return bd.read_sql(query, billing_project_id= project_id)