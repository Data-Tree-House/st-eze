import streamlit as st

from constants import c


def top_logo():
    st.logo(
        c.logo_banner_path,
        icon_image=c.logo_circle_path,
        size="large",
        link=c.datatreehouse_url,
    )
