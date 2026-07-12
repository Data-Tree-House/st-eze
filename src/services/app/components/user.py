import streamlit as st

from constants import c


def profile():
    with st.sidebar:
        try:
            profile_picture = st.user.picture or c.default_picture
        except Exception:
            profile_picture = c.default_picture

        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.image(
                f"{profile_picture}",
                width="content",
            )
        with col2:
            st.markdown(f"{st.user.name}")
            st.markdown(f"{st.user.email}")
