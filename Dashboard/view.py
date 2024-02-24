import funcoes
import querys
import streamlit as st
import plotly.express as px
import pandas as pd


st.title("Escritório de dados do Rio de Janeiro - Dashboard Datario")

st.header("Parte 1 - Análise dos bairros do Rio de Janeiro")

quantity_neighboors = funcoes.executar_consulta(querys.quantidade_bairros)
quantity_neighboors = funcoes.extrair_substring_array(quantity_neighboors, "quantidade")
st.write(f"☝️ Atualmente, a cidade do Rio de Janeiro possui {quantity_neighboors} bairros, mais do que São Gonçalo [com 91 bairros oficiais], Itaguaí [41] e Saquarema [14] juntos - que são cidades vizinhas.")


st.subheader("Análise Visual")
st.write(f"Gráfico dos 5 maiores bairros do Rio. ")

# GRÁFICO 1 - barras: 5 maiores bairros

area_query = funcoes.executar_consulta(querys.maiores_bairros)
area_bairros = pd.DataFrame(area_query, columns=["nome", "area"])
st.bar_chart(area_bairros.set_index('nome'))

# GRÁFICO 2 - pizza: maior cidade em relação à área total

areatotal = 1200000000
area_maior = float(area_bairros.iloc[0][1])

porcentagem = (area_maior / areatotal) * 100

nome_bairro = str(area_bairros.iloc[0][0])

# Criar um DataFrame para plotagem
dados = {'Área': [f'{nome_bairro}', 'Rio de Janeiro'],
         'Porcentagem': [porcentagem, 100 - porcentagem]}
comparacao_areas = pd.DataFrame(data=dados)

# Gráfico de pizza usando Plotly Express
custom_layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",  # cor para fundo do gráfico
        "plot_bgcolor": "rgba(0,0,0,0)",   # cor para o fundo do plot
        "font": {"color": "#2a3f5f"},      # cor do texto
        "colorway": ['#1f77b4', '#aec7e8', '#7f7f7f', '#98df8a', '#2ca02c', '#d62728', '#ff7f0e', '#ffbb78', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']  # Tons de azul
}
fig = px.pie(comparacao_areas, values='Porcentagem', names='Área', title=f'Porcentagem da área o bairro de {nome_bairro} em relação à Área Total da cidade. Muita coisa, né?')
fig.update_layout(custom_layout)  # Aplica o layout personalizado
st.plotly_chart(fig)

# GRÁFICO 3 - prefeituras mais atuantes
st.write("Cada bairro tem a sua subprefeitura, como acontece nas demais cidades do Brasil. No caso do Rio, algumas se repetem bastante, conforme mostrado no gráfico a seguir.")

subpre_dados = funcoes.executar_consulta(querys.subprefeituras_mais_repetem)
subprefeituras = pd.DataFrame(subpre_dados, columns=["subprefeitura", "Recorrencia"])
st.bar_chart(subprefeituras.set_index('subprefeitura'))


st.header("Parte 2 - Análise dos chamados efetuados no Rio de Janeiro")

# GRÁFICO 4 - 1o tipo de chamado mais recorrente

dado_chamado_mais_recorrente = funcoes.executar_consulta(querys.tipo_chamado_mais_recorrente)
tipo_chamado_mais_recorrente = funcoes.extrair_substring_array(dado_chamado_mais_recorrente, "tipo")
quantidade_chamado_mais_recorrente = funcoes.extrair_substring_array(dado_chamado_mais_recorrente, "total_ocorrencias")

st.write(f"☝️ Abrindo a seção dos chamados, o tipo mais recorrente em termos de solicitação foi [{tipo_chamado_mais_recorrente}], com [{quantidade_chamado_mais_recorrente}] chamados!")


# GRÁFICO 4 - gráfico por tipo de chamado mais recorrente usando latitude e longitude

st.write("Nesse gráfico, está disposto um mapa com as localizações com uma amostra de 1000 chamados da tabela consultada. Será que podemos extrair algum padrão daqui? Percebe que eles tendem a aparecer mais em algumas localidades do gráfico?")
# Consulta SQL para obter os 100 primeiros chamados com linhas válidas
dados_chamados = funcoes.executar_consulta(querys.local_1000_chamados)

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
quant_chamados_dia_mais_chamados = funcoes.executar_consulta(querys.dia_mais_chamados)
quant_chamados_dia_mais_chamados = quant_chamados_dia_mais_chamados.iloc[0]['total_chamados']

quant_total_chamados = funcoes.executar_consulta(querys.quantidade_total_chamados)
quant_total_chamados = quant_total_chamados.iloc[0]['total_chamados']

# Calcular a porcentagem de chamados em relação ao dia com mais chamados
porcentagem_dia_mais_chamados = (quant_chamados_dia_mais_chamados / quant_total_chamados) * 100

# Exibir o valor absoluto e a porcentagem
st.write(f"☝️ No dia com mais chamados, foram registrados {quant_chamados_dia_mais_chamados} chamados, o que representa apenas {porcentagem_dia_mais_chamados:.2f}% do total de chamados.")

#  GRÁFICO 5 - analise dos chamados por status

# Lista de status desejados

dados_chamados_por_status = funcoes.executar_consulta(querys.consulta_chamados_por_status)
if isinstance(dados_chamados_por_status, pd.DataFrame) and not dados_chamados_por_status.empty:
    

    # gráfico de pizza
    st.write(" > Distribuição dos chamados por status:")
    fig = px.pie(dados_chamados_por_status, values='total_chamados', names='status', title='Distribuição dos chamados por status')
    fig.update_layout(custom_layout)  # Aplica o layout personalizado
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Não há dados de chamados disponíveis para plotar.")


# INFO - tempo médio de resolução dos casos

resultado_tempo_medio_resolucao = funcoes.executar_consulta(querys.consulta_tempo_medio_resolucao)
if isinstance(resultado_tempo_medio_resolucao, pd.DataFrame) and not resultado_tempo_medio_resolucao.empty:
    # tempo_medio_resolucao = resultado_tempo_medio_resolucao.iloc[0]['tempo_medio_resolucao']
    tempo_medio_resolucao = funcoes.extrair_substring_array(resultado_tempo_medio_resolucao, "tempo_medio_resolucao")
    st.write(f" > Vale ressaltar que o tempo médio de resolução dos chamados é de aproximadamente {round(float(tempo_medio_resolucao))} dias.")
else:
    st.warning("Não há dados de tempo de prazo disponíveis para calcular o tempo médio de resolução dos chamados.")


# GRÁFICO 5 - chamados por trimestre

# Executar a consulta
resultados = funcoes.executar_consulta(querys.trimestres_query)
custom_colors = ['#1f77b4', '#aec7e8', '#7f7f7f', '#98df8a', '#2ca02c']

# gráfico com Plotly Express
fig = px.bar(resultados, x='trimestre', y='total_chamados', color='ano', barmode='group', 
             title='Distribuição dos Chamados ao Longo do Tempo por Trimestre/Ano', color_discrete_sequence=custom_colors)

# Exibir o gráfico
st.plotly_chart(fig)


st.header("Parte 3 - Análise pela perspectiva dos eventos do Rio de Janeiro")

eventos = funcoes.executar_consulta(querys.eventos_query)
eventos = funcoes.extrair_substring_array(eventos, "evento")
st.write(f"Os maiores eventos realizados são: {eventos}.")


# GRÁFICO 6 - média das taxas por evento

dados_eventos = funcoes.executar_consulta(querys.media_taxa)
fig = px.bar(dados_eventos, x='evento', y='media_taxa_ocupacao', 
             title='Média da Taxa de Ocupação por Evento',
             labels={'media_taxa_ocupacao': 'Taxa de Ocupação Média (%)'})

# Personalizar layout
fig.update_layout(xaxis_title='Evento', yaxis_title='Taxa de Ocupação Média (%)')

# Exibir o gráfico
st.plotly_chart(fig)

# GRÁFICO 7 - média de chamados por evento

dados_eventos_chamados_sql = funcoes.executar_consulta(querys.consulta_chamado_por_evento)
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

total_chamados_na_data = funcoes.executar_consulta(querys.total_chamados_na_data)
chamados_mais_recorrentes = funcoes.executar_consulta(querys.chamados_mais_recorrentes)

if isinstance(total_chamados_na_data, pd.DataFrame) and isinstance(chamados_mais_recorrentes, pd.DataFrame) and not chamados_mais_recorrentes.empty:
    # Exibir o tipo de chamado com mais ocorrências
    st.write(f"O tipo de chamado que mais foi aberto nesta data foi: {chamados_mais_recorrentes.iloc[0]['tipo']} com {chamados_mais_recorrentes.iloc[0]['total_ocorrencias']} chamados do total de {total_chamados_na_data.iloc[0]['total_chamados_abertos']}.")

    # Calcular a porcentagem do tipo específico em relação ao total de chamados
    porcentagem_tipo_especifico = (chamados_mais_recorrentes.iloc[0]['total_ocorrencias'] / total_chamados_na_data.iloc[0]['total_chamados_abertos']) * 100

    dados = {'Categoria': [f"{chamados_mais_recorrentes.iloc[0][0]}", 'Outros Tipos'],
             'Total de Chamados': [chamados_mais_recorrentes.iloc[0]['total_ocorrencias'], total_chamados_na_data.iloc[0]['total_chamados_abertos'] - chamados_mais_recorrentes.iloc[0]['total_ocorrencias']]}
    df = pd.DataFrame(data=dados)

    st.write("Distribuição dos chamados por tipo:")
    fig = px.pie(df, values='Total de Chamados', names='Categoria', title=f'Distribuição dos chamados por tipo específico ({porcentagem_tipo_especifico:.2f}%)')
    fig.update_traces(marker=dict(colors=['#1f77b4', '#aec7e8']))  # Tons de azul
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Não há dados disponíveis para a data especificada.")



# INFO - bairros com mais chamados abertos nesse dia

bairros = funcoes.executar_consulta(querys.localizacao_3_ocorrencia_chamado)
# Extrair todas as strings em uma única lista
bairros = funcoes.extrair_substring_array(bairros, "nome")
st.write(f"Bairros com mais chamados abertos neste dia: {bairros}")