from menu import unauthenticated_menu
import streamlit as st

st.set_page_config(
    page_title="Materials Informatics",
    page_icon="👾",
    layout="wide",
)

st.write("# Materials Informatics Portfolio")

st.write("Welcome! 👋🏼 This web app serves as my materials informatics portfolio. To navigate to a given topic, see the menu on the left of this page. To see a Jupyter notebook version containing the technical details of each topic application, visit the corresponding GitHub repo here. Enjoy!")

unauthenticated_menu()
