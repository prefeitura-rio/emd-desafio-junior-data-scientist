from typing import Callable

import pandas as pd
import pandas_gbq  # noqa: F401
import streamlit as st

from src.dashboards.analise_por_bairros import dashboard as analise_por_bairros
from src.dashboards.chamados_em_um_dia import dashboard as chamados_em_um_dia
from src.dashboards.chamados_por_subtipo import (
    dashboard as chamados_por_subtipo,
)
from src.mypages.homepage import page as homepage
from src.mypages.queries_python_page import page as queries_python_page
from src.mypages.queries_sql_page import page as queries_sql_page


@st.cache_data
def load_call_data() -> pd.DataFrame:
    """Carrega os dados dos chamados."""
    return pd.read_parquet(
        "data/chamado_1746.parquet",
        columns=[
            "id_chamado",
            "data_inicio",
            "data_fim",
            "tipo",
            "subtipo",
            "id_bairro",
            "dentro_prazo",
            "situacao",
            "tipo_situacao",
            "status",
        ],
    )


@st.cache_data
def load_neighborhood_data() -> pd.DataFrame:
    """Carrega os dados dos bairros."""
    return pd.read_parquet(
        "data/bairro.parquet",
        columns=["id_bairro", "nome", "subprefeitura", "geometry"],
    )


@st.cache_data
def load_event_data() -> pd.DataFrame:
    """Carrega os dados dos eventos."""
    return pd.read_parquet("data/rede_hoteleira_ocupacao_eventos.parquet")


def create_button(
    text: str,
    name: str,
    current_page: str,
    change_page_func: Callable[[str], None],
) -> st.sidebar.button:
    """Cria um botão na sidebar.

    Args:
        text (str): Texto do botão.
        name (str): Nome da página associada ao botão.
        current_page (str): Página atual.
        change_page_func (Callable[[str], None]): Função para alterar a página.

    Returns:
        st.sidebar.button: Botão criado.
    """
    return st.sidebar.button(
        text,
        use_container_width=True,
        on_click=change_page_func,
        args=(name,),
        type="primary" if current_page == name else "secondary",
    )


def change_page(name: str) -> None:
    """Altera a página atual."""
    st.session_state["page"] = name


def main():
    # Configurações da página
    st.set_page_config(
        page_title="Chamados ao 1746 Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
    )

    # Carregamento dos dados
    calls = load_call_data()
    neighborhoods = load_neighborhood_data()
    events = load_event_data()

    # Adicionando estilos CSS
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar com logo e título
    st.sidebar.markdown(
        """
        <a href="https://www.1746.rio/hc/pt-br" target="_blank">
            <img src="app/static/logo-1746.png" class="sidebar_logo">
        </a>
        <h1 class="sidebar_title"> Análise de Chamados - <span class="highlighted">Dashboard</span></h1>
        <p class="sidebar_subtitle">Análise de chamados abertos nos anos de 2022 e 2023</p>
        """,
        unsafe_allow_html=True,
    )

    # Mapeamento de páginas disponíveis
    pages = {
        "home": homepage,
        "dashboard_1": lambda: chamados_em_um_dia(calls, neighborhoods),
        "dashboard_2": lambda: chamados_por_subtipo(calls, events),
        "analise_por_bairros": lambda: analise_por_bairros(
            calls, neighborhoods
        ),
        "queries_sql": queries_sql_page,
        "queries_python": queries_python_page,
    }

    # Inicialização da página atual
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Criação dos botões da sidebar
    current_page = st.session_state["page"]
    create_button("🏠 Página Inicial", "home", current_page, change_page)
    st.sidebar.markdown("### 📊 Dashboards")
    create_button(
        "🗓️ Chamados em um dia", "dashboard_1", current_page, change_page
    )
    create_button(
        "🔊 Chamados por subtipo", "dashboard_2", current_page, change_page
    )
    create_button(
        "🏘️ Análise por bairros",
        "analise_por_bairros",
        current_page,
        change_page,
    )
    st.sidebar.markdown("### 💡 Solução do desafio")
    create_button(
        "💾 Consultas em SQL", "queries_sql", current_page, change_page
    )
    create_button(
        "🐍 Consultas em Python", "queries_python", current_page, change_page
    )

    # Renderização da página atual
    pages[current_page]()


if __name__ == "__main__":
    main()
