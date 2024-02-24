import streamlit as st


def page():
    with open("desafio/analise_python.md", "r") as file:
        markdown = file.read()
        markdown = markdown.replace("analise_python_files/", "app/static/")
    st.markdown(markdown, unsafe_allow_html=True)
