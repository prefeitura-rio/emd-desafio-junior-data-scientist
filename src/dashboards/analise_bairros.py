import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from src.plots import plot_bar_chart


def create_days_of_week(data):
    return data.assign(
        dia_da_semana=pd.Categorical(
            data["data_inicio"]
            .dt.day_name()
            .map(
                {
                    "Sunday": "Domingo",
                    "Monday": "Segunda",
                    "Tuesday": "Terça",
                    "Wednesday": "Quarta",
                    "Thursday": "Quinta",
                    "Friday": "Sexta",
                    "Saturday": "Sábado",
                }
            ),
            categories=[
                "Domingo",
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
            ],
            ordered=True,
        )
    )


@st.cache_data
def neighborhood_calls(calls, neighborhoods):
    return create_days_of_week(calls.merge(neighborhoods, on="id_bairro"))


def format_number(number: str):
    return number.replace(".", "|").replace(",", ".").replace("|", ",")


def metrics(calls):
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total de Chamados", format_number(f"{calls.shape[0]:,d}")
            )
        with col2:
            calls_on_time = calls["dentro_prazo"].value_counts()
            calls_on_time = calls_on_time.get("No prazo", 0)
            st.metric(
                "Chamados no prazo", format_number(f"{calls_on_time:,d}")
            )
        with col3:
            avg_days = (
                calls["data_fim"]
                .sub(calls["data_inicio"])
                .mean(skipna=True)
                .days
            )
            if avg_days != avg_days:
                st.metric("Tempo médio de atendimento", "N/A")
            else:
                st.metric(
                    "Tempo médio de atendimento",
                    format_number(f"{avg_days:.1f} dias"),
                )
        with col4:
            current_calls = calls["situacao"].value_counts(normalize=True)
            current_calls = current_calls.get("Encerrado", 0)
            st.metric(
                "Chamados encerrados", format_number(f"{current_calls:.1%}")
            )


def filters(data):
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            subprefecture_option = st.multiselect(
                "Subprefeitura", data["subprefeitura"].unique()
            )
            if subprefecture_option:
                data = data[data["subprefeitura"].isin(subprefecture_option)]
        with col2:
            neighborhoods_option = st.multiselect(
                "Bairro", data["nome"].unique()
            )
            if neighborhoods_option:
                data = data[data["nome"].isin(neighborhoods_option)]
        with col3:
            situation_option = st.multiselect(
                "Tipo Situação", data["tipo_situacao"].unique()
            )
            if situation_option:
                data = data[data["tipo_situacao"].isin(situation_option)]
        with col4:
            col5, col6 = st.columns([1, 1])
            with col5:
                dt_start = st.date_input(
                    "Início do Período",
                    value=datetime.date(2022, 1, 1),
                    min_value=datetime.date(2022, 1, 1),
                    max_value=datetime.date(2023, 12, 31),
                )
            with col6:
                dt_end = st.date_input(
                    "Fim do Período",
                    value=datetime.date(2023, 12, 31),
                    min_value=datetime.date(2022, 1, 1),
                    max_value=datetime.date(2023, 12, 31),
                )

                if dt_start > dt_end:
                    st.error(
                        "A data de início do período deve ser anterior à data de fim."
                    )
                else:
                    data = data[
                        (
                            (data["data_inicio"].dt.date >= dt_start)
                            & (data["data_inicio"].dt.date <= dt_end)
                        )
                        | (
                            (
                                data["data_fim"]
                                .fillna(datetime.datetime.now())
                                .dt.date
                                >= dt_start
                            )
                            & (
                                data["data_fim"]
                                .fillna(datetime.datetime.now())
                                .dt.date
                                <= dt_end
                            )
                        )
                    ]

    return data


def dashboard(calls, neighborhoods):
    st.title("Análise por Bairros")
    st.write(
        """
        Nesta seção, você pode analisar os chamados por bairros.
        """
    )

    data = neighborhood_calls(calls, neighborhoods)
    data = filters(data)

    metrics(data)
    st.write("\n\n")

    with st.container():
        col1, col2, col3 = st.columns([0.2, 0.45, 0.35])
        with col1:
            fig = px.pie(
                data["dentro_prazo"].value_counts().reset_index(),
                names="dentro_prazo",
                values="count",
                title="Chamados dentro do prazo",
                hole=0.6,
            )

            fig.update_traces(
                marker=dict(colors=["#004A80", "#ECECEC"]),
                textfont=dict(size=16),
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            fig.update_layout(title_font_size=20)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.plotly_chart(
                plot_bar_chart(
                    data["status"]
                    .value_counts()
                    .reset_index()
                    .sort_values("count"),
                    "count",
                    "status",
                    title="Número de chamados por status",
                    title_font_size=20,
                ),
                config={"displayModeBar": False},
                use_container_width=True,
            )

        with col3:
            fig = px.bar(
                data["dia_da_semana"]
                .value_counts()
                .reset_index()
                .sort_values("dia_da_semana"),
                x="dia_da_semana",
                y="count",
                title="Chamados por dia da semana",
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                title_font_size=20,
            )

            fig.update_traces(marker_color="#004A80", width=0.6)
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.plotly_chart(
                plot_bar_chart(
                    data["tipo"]
                    .value_counts()
                    .head(10)
                    .reset_index()
                    .sort_values("count"),
                    "count",
                    "tipo",
                    title="Top 10 tipos de chamados",
                    title_font_size=20,
                    height=420,
                ),
                config={"displayModeBar": False},
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                plot_bar_chart(
                    data["subtipo"]
                    .value_counts()
                    .head(10)
                    .reset_index()
                    .sort_values("count"),
                    "count",
                    "subtipo",
                    title="Top 10 subtipos de chamados",
                    title_font_size=20,
                    height=420,
                ),
                config={"displayModeBar": False},
                use_container_width=True,
            )
