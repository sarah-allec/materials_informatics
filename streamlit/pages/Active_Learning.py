from menu import unauthenticated_menu
import streamlit as st
from st_files_connection import FilesConnection
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from plotting import format_figure
from pathlib import Path

path = Path(__file__).parents[1]

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
st.write("Active learning is a machine learning (ML) approach where the ML model predictions and uncertainties are used to decide what data point to evaluate next in a search space. In the context of materials and chemicals, active learning is often used to guide design and optimization. To decide what material or experiment to run next, we utilize :violet[acquisition functions] to either *explore* or *exploit* the search space. For example, if we seek to optimize a particular chemical property, we would utilize an *exploitive* :violet[acquisition function] that prioritizes compounds predicted to have property values close to our target value. On the other hand, if we want to *explore* the search space and diversify our training data, we would utilize an *explorative* :violet[acquisition function] that prioritizes compounds for which the model is most uncertain. For more information on :violet[acquisition functions], see <a href='https://tune.tidymodels.org/articles/acquisition_functions.html' target='_blank'>`here`</a> and <a href='https://ekamperi.github.io/machine%20learning/2021/06/11/acquisition-functions.html' target='_blank'>`here`</a>", unsafe_allow_html=True) 

st.write("Active learning is typically performed iteratively - *i.e.*, the process of training the model, picking which compounds to test experimentally (or with simulations), and adding the experimental results to the training data is repeated until some target is reached. This is displayed in the schematic below.")

st.image(f'{path}/active learning loop.svg')

st.write("## Approach")
st.write("Here, I will use Gaussian process models to perform active learning with the goal of maximizing the :violet[LUMO] energy of a sample of the <a href='https://paperswithcode.com/dataset/qm9' target='_blank'>`qm9`</a> dataset. I have chosen Gaussian processes because they tend to be robust across all dataset sizes, generally don't require extensive hyperparameter tuning, and naturally return prediction uncertainties (epistemic uncertainties in particular, if you're interested). This last point is particularly important for active learning because without good uncertainty estimates, the range of :violet[acquisition functions] one can use is limited. All models here were built with <a href='https://www.gpflow.org/' target='_blank'>`GPflow`</a>. For the dataset, I randomly sampled 10,000 data point from the entire <a href='https://paperswithcode.com/dataset/qm9' target='_blank'>`qm9`</a> dataset. For a Jupyter notebook version with all relevant code, see <a href='https://github.com/sarah-allec/materials_informatics/blob/main/notebooks/active_learning.ipynb' target='_blank'>here</a>.", unsafe_allow_html=True) 

st.write("### Initial model")
st.write("To simulate a real-world scenario, I started with an initial training dataset of 50 data points, sampled randomly from the 10,000 data points I initially took from <a href='https://paperswithcode.com/dataset/qm9' target='_blank'>`qm9`</a>. Let's first analyze the accuracy of a model built with this small dataset. In the parity plot below, which displays the ML-predicted :violet[LUMO] energy as a function of the true :violet[LUMO] energy for the rest of the 9,950 molecules, we see that this model is pretty flat, which means its accuracy is low. Fortunately, active learning does not require very accurate models for materials discovery, as demonstrated by <a href='https://pubs.rsc.org/en/content/articlelanding/2023/dd/d2dd00113f' target='_blank'>Borg *et al.*</a>.", unsafe_allow_html=True)

fig = px.scatter( x = initial_preds_df.y_true, y = initial_preds_df.y_pred, color_discrete_sequence=["deepskyblue"] )
fig.add_trace( go.Scatter(x=initial_preds_df.y_true, y=initial_preds_df.y_true,
                    mode='lines', line = dict(shape = 'linear', color = '#C1E1C1', dash = 'dash'),
                    showlegend=False, name='Parity line') )
fig.update_layout(
    xaxis_title="Actual LUMO energy", yaxis_title="Predicted LUMO energy"
)
format_figure(fig)
fig.update_traces(marker=dict(size=10, symbol='circle-open', line=dict(width=1.5)))
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("### Active learning")
st.write("In a typical active learning loop, the number of compounds to test in each iteration is dictated by the cost, difficulty, and timescale of the experiment or simulation. Here, I chose to select 10 compounds at each step, although for this particular case, experimental measurements of HOMO/LUMO energies via voltammetry and theoretical estimates via *ab initio* methods could reasonably afford a higher number. Here, I simply take the value in the <a href='https://paperswithcode.com/dataset/qm9' target='_blank'>`qm9`</a> database, which is a theoretical value. I performed 100 steps of active learning, where I initially use an *explorative* :violet[acquisition] function in order to build up the training data and improve model accuracy, and then I switch to a more *exploitive* :violet[acquisition] function when the accuracy is above some threshold.", unsafe_allow_html=True) 
st.write("The figure below plots the maximum :violet[LUMO] energy in the training data at each active learning step. For comparision, I do the same but for random sampling (no acquisition function). It is pretty amazing that out of the nearly 10,000 molecules in the search space, active learning finds the molecule with the maximum :violet[LUMO] energy in less than 30 steps, and finds another molecule very close to the maximum in less than 10 steps.", unsafe_allow_html=True)

fig = make_subplots(rows=1, cols=1)
fig.add_trace( go.Scatter( x = list(range(len(y_max_df))), y = [0.1055]*len(y_max_df), mode='lines', line=dict(shape='linear', color='#FDFD96', dash='dash'), name = 'maximum' ) ) 
fig.add_trace( go.Scatter( x = list(range(len(y_max_df))), y = y_max_df.y_max_al, mode='lines', line=dict(shape='linear', color='lime'), name = 'active learning' ) )
fig.add_trace( go.Scatter( x = list(range(len(y_max_df))), y = y_max_df.y_max_rand, mode='lines', line=dict(shape='linear', color='cyan'), name = 'random' ) )
fig.update_layout(
    xaxis_title="Step",
    yaxis_title="Max. LUMO energy"
)
format_figure(fig)
fig.update_traces(marker_line_width=1,marker_line_color="white")
st.plotly_chart(fig, theme=None, use_container_width=True)

unauthenticated_menu()
