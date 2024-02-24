import funcoes
import streamlit as st
import plotly.express as px
import pandas as pd

project_id = "dadosrio"
main_path = "datario.administracao_servicos_publicos.chamado_1746"
neighborhood_path = "datario.dados_mestres.bairro"
events_path = "datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos"


st.title("Escritório de dados do Rio de Janeiro - Dashboard Datario")

st.header("Parte 1 - Análise dos bairros do Rio de Janeiro")

quantity_neighboors = funcoes.apply_query(f"SELECT COUNT(*) FROM {neighborhood_path};")
st.write(f"☝️ Atualmente, a cidade do Rio de Janeiro possui {quantity_neighboors.values[0]} bairros, mais do que São Gonçalo [com 91 bairros oficiais], Itaguaí [41] e Saquarema [14] juntos - que são cidades vizinhas.")


st.subheader("Análise Visual")
st.write(f"Gráfico dos 5 maiores bairros do Rio. ")

# GRÁFICO 1 - barras: 5 maiores bairros

area_query = funcoes.apply_query(f"SELECT nome, area FROM {neighborhood_path} ORDER BY area DESC LIMIT 5;")
df = pd.DataFrame(area_query, columns=["nome", "area"])
st.bar_chart(df.set_index('nome'))

# GRÁFICO 2 - pizza: maior cidade em relação à área total

areatotal = 1200000000
area_maior = float(df.iloc[0][1])

porcentagem = (area_maior / areatotal) * 100

nome_bairro = str(df.iloc[0][0])

# Criar um DataFrame para plotagem
dados = {'Área': [f'{nome_bairro}', 'Rio de Janeiro'],
         'Porcentagem': [porcentagem, 100 - porcentagem]}
df = pd.DataFrame(data=dados)

# Plotar o gráfico de pizza usando Plotly Express
custom_layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",  # Define uma cor transparente para o fundo do gráfico
        "plot_bgcolor": "rgba(0,0,0,0)",   # Define uma cor transparente para o fundo do plot
        "font": {"color": "#2a3f5f"},      # Define a cor do texto
        "colorway": ['#1f77b4', '#aec7e8', '#7f7f7f', '#98df8a', '#2ca02c', '#d62728', '#ff7f0e', '#ffbb78', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']  # Tons de azul
}
fig = px.pie(df, values='Porcentagem', names='Área', title=f'Porcentagem da área o bairro de {nome_bairro} em relação à Área Total da cidade. Muita coisa, né?')
fig.update_layout(custom_layout)  # Aplica o layout personalizado
st.plotly_chart(fig)

# GRÁFICO 3 - prefeituras mais atuantes
st.write("Cada bairro tem a sua subprefeitura, como acontece nas demais cidades do Brasil. No caso do Rio, algumas se repetem bastante, conforme mostrado no gráfico a seguir.")

subpre_query = f"SELECT subprefeitura, COUNT(*) AS Recorrencia FROM {neighborhood_path} GROUP BY subprefeitura ORDER BY Recorrencia DESC LIMIT 5;"
subpre_dados = funcoes.apply_query(subpre_query)
subprefeituras = pd.DataFrame(subpre_dados, columns=["subprefeitura", "Recorrencia"])
st.bar_chart(subprefeituras.set_index('subprefeitura'))
# colocar gráfico do mapa aqui!


st.header("Parte 2 - Análise dos chamados efetuados no Rio de Janeiro")

# GRÁFICO 4 - 1o tipo de chamado mais recorrente

os_type = funcoes.apply_query(f"SELECT tipo, COUNT(*) AS total_ocorrencias FROM {main_path} GROUP BY tipo ORDER BY total_ocorrencias DESC LIMIT 1;")
os_most_recurrent_type = os_type.values[0][0]

st.write(f"☝️ Abrindo a seção dos chamados, o tipo mais recorrente em termos de solicitação foi [{str(os_most_recurrent_type)}], com [{str(os_type.values[0][1])}] chamados!")


# GRÁFICO 4 - gráfico por tipo de chamado mais recorrente usando latitude e longitude

st.write("Nesse gráfico, está disposto um mapa com as localizações com uma amostra de 1000 chamados da tabela consultada. Será que podemos extrair algum padrão daqui? Percebe que eles tendem a aparecer mais em algumas localidades do gráfico?")
# Consulta SQL para obter os 100 primeiros chamados com linhas válidas
consulta_chamados = f"SELECT latitude, longitude FROM {main_path} WHERE latitude IS NOT NULL AND longitude IS NOT NULL LIMIT 1000;"
dados_chamados = funcoes.apply_query(consulta_chamados)

# Verificar se há dados válidos para plotar
if isinstance(dados_chamados, pd.DataFrame) and not dados_chamados.empty:
    # Verificar se ainda há dados válidos para plotar
    if dados_chamados['latitude'].notnull().any() and dados_chamados['longitude'].notnull().any():
        # Plotar os pontos no mapa
        st.map(dados_chamados)
    else:
        st.warning("Não há dados válidos de latitude e longitude disponíveis para plotar.")
else:
    st.warning("Não há dados de latitude e longitude disponíveis para plotar.")


# INFO - dia com mais chamados abertos em relação aos demais

# Consulta dia com mais chamados
dia_mais_chamados_query = f"""
SELECT COUNT(*) AS total_chamados 
FROM {main_path} 
WHERE DATE(data_inicio) = (
    SELECT DATE(data_inicio) 
    FROM `datario.administracao_servicos_publicos.chamado_1746` 
    GROUP BY DATE(data_inicio) 
    ORDER BY COUNT(*) DESC 
    LIMIT 1
);
"""

quant_chamados_dia_mais_chamados = funcoes.apply_query(dia_mais_chamados_query)
quant_chamados_dia_mais_chamados = quant_chamados_dia_mais_chamados.iloc[0]['total_chamados']

quant_total_chamados = funcoes.apply_query(f"SELECT COUNT(*) AS total_chamados FROM {main_path} ;")
quant_total_chamados = quant_total_chamados.iloc[0]['total_chamados']

# Calcular a porcentagem de chamados em relação ao dia com mais chamados
porcentagem_dia_mais_chamados = (quant_chamados_dia_mais_chamados / quant_total_chamados) * 100

# Exibir o valor absoluto e a porcentagem
st.write(f"☝️ No dia com mais chamados, foram registrados {quant_chamados_dia_mais_chamados} chamados, o que representa apenas {porcentagem_dia_mais_chamados:.2f}% do total de chamados.")

#  GRÁFICO 5 - analise dos chamados por status

# Lista de status desejados
status_desejados = ['Fechado com solução', 'Em andamento', 'Fechado com providências', 'Sem possibilidade de atendimento']

# Consulta para contar o número de chamados por status
consulta_chamados_por_status = f"""
SELECT status, COUNT(*) AS total_chamados
FROM {main_path}
WHERE status IN {tuple(status_desejados)}
GROUP BY status
"""

# Aplicar a consulta e verificar se o DataFrame é válido
dados_chamados_por_status = funcoes.apply_query(consulta_chamados_por_status)
if isinstance(dados_chamados_por_status, pd.DataFrame) and not dados_chamados_por_status.empty:
    
    # Define um layout personalizado com tonalidades de azul

    # Plota o gráfico de pizza com o layout personalizado
    st.write(" > Distribuição dos chamados por status:")
    fig = px.pie(dados_chamados_por_status, values='total_chamados', names='status', title='Distribuição dos chamados por status')
    fig.update_layout(custom_layout)  # Aplica o layout personalizado
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Não há dados de chamados disponíveis para plotar.")


# INFO - tempo médio de resolução dos casos
# Consulta para calcular o tempo médio de resolução dos chamados
consulta_tempo_medio_resolucao = f"""
SELECT AVG(tempo_prazo) AS tempo_medio_resolucao
FROM {main_path}
WHERE tempo_prazo IS NOT NULL
"""

# Aplicar a consulta e verificar se o resultado é válido
resultado_tempo_medio_resolucao = funcoes.apply_query(consulta_tempo_medio_resolucao)
if isinstance(resultado_tempo_medio_resolucao, pd.DataFrame) and not resultado_tempo_medio_resolucao.empty:
    # Extrair o tempo médio de resolução dos chamados
    tempo_medio_resolucao = resultado_tempo_medio_resolucao.iloc[0]['tempo_medio_resolucao']

    # Exibir o tempo médio de resolução dos chamados
    st.write(f" > Ressalto que o tempo médio de resolução dos chamados é de aproximadamente {tempo_medio_resolucao:.2f} dias.")
else:
    st.warning("Não há dados de tempo de prazo disponíveis para calcular o tempo médio de resolução dos chamados.")


# GRÁFICO 5 - chamados por trimestre


trimestres_query = f"""
SELECT
  EXTRACT(YEAR FROM data_inicio) AS ano,
  CASE
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 1 AND 3 THEN '1º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 4 AND 6 THEN '2º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 7 AND 9 THEN '3º trimestre'
    WHEN EXTRACT(MONTH FROM data_inicio) BETWEEN 10 AND 12 THEN '4º trimestre'
  END AS trimestre,
  COUNT(*) AS total_chamados
FROM
  {main_path}
GROUP BY
  ano,
  trimestre
ORDER BY
  ano,
  trimestre;
"""

# Executar a consulta
resultados = funcoes.apply_query(trimestres_query)

# Definir as cores personalizadas
custom_colors = ['#1f77b4', '#aec7e8', '#7f7f7f', '#98df8a', '#2ca02c']

# Criar o gráfico de barras com Plotly Express
fig = px.bar(resultados, x='trimestre', y='total_chamados', color='ano', barmode='group', 
             title='Distribuição dos Chamados ao Longo do Tempo por Trimestre/Ano', color_discrete_sequence=custom_colors)

# Exibir o gráfico
st.plotly_chart(fig)


st.header("Parte 3 - Análise pela perspectiva do turismo em alguns eventos do Rio de Janeiro")

eventos_query = f"""
SELECT DISTINCT evento
FROM {events_path};
"""

eventos = funcoes.apply_query(eventos_query)

# Extrair todas as strings em uma única lista -- TRANSFORMAR EM
todas_as_strings = eventos['evento'].tolist()

# Remover as aspas de cada string na lista
todas_as_strings = [evento.strip("'") for evento in todas_as_strings]

# Juntar todas as strings em uma única string, separadas por vírgula
string_resultante = ', '.join(todas_as_strings)



st.write(f"Os maiores eventos realizados são: {string_resultante}.")

media_taxa_query = f"""
SELECT evento, AVG(taxa_ocupacao) AS media_taxa_ocupacao
FROM {events_path}
GROUP BY evento;

"""

# GRÁFICO 6 - média das taxas por evento

dados_eventos = funcoes.apply_query(media_taxa_query)
fig = px.bar(dados_eventos, x='evento', y='media_taxa_ocupacao', 
             title='Média da Taxa de Ocupação por Evento',
             labels={'media_taxa_ocupacao': 'Taxa de Ocupação Média (%)'})

# Personalizar layout
fig.update_layout(xaxis_title='Evento', yaxis_title='Taxa de Ocupação Média (%)')

# Exibir o gráfico
st.plotly_chart(fig)

# GRÁFICO 7 - média de chamados por evento
consulta_evento = f"""
SELECT eventos.evento, COUNT(chamados.id_chamado) AS num_chamados
FROM {main_path} AS chamados
JOIN {events_path} AS eventos
ON chamados.data_inicio >= eventos.data_inicial
AND chamados.data_inicio <= eventos.data_final
GROUP BY eventos.evento;


"""
dados_eventos_chamados_sql = funcoes.apply_query(consulta_evento)
# Verificar se há dados válidos para plotar
if isinstance(dados_eventos_chamados_sql, pd.DataFrame) and not dados_eventos_chamados_sql.empty:
    # Plotar o gráfico de barras
    st.write("Número de Chamados por Evento:")
    fig = px.bar(dados_eventos_chamados_sql, x='evento', y='num_chamados', title='Número de Chamados por Evento')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Não há dados de eventos disponíveis para plotar.")

st.header("Parte 4 - Sobre a data 01/04/2023")
st.write("Que dados podemos extrair sobre esta data?")
# INFO - tipo de chamado mais recorrente nesta data

# Consulta para obter o tipo de chamado com mais ocorrências na data especificada
order_by_type_query = f"""
SELECT
  tipo,
  COUNT(*) AS total_ocorrencias
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01'
GROUP BY
  tipo
ORDER BY
  total_ocorrencias DESC
LIMIT
  1;
"""

# Consulta para obter o total de chamados abertos na data especificada
quantity_query = f"""
SELECT
  COUNT(*) AS total_chamados_abertos
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01';
"""

# Executar as consultas
quantity_result = funcoes.apply_query(quantity_query)
result = funcoes.apply_query(order_by_type_query)

# Consulta para obter o tipo de chamado com mais ocorrências na data especificada
order_by_type_query = f"""
SELECT
  tipo,
  COUNT(*) AS total_ocorrencias
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01'
GROUP BY
  tipo
ORDER BY
  total_ocorrencias DESC
LIMIT
  1;
"""

# Consulta para obter o total de chamados abertos na data especificada
quantity_query = f"""
SELECT
  COUNT(*) AS total_chamados_abertos
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01';
"""

# Executar as consultas
quantity_result = funcoes.apply_query(quantity_query)
result = funcoes.apply_query(order_by_type_query)

# Consulta para obter o tipo de chamado com mais ocorrências na data especificada
order_by_type_query = f"""
SELECT
  tipo,
  COUNT(*) AS total_ocorrencias
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01'
GROUP BY
  tipo
ORDER BY
  total_ocorrencias DESC
LIMIT
  1;
"""

# Consulta para obter o total de chamados abertos na data especificada
quantity_query = f"""
SELECT
  COUNT(*) AS total_chamados_abertos
FROM
  {main_path}
WHERE
  DATE(data_inicio) = '2023-04-01';
"""

# Executar as consultas
quantity_result = funcoes.apply_query(quantity_query)
result = funcoes.apply_query(order_by_type_query)

# Verificar se as consultas retornaram resultados
if isinstance(quantity_result, pd.DataFrame) and isinstance(result, pd.DataFrame) and not result.empty:
    # Exibir o tipo de chamado com mais ocorrências
    st.write(f"O tipo de chamado que mais foi aberto nesta data foi: {result.iloc[0]['tipo']} com {result.iloc[0]['total_ocorrencias']} chamados do total de {quantity_result.iloc[0]['total_chamados_abertos']}.")

    # Calcular a porcentagem do tipo específico em relação ao total de chamados
    porcentagem_tipo_especifico = (result.iloc[0]['total_ocorrencias'] / quantity_result.iloc[0]['total_chamados_abertos']) * 100

    # Criar um DataFrame com esses dados
    dados = {'Categoria': [f"{result.iloc[0][0]}", 'Outros Tipos'],
             'Total de Chamados': [result.iloc[0]['total_ocorrencias'], quantity_result.iloc[0]['total_chamados_abertos'] - result.iloc[0]['total_ocorrencias']]}
    df = pd.DataFrame(data=dados)

    # Plotar o gráfico de pizza
    st.write("Distribuição dos chamados por tipo:")
    fig = px.pie(df, values='Total de Chamados', names='Categoria', title=f'Distribuição dos chamados por tipo específico ({porcentagem_tipo_especifico:.2f}%)')
    
    # Especificar a paleta de cores
    fig.update_traces(marker=dict(colors=['#1f77b4', '#aec7e8']))  # Tons de azul
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Não há dados disponíveis para a data especificada.")


# INFO - bairros com mais chamados abertos nesse dia
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

bairros = funcoes.apply_query(location_query)
# Extrair todas as strings em uma única lista
todas_as_strings = bairros['nome'].tolist()

# Remover as aspas de cada string na lista
todas_as_strings = [evento.strip("'") for evento in todas_as_strings]

# Juntar todas as strings em uma única string, separadas por vírgula
bairros_resultante = ', '.join(todas_as_strings)

st.write(f"Bairros com mais chamados abertos neste dia: {bairros_resultante}")
