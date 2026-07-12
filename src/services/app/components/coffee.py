import streamlit as st

from constants import c


def buy_us_a_coffee():
    with st.sidebar:
        st.divider()
        st.markdown(
            f"[![buy-us-a-coffee](./app/{c.buy_us_a_coffee_path})]({c.snapscan_url})",
            width=350,
        )
