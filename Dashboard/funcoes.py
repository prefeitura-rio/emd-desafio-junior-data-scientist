import basedosdados as bd
project_id = "dadosrio"


def executar_consulta(query):
  return bd.read_sql(query, billing_project_id= project_id)

def extrair_substring_array(df, key):
    all_values = df[key].tolist()

    str_values = [str(value) for value in all_values]

    cleaned_values = [value.strip("'") for value in str_values]

    str_list = ', '.join(cleaned_values)

    return str_list
