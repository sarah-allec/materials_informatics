from menu import unauthenticated_menu
import streamlit as st
from st_files_connection import FilesConnection
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from plotting import format_figure

st.set_page_config(
    page_title="Active Learning",
    page_icon="🏃🏽<200d>♀️🏼",
    layout="wide",
)

conn = st.connection('gcs', type=FilesConnection)
df = conn.read("materials_informatics_portfolio/qm9_ecfp4_sample.csv", input_format="csv", ttl=600)
initial_preds_df = conn.read("materials_informatics_portfolio/initial_preds.csv", input_format="csv", ttl=600)
y_max_df = conn.read("materials_informatics_portfolio/y_max.csv", input_format="csv", ttl=600)
final_preds_df = conn.read("materials_informatics_portfolio/final_preds.csv", input_format="csv", ttl=600)

st.write("# Active Learning 🏃🏽‍♀️")

st.write("## Background")
st.write("### HOMO/LUMO energies")
st.write("The energy gap between the :violet[HOMO] (highest occupied molecular orbital)  and :violet[LUMO] (lowest unoccupied molecular orbital) determines how easily electrons can be excited in a given molecule: the smaller the :violet[HOMO-LUMO] gap, the less energy is required to excite an electron from the :violet[HOMO] to the :violet[LUMO]. The :violet[HOMO-LUMO] gap also dictates what wavelengths of light a molecule can absorb.")
st.write("In the figure below, I've plotted the distributions of the :violet[HOMO] and :violet[LUMO] energies in a sample of the <a href='https://paperswithcode.com/dataset/qm9' target='_blank'>`qm9`</a> dataset. In general, :violet[LUMO] energies lie above :violet[HOMO] energies, and for a given molecule, the :violet[LUMO] is *always* above the :violet[HOMO].", unsafe_allow_html=True)

fig = make_subplots(rows=1, cols=1)
fig.add_trace( go.Histogram( x = df.homo, marker=dict(color='lime'), name = 'homo' ) )
fig.add_trace( go.Histogram( x = df.lumo, marker=dict(color='cyan'), name = 'lumo' ) )
fig.update_layout(
    xaxis_title="Energy"
)
format_figure(fig)
fig.update_traces(marker_line_width=1,marker_line_color="white")
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("### Active learning")
st.write("Active learning is a machine learning (ML) approach where the ML model predictions and uncertainties are used to decide what data point to evaluate next in a search space. In the context of materials and chemicals, active learning is often used to guide design and optimization.") 
unauthenticated_menu()
