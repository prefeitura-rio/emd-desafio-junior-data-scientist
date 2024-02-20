import streamlit as st


def page():
    with open("analise_sql.md", "r") as file:
        st.markdown(file.read())
