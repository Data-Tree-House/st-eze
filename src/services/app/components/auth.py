import streamlit as st

from services.app.utils import google_text, primary_text


def login():
    with st.container(border=True, horizontal_alignment="center"):
        st.markdown(f"### Welcome to our {primary_text('demo app')}", text_alignment="center")

        if st.button(f"Sign in with {google_text()}"):
            st.login("google")
    st.stop()


def logout():
    if st.sidebar.button("Log out"):
        st.logout()
