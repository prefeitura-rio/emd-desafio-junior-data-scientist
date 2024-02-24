import datetime
from typing import Any

import pandas as pd
import streamlit as st

from src.plots import make_choropleth
from src.plots import plot_bar_chart
from src.utils import display_card
from src.utils import display_dashboard_header
from src.utils import make_grid


def filter_data(data: pd.DataFrame, dt: datetime.date) -> pd.DataFrame:
    """Filtra os dados para a data selecionada.

    Args:
        data (pd.DataFrame): Dados dos chamados.
        dt (datetime.date): Data selecionada.

    Returns:
        pd.DataFrame: Dados filtrados.
    """
    return data[data["data_inicio"].dt.date == dt]


def get_calls_by_neighborhood(
    data: pd.DataFrame, neighborhoods: pd.DataFrame
) -> pd.DataFrame:
    """Obtém os chamados por bairro.

    Args:
        data (pd.DataFrame): Dados dos chamados.
        neighborhoods (Any): Dados dos bairros.

    Returns:
        pd.DataFrame: Chamados por bairro.
    """
    return data.merge(neighborhoods, on="id_bairro")


def display_cards(
    filtered_data: Any,
    calls_by_neighborhood: Any,
    selected_date: datetime.date,
) -> None:
    """Exibe os cards com informações dos chamados.

    Args:
        filtered_data (Any): Dados filtrados dos chamados.
        calls_by_neighborhood (Any): Chamados por bairro.
        selected_date (datetime.date): Data selecionada.
    """
    grid = make_grid(rows=1, cols=4)
    most_common_type = filtered_data["tipo"].value_counts().idxmax()
    cards_data = [
        ("Quantidade de chamados", filtered_data.shape[0], ""),
        ("Tipo mais comum", most_common_type, most_common_type),
        (
            "Subprefeitura comum",
            calls_by_neighborhood.subprefeitura.value_counts().idxmax(),
            "",
        ),
        ("Data que foi selecionada", selected_date.strftime("%d/%m/%Y"), ""),
    ]

    for i, (description, value, tooltip) in enumerate(cards_data):
        with grid[0][i]:
            display_card(value, description, tooltip)


def display_plots(
    filtered_data: pd.DataFrame,
    calls_by_neighborhood: pd.DataFrame,
    neighborhoods: pd.DataFrame,
) -> None:
    """Exibe os plots com informações dos chamados.

    Args:
        filtered_data (pd.DataFrame): Dados filtrados dos chamados.
        calls_by_neighborhood (pd.DataFrame): Chamados por bairro.
        neighborhoods (pd.DataFrame): Dados dos bairros.
    """
    st.markdown(
        """
        <h2 class="section_title">Mapa de Chamados</h2>
        <p class="section_subtitle">Distribuição de chamados por bairro</p>
        """,
        unsafe_allow_html=True,
    )

    grid = make_grid(rows=1, cols=2)

    with grid[0][0]:
        st.plotly_chart(
            make_choropleth(filtered_data, neighborhoods),
            use_container_width=True,
        )

    with grid[0][1]:
        top_10 = (
            calls_by_neighborhood["nome"]
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )
        st.plotly_chart(
            plot_bar_chart(
                top_10,
                "count",
                "nome",
                height=350,
                margin=dict(l=0, r=0, b=0, t=0),
            ),
            config={"displayModeBar": False},
            use_container_width=True,
        )


def display_calls_without_neighborhood(filtered_data: pd.DataFrame) -> None:
    """Exibe os chamados sem bairro associado.

    Args:
        filtered_data (pd.DataFrame): Dados filtrados dos chamados.
    """
    st.markdown(
        """
        <h2 class="section_title">Chamados sem bairro associado</h2>
        <p class="section_subtitle">Tipos e subtipos de chamados sem bairro associado</p>
        """,
        unsafe_allow_html=True,
    )

    calls_without_neighborhood = filtered_data[
        filtered_data["id_bairro"].isna()
    ]
    st.dataframe(
        calls_without_neighborhood[["id_chamado", "tipo", "subtipo"]]
        .groupby(["tipo", "subtipo"])
        .size()
        .reset_index(name="quantidade")
        .sort_values("quantidade", ascending=False),
        use_container_width=True,
        height=150,
        hide_index=True,
    )


def dashboard(data: pd.DataFrame, neighborhoods: pd.DataFrame) -> None:
    """Cria o dashboard com as análises dos chamados.

    Args:
        data (pd.DataFrame): Dados dos chamados.
        neighborhoods (pd.DataFrame): Dados dos bairros.
    """
    display_dashboard_header(
        "Análise de Chamados - Dashboard",
        "Análise de chamados abertos em um dado dia",
    )

    dt = st.date_input(
        "Selecione a data",
        value=datetime.date(2023, 4, 1),
        min_value=datetime.date(2022, 1, 1),
        max_value=datetime.date(2023, 12, 31),
    )

    filtered_data = filter_data(data, dt)
    calls_by_neighborhood = get_calls_by_neighborhood(
        filtered_data, neighborhoods
    )

    with st.container():
        display_cards(filtered_data, calls_by_neighborhood, dt)

    with st.container():
        display_plots(filtered_data, calls_by_neighborhood, neighborhoods)

    with st.container():
        display_calls_without_neighborhood(filtered_data)
