import streamlit as st

def format_figure(fig):
    fig.update_layout(
        plot_bgcolor='#2c016d',
        yaxis = dict(
                    tickfont = dict(size=18),
                    showgrid=True, gridwidth=0.8, gridcolor='white',
                    color='white'
                    ),
        yaxis_title = dict(
                          font = dict(size=20),
                          ),
        xaxis = dict(
                    tickfont = dict(size=18),
                    showgrid=True, gridwidth=0.8, gridcolor='white',
                    color='white'
                    ),
        xaxis_title = dict(
                          font = dict(size=20),
                          standoff = 10
                          ),
        legend = dict(font = dict(size=20)),
        legend_title=None
    
    )
    return
