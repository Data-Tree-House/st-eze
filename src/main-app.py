import streamlit as st
from loguru import logger

import core.utils as utils
from constants import c
from services.app import components as comp

# TODO: add sigterm handlers

# =============== // INITIALIZE APPLICATION // ===============

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon=c.favicon,
)
utils.load_umami()

if "init" not in st.session_state:
    logger.info("Initializing new session session")
    st.session_state.init = True


# =============== // REDIRECT TO AUTH // ===============

if not st.user.is_logged_in:
    logger.info("A visitor!")
    comp.login()
else:
    logger.info(f"User {st.user.name} ({st.user.sub}), {st.user.email}, just logged in")

# =============== // PAGE NAVIGATION // ===============

pages = {
    "": [
        st.Page(
            f"{c.pages_path}/home.py",
            title="Home",
            icon=":material/home:",
        ),
    ],
    "Category": [
        st.Page(
            f"{c.pages_path}/about.py",
            title="About",
            icon=":material/info:",
        ),
    ],
}
page = st.navigation(pages)
page.run()

# =============== // SIDEBAR AND LOGOUT // ===============

comp.top_logo()
comp.profile()
if st.user.is_logged_in:
    comp.logout()
comp.buy_us_a_coffee()
