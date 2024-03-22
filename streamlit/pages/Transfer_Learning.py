from menu import unauthenticated_menu
from sklearn.metrics import r2_score, mean_absolute_error
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from plotting import format_figure
from st_pages import Page, show_pages, add_page_title
import os

wd = os.getcwd()
par_d = os.path.abspath(os.path.join(wd, os.pardir))

st.write("# Transfer Learning 🤝🏼")

# Data & ML
expt_gap_df = pd.read_csv(f'{par_d}/data/matbench_expt_gap_featurized.csv')
theor_gap_df = pd.read_csv(f'{par_d}/data/matbench_mp_gap_featurized.csv')

conductors_expt = expt_gap_df[ expt_gap_df['gap expt'] < 0.1 ]
semiconductors_expt = expt_gap_df[ (expt_gap_df['gap expt'] > 0.1) & (expt_gap_df['gap expt'] < 5) ]
insulators_expt = expt_gap_df[ expt_gap_df['gap expt'] > 5 ] 

expt_gap_df['type'] = ['conductor']*len(expt_gap_df)
expt_gap_df.loc[semiconductors_expt.index, 'type'] = ['semiconductor']*len(semiconductors_expt)
expt_gap_df.loc[insulators_expt.index, 'type'] = ['insulator']*len(insulators_expt)

no_tl_pred_df = pd.read_csv('no_tl_expt_gap_pred_lv.csv')
y_true_no_tl_lv = no_tl_pred_df.y_true
y_pred_no_tl_lv = no_tl_pred_df.y_pred

tl_pred_df = pd.read_csv('tl_expt_gap_pred_lv.csv')
y_true_tl_lv = tl_pred_df.y_true
y_pred_tl_lv = tl_pred_df.y_pred

# Display

# Background
st.write("## Background")
st.write("### Band gaps")
st.write("The band gap of a material dictates many of its electrical properties and defines whether or not it is an :violet[insulator], a :violet[semiconductor], or a :violet[conductor]. A model that can predict the experimental band gap of a given material, as well as guide/screen new materials, is useful in a variety of electronic applications.")
st.write("In the histogram below, the counts of each of these materials types are shown for an experimental dataset (*note*: I have used cutoffs of 0.1 eV and 5 eV for classification purposes - *i.e.*, anything with a band gap less than 0.1 eV is a :violet[conductor], anything with a band gap greater than 5 eV is an :violet[insulator], and everything else is a :violet[semiconductor]). We see that the dataset is dominated by :violet[conductors] and is thus imbalanced. To get a closer look at the counts of :violet[semiconductors] and :violet[insulators], you can use <a href='https://plotly.com/' target='_blank'>`plotly`</a>'s zoom and pan features at the top right of the figure.", unsafe_allow_html=True)

fig = px.histogram( data_frame = expt_gap_df, x = 'gap expt', color = 'type', color_discrete_sequence=["deepskyblue", "#52FFB3", 
                    "#C1AFF6"]  )
fig.update_layout(
    xaxis_title="Experimental band gap (eV)"
)
format_figure(fig)
fig.update_traces(marker_line_width=1,marker_line_color="#F2CEE6")
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("### Transfer learning")
st.write("Transfer learning is a machine learning (ML) approach where knowledge gained from a pre-trained model is used in the training of another model. Usually the pre-trained model is trained on a higher quality or more general dataset, and the target model is trained on a lower quality or more specific dataset. The goal is usually to *speed up and/or improve learning on the target task*. There are many transfer learning methods; here, I explore two: i) a :violet[latent variable (LV)] approach, where the output of the pre-trained model is used as an input feature to the target model, and ii) a :violet[fine-tuning (FT)] approach, where some optimized parameters of the pre-trained model are used to initialize the parameters of the target model.") 

st.image('pre-trained model.svg')

# Approach
st.write("## Approach")
st.write("Here, I develop a ML model that can predict the experimental band gap of a material given only its composition, utilizing transfer learning to improve the accuracy of the model. In this case, I am using a model trained on a theoretical band gap dataset, where the band gaps have been computed with density functional theory, as the pre-trained model, and we use this model to transfer learn to a smaller experimental band gap dataset. Both datasets were taken from <a href='https://matbench.materialsproject.org/' target='_blank'>`matbench`</a>. To handle duplicate compositions, I averaged the band gap over a given duplicated composition and kept it if the standard deviation was less than 0.5 eV.", unsafe_allow_html=True)

st.write("### Latent Variable Approach")
st.write("For the :violet[LV] approach, I will be utilizing random forests (RFs) instead of neural networks (NNs) to demonstrate the power of RF models for small materials datasets. NNs are data-hungry and often don't outperform RF models for small datasets (by small, I mean having on the order of a few thousand training data points or less). All of the RF models here were built with <a href='https://scikit-learn.org/stable/' target='_blank'>`scikit-learn`</a>. For a Jupyter notebook version with all relevant code, see <a href='https://github.com/sarah-allec/materials_informatics/blob/main/notebooks/latent_variable.ipynb' target='_blank'>here</a>.", unsafe_allow_html=True)

st.write("#### Model Without Transfer Learning")
st.write("Let's first analyze the accuracy of the experimental band gap model *without transfer learning*. In the parity plot below, which displays the ML-predicted band gap as a function of the true experimental band gap, we see that for non-metals, the data points generally lie along the parity line (green dashed line), signifying that the ML model has decent predictive capability. However, many of the metals are predicted to have band gaps much greater than 0, leading to a vertical line at x = 0." ) 
fig = px.scatter( x = y_true_no_tl_lv, y = y_pred_no_tl_lv, color_discrete_sequence=["deepskyblue"] )
fig.add_trace( go.Scatter(x=y_true_no_tl_lv, y=y_true_no_tl_lv,
                    mode='lines', line = dict(shape = 'linear', color = '#C1E1C1', dash = 'dash'),
                    showlegend=False, name='Parity line') )
fig.update_layout(
    xaxis_title="Actual band gap (eV)", yaxis_title="Predicted band gap (eV)"
)
format_figure(fig)
fig.update_traces(marker=dict(size=10, symbol='circle-open', line=dict(width=1.5)))
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("#### Model With Transfer Learning")
st.write("I now utilize the outputs of a pre-trained model trained on theoretical band gaps. This dataset is much larger than the experimental band gap dataset, as shown in the histogram below. We expect that the dataset is more diverse and will learn a more general relationship between composition and band gap. This is reflected in the fact that the pre-trained model has a much higher coefficient of determination, 0.9, than the experimental band gap model.")

fig = make_subplots(rows=1, cols=1)
fig.add_trace( go.Histogram( x = expt_gap_df['gap expt'], marker=dict(color='lime'), name = 'expt' ) )
fig.add_trace( go.Histogram( x = theor_gap_df['gap pbe'], marker=dict(color='cyan'), name = 'theor' ) ) 
fig.update_layout(
    xaxis_title="Band gap (eV)"
)
format_figure(fig)
fig.update_traces(marker_line_width=1,marker_line_color="#F2CEE6")
st.plotly_chart(fig, theme=None, use_container_width=True)

st.write(" The parity plot below shows the accuracy improvement as a result of transfer learning, where the yellow circles are the transfer-learned predictions and the sky blue circles are the original (non-transfer-learned) predictions. In particular, the coefficient of determination for non-metal band gap prediction has now increased from 0.70 in the original model to 0.87 and the mean absolute error for non-metal band gap prediction has decreased from 0.5 eV to 0.4 eV.")

fig = make_subplots(rows=1, cols=1)
fig.add_trace( go.Scatter( x = y_true_tl_lv, y = y_pred_tl_lv, mode='markers',
               marker=dict(color='#FDFD96'), name='transfer-learned' ) )
fig.add_trace( go.Scatter( x = y_true_no_tl_lv, y = y_pred_no_tl_lv, mode='markers',
               marker=dict(color='deepskyblue'), name='original' ) )

fig.add_trace( go.Scatter(x=y_true_tl_lv, y=y_true_tl_lv,
                    mode='lines', line = dict(shape = 'linear', color = '#C1E1C1', dash = 'dash'),
                    showlegend=False, name='Parity line') )
fig.update_layout(
    xaxis_title="Actual band gap (eV)", yaxis_title="Predicted band gap (eV)"
)
format_figure(fig)
fig.update_traces(marker=dict(size=10, symbol='circle-open', line=dict(width=1.5)))

st.plotly_chart(fig, theme=None, use_container_width=True)

#st.write("### Fine-Tuning Approach")
#st.write("For the :violet[FT] approach, I will be utilizing NNs instead of RFs because :violet[FT] requires the sharing of optimized hyperparameters between models, but RF typically does not require any sort of hyperparameter tuning. This hyperparameter tuning process is what allows for significant flexibility in the types of relationships NNs can learn, and thus the knowledge that a NN learns is encoded in its hyperparameters. All NN models here were built with  <a href='https://pytorch.org/' target='_blank'>`pytorch`</a>.", unsafe_allow_html=True) 
#unauthenticated_menu()
