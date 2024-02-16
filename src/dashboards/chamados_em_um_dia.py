import datetime

import plotly.express as px
import streamlit as st

from src.plots import make_choropleth


def filter_data(data, dt):
    return data[data["data_inicio"].dt.date == dt]


def get_calls_by_neighborhood(data, neighborhoods):
    return data.merge(neighborhoods, on="id_bairro")


def dashboard(data, neighborhoods):
    st.markdown(
        """
        <header class="dashboard_header">
            <h1 class="dashboard_title"> Análise de Chamados - <span class="highlighted">
            Dashboard</span>
            </h1>
            <p class="dashboard_subtitle">Análise de chamados abertos em um dado dia</p>
            <a href="https://www.1746.rio/hc/pt-br" target="_blank">
                <img src="app/static/logo.jpeg" class="dashboard_logo">
            </a>
        </header>
        """,
        unsafe_allow_html=True,
    )

    dt = st.date_input(
        "Selecione a data",
        value=datetime.date(2023, 4, 1),
        min_value=datetime.date(2022, 1, 1),
        max_value=datetime.date(2023, 12, 31),
    )

    filtered_data = filter_data(data, dt)

    # -----------------# Card Section #-----------------#
    calls_amount_col, most_common_call_col, subprefecture_col, date_col = (
        st.columns((1, 1, 1, 1))
    )

    with calls_amount_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title">{filtered_data.shape[0]}</h2>
                <p class="card_value">Quantidade de chamados</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with most_common_call_col:
        most_common_call = filtered_data.tipo.value_counts().idxmax()
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title"
                title="{most_common_call}"
                >{most_common_call}</h2>
                <p class="card_value">Tipo mais comum</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with subprefecture_col:
        calls_by_neighborhood = get_calls_by_neighborhood(
            filtered_data, neighborhoods
        )
        subprefecture = (
            calls_by_neighborhood.subprefeitura.value_counts().idxmax()
        )
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title"
                >{subprefecture}</h2>
                <p class="card_value">Subprefeitura comum</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with date_col:
        st.markdown(
            f"""
            <div class="card">
                <h2 class="card_title">{dt.strftime('%d/%m/%Y')}</h2>
                <p class="card_value
                ">Data que foi selecionada</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------# Plots Section #-----------------#
    st.markdown(
        """
        <h2 class="section_title">Mapa de Chamados</h2>
        <p class="section_subtitle">Distribuição de chamados por bairro</p>
        """,
        unsafe_allow_html=True,
    )

    map_col, neighborhoods_col = st.columns((1, 1))

    with map_col:
        st.plotly_chart(
            make_choropleth(filtered_data, neighborhoods),
            use_container_width=True,
        )

    with neighborhoods_col:
        top_10 = (
            calls_by_neighborhood["nome"].value_counts().head(10).sort_values()
        )
        fig = px.bar(
            top_10,
            x=top_10.values,
            y=top_10.index,
            orientation="h",
            labels={"x": "Chamados", "y": "Bairro"},
            width=400,
            height=350,
        )

        fig.update_traces(marker_color="#004A71")

        for i, v in enumerate(top_10.values):
            fig.add_annotation(
                x=v,
                y=top_10.index[i],
                text=str(v),
                xshift=12,
                showarrow=False,
            )
        fig.update_yaxes(title_text="")
        fig.update_layout(
            xaxis_visible=False,
            xaxis_showticklabels=False,
            margin=dict(l=0, r=0, b=0, t=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )

        st.plotly_chart(
            fig, config={"displayModeBar": False}, use_container_width=True
        )

    # ------ Chamados não associados a um bairro

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
