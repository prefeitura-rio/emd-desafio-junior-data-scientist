import streamlit as st


def display_card(
    card_value: str, card_description: str, tooltip: str = ""
) -> None:
    """Exibe um card com um título e um valor.

    Args:
        card_value (str): Valor do card.
        card_description ([type]): Descrição do card.
        tooltip (str): Texto de ajuda.
    """
    st.markdown(
        f"""
        <div class="card">
            <h2 class="card_title" title="{tooltip}">{card_value}</h2>
            <p>{card_description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_grid(cols: int = 1, rows: int = 1) -> list:
    """Cria um grid de colunas e linhas.

    Args:
        cols (int): Número de colunas.
        rows (int): Número de linhas.

    Returns:
        list: Grid de colunas e linhas.
    """
    grid = [0] * rows
    for i in range(rows):
        grid[i] = st.columns(cols)
    return grid


def display_dashboard_header(title: str, description: str) -> None:
    """Exibe o cabeçalho do dashboard com título, descrição.

    Args:
        title (str): Título do dashboard.
        description (str): descrição do dashboard.
    """
    st.markdown(
        f"""
        <header class="dashboard_header">
            <h1 class="dashboard_title">{title}</h1>
            <p class="dashboard_subtitle">{description}</p>
            <a href="https://www.1746.rio/hc/pt-br" target="_blank">
                <img src="app/static/logo.jpeg" class="dashboard_logo">
            </a>
        </header>
        """,
        unsafe_allow_html=True,
    )
