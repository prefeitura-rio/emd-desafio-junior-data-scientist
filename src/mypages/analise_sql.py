import streamlit as st


def page():
    with open("desafio/analise_sql.md", "r") as file:
        st.markdown(file.read())
