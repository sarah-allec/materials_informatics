import streamlit as st

def custom_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Materials_Informatics.py", label="Home 🏠")
    st.sidebar.page_link("pages/Transfer_Learning.py", label="Transfer Learning 🤝")
    st.sidebar.page_link("pages/Active_Learning.py", label="Active Learning 🏃🏽‍♀️")
    st.sidebar.page_link("pages/Physics_Informed_Learning.py", label="Physics-Informed Learning ⚛️")
