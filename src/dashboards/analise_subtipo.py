import datetime

import pandas as pd
import streamlit as st

from src.plots import plot_bar_chart
from src.plots import plot_calls_ts
from src.utils import display_card
from src.utils import display_dashboard_header
from src.utils import make_grid


def get_event(date: datetime.date, events: pd.DataFrame) -> str | None:
    """Obtém o evento associado a uma data, se houver.

    Args:
        date (datetime.date): A data para a qual se deseja obter o evento.
        events (pd.DataFrame): O dataframe contendo os eventos e suas datas.

    Returns:
        str | None: O evento associado à data, se houver.
    """
    event = events.loc[
        (date >= events["data_inicial"]) & (date <= events["data_final"]),
        "evento",
    ]
    return event.item() if event.shape[0] > 0 else None


def get_subtypes(data: pd.DataFrame) -> list[str]:
    """Obtém a lista de subtipos presentes nos dados.

    Args:
        data (pd.DataFrame): O dataframe contendo os chamados.

    Returns:
        List[str]: A lista de subtipos presentes nos dados.
    """
    return data.subtipo.value_counts().index.tolist()


def get_avg_calls(data: pd.DataFrame) -> float:
    """Calcula a média diária de chamados.

    Args:
        data (pd.DataFrame): O dataframe contendo os chamados.

    Returns:
        float: A média diária de chamados.
    """
    if data.empty:
        return 0
    return data["data_inicio"].dt.date.value_counts().mean()


@st.cache_data
def get_calls_with_event(
    data: pd.DataFrame, events: pd.DataFrame
) -> pd.DataFrame:
    """Filtra os chamados que ocorreram durante eventos.

    Args:
        data (pd.DataFrame): O dataframe contendo os chamados.
        events (pd.DataFrame): O dataframe contendo os eventos.

    Returns:
        pd.DataFrame: O dataframe contendo os chamados que ocorreram durante eventos.
    """
    calls_during_events = data.loc[
        data["data_inicio"].dt.date.between(
            events["data_inicial"].min(), events["data_final"].max()
        ),
        ["id_chamado", "tipo", "subtipo", "data_inicio"],
    ].assign(
        durante_evento=lambda d: d["data_inicio"].dt.date.apply(
            lambda x: get_event(x, events)
        )
    )
    return calls_during_events


def display_cards(
    calls_during_events: pd.DataFrame,
    filtered_calls: pd.DataFrame,
    subtype: str,
) -> None:
    """Exibe os cartões com informações sobre os chamados.

    Args:
        calls_during_events (pd.DataFrame): O dataframe contendo os chamados durante eventos.
        filtered_calls (pd.DataFrame): O dataframe contendo os chamados filtrados por subtipo.
        subtype (str): O subtipo de chamado selecionado.
    """
    grid = make_grid(rows=1, cols=5)
    cards_data = [
        ("Subtipo selecionado", subtype, subtype),
        ("Chamados abertos desse subtipo", filtered_calls.shape[0], ""),
        (
            "Evento com mais chamados",
            (
                calls_during_events["durante_evento"].value_counts().idxmax()
                if not calls_during_events.empty
                else "Nenhum evento"
            ),
            "",
        ),
        (
            "Média diária durante todo o período",
            f"{get_avg_calls(filtered_calls):.2f}",
            "",
        ),
        (
            "Média diária durante eventos",
            f"{get_avg_calls(calls_during_events.dropna(subset=['durante_evento'])):.2f}",
            "",
        ),
    ]

    for i, (description, value, tooltip) in enumerate(cards_data):
        with grid[0][i]:
            display_card(value, description, tooltip=tooltip)


def dashboard(calls: pd.DataFrame, events: pd.DataFrame) -> None:
    """Cria o dashboard para análise de chamados.

    Args:
        calls (pd.DataFrame): O dataframe contendo os chamados.
        events (pd.DataFrame): O dataframe contendo os eventos.
    """
    display_dashboard_header(
        "Análise de Chamados - Dashboard",
        "Análise de chamados para um subtipo específico no período de 2022 a 2023",
    )

    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.date(2023, 12, 31)

    error_col, filter_col = st.columns([2, 1])

    with st.container():
        with filter_col:
            date_picker_col, subtype_col = st.columns([1, 1])

            with date_picker_col:
                dates = st.date_input(
                    "Selecione o período",
                    [min_date, max_date],
                    min_value=min_date,
                    max_value=max_date,
                    help="Selecione o período de análise",
                )

            with subtype_col:
                subtypes = get_subtypes(calls)
                subtype = st.selectbox(
                    "Selecione o subtipo",
                    subtypes,
                    index=subtypes.index("Perturbação do sossego"),
                    help="Selecione o subtipo de chamado para análise",
                )

        with error_col:
            try:
                min_date, max_date = dates
            except ValueError:
                st.write("")
                st.error(
                    "Você deve selecionar um período de análise com duas datas"
                )
                st.stop()

    calls = calls.loc[
        (calls.data_inicio.dt.date >= min_date)
        & (calls.data_inicio.dt.date <= max_date)
    ]
    filtered_calls = calls[calls.subtipo == subtype]
    calls_during_events = get_calls_with_event(filtered_calls, events)

    with st.container():
        display_cards(calls_during_events, filtered_calls, subtype)

    with st.container():
        st.markdown(
            """
            <h2 class="section_title">Série Temporal de Chamados</h2>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            plot_calls_ts(filtered_calls),
            use_container_width=True,
            theme="streamlit",
            config={"displayModeBar": False},
        )

        st.markdown(
            """
            <h2 class="section_title">Chamados Durante Eventos</h2>
            """,
            unsafe_allow_html=True,
        )

    bar_chart_col, table_col = st.columns([1, 1])

    calls_during_events = calls_during_events.dropna(subset=["durante_evento"])

    with st.container():
        if calls_during_events.empty:
            st.markdown(
                "Não há chamados registrados durante eventos no período selecionado"
            )
            return
        with table_col:
            st.dataframe(calls_during_events)

        with bar_chart_col:
            calls_during_events = (
                calls_during_events["durante_evento"]
                .value_counts()
                .reset_index()
            )
            calls_during_events.columns = ["evento", "chamados"]
            st.plotly_chart(
                plot_bar_chart(
                    calls_during_events.sort_values(
                        "chamados", ascending=True
                    ),
                    "chamados",
                    "evento",
                    height=380,
                    margin=dict(l=0, r=0, b=0, t=0),
                ),
                use_container_width=True,
                theme="streamlit",
                config={"displayModeBar": False},
            )
