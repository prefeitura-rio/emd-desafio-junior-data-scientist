import streamlit as st
import datetime
import plotly.express as px
from src.plots import plot_calls_ts, plot_calls_during_events


def get_event(date, events):
    event = events.loc[
        (date >= events["data_inicial"]) & (date <= events["data_final"]), "evento"
    ]
    return event.item() if event.shape[0] > 0 else None


def get_subtypes(data):
    return data.subtipo.value_counts().index.tolist()


def get_avg_calls(data, event: list = None):
    return data["data_inicio"].dt.date.value_counts().mean()


@st.cache_data
def get_calls_with_event(data, events):
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


def dashboard(calls, events):
    st.markdown(
        """
        <header class="dashboard_header">
            <h1 class="dashboard_title"> Análise de Chamados - <span class="highlighted">
            Dashboard</span>
            </h1>
            <p class="dashboard_subtitle">Análise de chamados para um subtipo específico no período de 2022 a 2023</p>
            <a href="https://www.1746.rio/hc/pt-br" target="_blank">
                <img src="app/static/logo.jpeg" class="dashboard_logo">
            </a>
        </header>
        """,
        unsafe_allow_html=True,
    )

    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.date(2023, 12, 31)

    error_col, filter_col = st.columns([2, 1])

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
            st.error("Você deve selecionar um período de análise com duas datas")
            st.stop()

    calls = calls.loc[
        (calls.data_inicio.dt.date >= min_date)
        & (calls.data_inicio.dt.date <= max_date)
    ]
    filtered_calls = calls[calls.subtipo == subtype]
    calls_during_events = get_calls_with_event(filtered_calls, events)

    (
        subtype_col,
        calls_qty_cot,
        event_max_avg_col,
        avg_calls_col,
        avg_calls_during_event_col,
    ) = st.columns(5)

    with subtype_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title"
                title="{subtype}"
                >{subtype}</h2>
                <p class="card_value">Subtipo selecionado</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with calls_qty_cot:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title">{filtered_calls.shape[0]}</h2>
                <p class="card_value
                ">Chamados abertos desse subtipo</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with event_max_avg_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title
                ">Rock in Rio</h2>
                <p class="card_value
                ">Evento com mais chamados</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with avg_calls_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title
                ">{get_avg_calls(filtered_calls):.2f}</h2>
                <p class="card_value
                ">Média diária durante todo o período</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with avg_calls_during_event_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title
                ">{calls_during_events.dropna(subset=["durante_evento"])["data_inicio"].dt.date.value_counts().mean():.2f}</h2>
                <p class="card_value
                ">Média diária durante eventos</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
    with table_col:
        st.dataframe(calls_during_events)

    with bar_chart_col:
        calls_during_events = (
            calls_during_events["durante_evento"].value_counts().reset_index()
        )
        calls_during_events.columns = ["evento", "chamados"]
        st.plotly_chart(
            plot_calls_during_events(
                calls_during_events.sort_values("chamados", ascending=True)
            ),
            use_container_width=True,
            theme="streamlit",
            config={"displayModeBar": False},
        )
