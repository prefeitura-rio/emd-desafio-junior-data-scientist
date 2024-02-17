import streamlit as st


def page():
    with open("perguntas_desafio.md", "r") as file:
        st.markdown(file.read())
