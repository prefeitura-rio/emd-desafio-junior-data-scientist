import streamlit as st


def page():
    with open("analise_python.md", "r") as file:
        st.markdown(file.read(), unsafe_allow_html=True)
