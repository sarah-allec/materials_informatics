from menu import unauthenticated_menu
import streamlit as st
import base64

st.set_page_config(
    page_title="Materials Informatics",
    page_icon="✨",
    #layout="wide",
)

st.write("# Materials Informatics Portfolio")
st.write("## Welcome! 👋🏼")
st.write("This page serves as my materials informatics portfolio. To navigate to a given topic, see the menu on the left of this page. To see a Jupyter notebook version containing the technical details of each topic application, visit the corresponding GitHub <a href='https://github.com/sarah-allec/materials_informatics' target='_blank'>repo</a>. Enjoy!", unsafe_allow_html=True)

st.write("#")

columns = st.columns(12)

with columns[4]:
    st.write("""<div style="width:100%;text-align:center;"><a href="https://sarah-allec.github.io/" style="float:center"><img width="32px" height="32px" src="https://img.icons8.com/nolan/64/domain.png" alt="domain"/></img></a></div>""", unsafe_allow_html=True)

with columns[5]:
    st.write("""<div style="width:100%;text-align:center;"><a href="https://www.linkedin.com/in/sarah-allec/" style="float:center"><img width="32px" height="32px" src="https://img.icons8.com/nolan/64/linkedin.png" alt="linkedin"/> </img></a></div>""", unsafe_allow_html=True)

with columns[6]:
    st.write("""<div style="width:100%;text-align:center;"><a href="https://github.com/sarah-allec" style="float:center"><img width="32px" height="32px" src="https://img.icons8.com/nolan/64/github.png" alt="github"/></a></div>""", unsafe_allow_html=True)
    
unauthenticated_menu()
