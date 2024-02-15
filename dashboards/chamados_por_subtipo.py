import streamlit as st
import datetime


def get_subtypes(data):
    return data.subtipo.value_counts().index.tolist()


def dashboard(calls):
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
                "Selecione o subtipo de chamado",
                subtypes,
                index=subtypes.index("Perturbação do sossego"),
                help="Selecione o subtipo de chamado para análise",
            )

    with error_col:
        try:
            start_date, end_date = dates
        except ValueError:
            st.write("")
            st.error("Você deve selecionar um período de análise com duas datas")
            st.stop()


# Subtipo de chamado: Perturbação de sossego
# Quantidade total de chamados dessa natureza
# Eventos com mais ocorrencias desse subtipo
# Quantidade de chamados desse subtipo por evento
# Evento com maior média diária de chamados desse subtipo
# Média diária de chamados desse subtipo por evento e a média geral
