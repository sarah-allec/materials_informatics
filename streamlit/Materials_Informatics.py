from menu import unauthenticated_menu
import streamlit as st
from st_pages import Page, show_pages, add_page_title

#show_pages(
#    [
#        Page("Materials_Informatics.py", "Materials Informatics", "🏠"),
#        Page("pages/Transfer_Learning.py", "Transfer Learning", "🤝")
#    ]
#)
#
#add_page_title(layout="wide")

st.write("# Materials Informatics Portfolio")

st.write("Welcome! 👋🏼 This web app serves as my materials informatics portfolio. To navigate to a given topic, see the menu on the left of this page. To see a Jupyter notebook version containing the technical details of each topic application, visit the corresponding GitHub repo here. Enjoy!")

unauthenticated_menu()
