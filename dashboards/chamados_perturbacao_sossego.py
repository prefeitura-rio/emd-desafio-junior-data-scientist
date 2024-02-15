import streamlit as st


def dashboard():
    st.markdown(
        """
        <h1 class="main_title dashboard_title"> Chamados de Perturbação de Sossego</h1>
        <p class="main_subtitle">Análise de chamados de perturbação de sossego</p>
        """,
        unsafe_allow_html=True,
    )
