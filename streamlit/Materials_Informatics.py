from menu import unauthenticated_menu
import streamlit as st

st.set_page_config(
    page_title="Materials Informatics",
    page_icon="✨",
    layout="wide",
)

st.write("# Materials Informatics Portfolio")
st.write("## Welcome! 👋🏼")
st.write("This page serves as my materials informatics portfolio. To navigate to a given topic, see the menu on the left of this page. To see a Jupyter notebook version containing the technical details of each topic application, visit the corresponding GitHub <a href='https://github.com/sarah-allec/materials_informatics' target='_blank'>repo</a>. Enjoy!", unsafe_allow_html=True)

unauthenticated_menu()
