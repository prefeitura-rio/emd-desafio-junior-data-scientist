import streamlit as st
import pandas as pd
import basedosdados as bd
from dashboards.chamados_em_um_dia import dashboard as chamados_em_um_dia
from dashboards.chamados_por_subtipo import (
    dashboard as chamados_por_subtipo,
)


@st.cache_data
def load_call_data():
    return pd.read_parquet(
        "data/chamado_1746.parquet",
        columns=[
            "id_chamado",
            "data_inicio",
            "tipo",
            "subtipo",
            "id_bairro",
        ],
    )


@st.cache_data
def load_neighborhoods():
    return pd.read_parquet(
        "data/bairro.parquet",
        columns=["id_bairro", "nome", "subprefeitura", "geometry"],
    )


st.set_page_config(
    page_title="Chamados ao 1746 Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

calls = load_call_data()
neighborhoods = load_neighborhoods()

page_names_to_display = {
    "🛎️ Chamados em um dia": lambda: chamados_em_um_dia(calls, neighborhoods),
    "🔊 Chamados por subtipo": lambda: chamados_por_subtipo(calls),
}

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <h1 class="sidebar_title"> Análise de Chamados - <span class="highlighted">Dashboard</span></h1>
    <p class="sidebar_subtitle">Análise de chamados abertos nos anos de 2022 e 2023</p>
    """,
    unsafe_allow_html=True,
)
page_name = st.sidebar.radio(
    "Escolha um dashboard:", list(page_names_to_display.keys())
)
page_names_to_display[page_name]()
