import streamlit as st

def format_figure(fig):
    fig.update_layout(
        plot_bgcolor='black',
        yaxis = dict(
                    tickfont = dict(size=18),
                    showgrid=True, gridwidth=0.8, gridcolor='#F2CEE6',
                    color='#F2CEE6'
                    ),
        yaxis_title = dict(
                          font = dict(size=20),
                          ),
        xaxis = dict(
                    tickfont = dict(size=18),
                    showgrid=True, gridwidth=0.8, gridcolor='#F2CEE6',
                    color='#F2CEE6'
                    ),
        xaxis_title = dict(
                          font = dict(size=20),
                          standoff = 10
                          ),
        legend = dict(font = dict(size=20)),
        legend_title=None
    
    )
    return
