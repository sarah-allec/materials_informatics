from menu import unauthenticated_menu
import streamlit as st

st.set_page_config(
    page_title="Physics-Informed Learning",
    page_icon="⚛️",
    layout="wide",
)

st.write("# Physics-Informed Learning ⚛️")

unauthenticated_menu()
