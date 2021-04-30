# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 02:30:17 2021

@author: roany
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
pd.options.display.max_columns = 500
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly

st.beta_set_page_config(layout='wide') #page_icon='Images/icon4.png', 

@st.cache(persist=True, allow_output_mutation=True, show_spinner = True)
def load_data():
    games = pd.read_pickle('data/games.pkl')

    players = pd.read_pickle('data/players.pkl')

    epl = pd.read_pickle('data/epl.pkl')
    
    return games, players, epl

games, players, epl = load_data()


#st.sidebar.title('Filter:')
#st.sidebar.text('April 2021 | Rohan Ahire')    


option = st.sidebar.selectbox(
    'Select Page',
     ['Clubs',  'Players'])

  


img_url = "https://www.fifplay.com/img/public/premier-league-3-logo.png"
link = "https://www.premierleague.com/"    

html = f""" 
       <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
       <a href='{link}'><img style='display:block; width:450px;height:100px;margin-left:320px;margin-bottom:45px'  
       src='{img_url}'/></a>"""
       
    
   
st.markdown(html,  unsafe_allow_html=True) 


if option == 'Clubs': 
    
    
    club_name = st.sidebar.selectbox('Enter Club: ', list(epl['club'].value_counts().index)) 
    

    
    colors = ['lightslategray'] * 16
    colors[0] = 'crimson'
    
    df_plot = epl[epl['club'] == club_name]['nationality'].value_counts()
    
     
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Club vs Nationality of players", "Player Market Value"),
                   vertical_spacing=0.2)

    
    fig.add_trace(
        go.Bar(x=df_plot.index,
        y=df_plot.values,
        marker_color=colors), row=1, col=1)
    
    market_df = epl[epl['club'] == club_name].sort_values(by=['market_value'], ascending=False).head(10)[['name', 'market_value']]
    
    colors = ['lightslategray',] * 16
    colors[0] = '#1f77b4'
    
    fig.add_trace(go.Bar(
        x=market_df['name'],
        y=market_df['market_value'],
        marker_color=colors
    ), row=1, col=2)
    
    # Update xaxis properties
    fig.update_xaxes(title_text="Country", row=1, col=1)
    fig.update_xaxes(title_text="Player", row=1, col=2)
    
    # Update yaxis properties
    fig.update_yaxes(title_text="Number of Players", row=1, col=1)
    fig.update_yaxes(title_text="Market Value (In Million Euros)", row=1, col=2)
    
    fig.update_layout(height=500, width=1000, showlegend=False)    
    st.plotly_chart(fig, use_container_width=True)
    
    
    mvp_df = epl[epl['club'] == club_name].groupby(['position'])['market_value'].mean().round(2).sort_values(ascending=True)
    
    colors = ['lightslategray',] * 16
    colors[len(mvp_df)-1] = '#9467bd'
    
    fig = go.Figure(data=[go.Bar(
        x=mvp_df.values,
        y=mvp_df.index,
        marker_color=colors, orientation='h'
    )])
    fig.update_layout(title_text='Position wise average Market Value of Players', height=500, width=1100,
                     yaxis_title = 'Position', xaxis_title = 'Market Value (in Million Euros)')    
    st.plotly_chart(fig)
    
    
    
    avm_df = epl[epl['club'] == club_name].groupby(['age'])['market_value'].mean()

    pva_df = epl[epl['club'] == club_name].groupby(['position'])['age'].mean().round().sort_values(ascending=False)


    fig = make_subplots(rows=1, cols=2, subplot_titles=("Age wise average Market Value of Players", 
                                                        "Position wise average Age of Players"),
                                                         vertical_spacing=0.2)
    
    colors = ['#17becf',] * 16
    
    fig.add_trace(
        go.Bar(
                x=avm_df.index,
                y=avm_df.values,
                marker_color=colors
            ), row=1, col=1)
    
    colors = ['#ff7f0e',] * 16
    
    fig.add_trace(
        go.Bar(
            x=pva_df.index,
            y=pva_df.values,
            marker_color=colors
        ), row=1, col=2)
    
    fig.update_xaxes(title_text="Age", row=1, col=1)
    fig.update_xaxes(title_text="Position", row=1, col=2)
    
    # Update yaxis properties
    fig.update_yaxes(title_text="Market Value (in Million Euros)", row=1, col=1)
    fig.update_yaxes(title_text="Average Age", row=1, col=2)
    
    fig.update_layout(height=500, width=1000, showlegend=False)    
    st.plotly_chart(fig, use_container_width=True)

    
   # ======================= Data Table ============================
   
    table_df = epl[epl['club'] == club_name][['name', 'age', 'position',
                                             'nationality', 'market_value']]
    
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(['Player Name', 'Age', 'Position', 'Nationality', 'Market Value']),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=table_df.transpose().values.tolist(),
               fill_color='lavender',
               align='left'))
])
    
    fig.update_layout(height=700, width=1200)
    
    st.plotly_chart(fig)
    
    
else: 
    
    player_name = st.sidebar.selectbox('Enter Player: ', list(players['full'].value_counts().index))
    
    players_attack = players[players['full'] == player_name].groupby(['full'])[['assists', 'goals_scored',
                                                                             'penalties_missed']].sum()
    
    players_defense = players[players['full'] == player_name].groupby(['full'])[['clean_sheets', 'own_goals','red_cards',
                                                                             'yellow_cards','penalties_saved']].sum()
    
        
    
    fig2 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                         subplot_titles = ('Attack Stats',' Defense Stats'))

    fig2.add_trace(go.Pie(labels=players_attack.columns.tolist(), values=players_attack.values.tolist()[0],
                    marker=dict(colors=plotly.colors.sequential.YlOrRd_r,line=dict(color='#FFF', width=1)),pull=[0,0,0,0,0,0,0]),
              1, 1)
    fig2.add_trace(go.Pie(labels=players_defense.columns.tolist(), values=players_defense.values.tolist()[0],
              marker=dict(colors=plotly.colors.sequential.Teal_r, line=dict(color='#FFF', width=1)),pull=[0,0,0,0,0,0,0]), 
              1, 2)
    fig2.update_traces(hole=.5, hoverinfo="label+value",showlegend=False, textinfo='label+value')
    fig2.update_layout( width = 800, height = 500, title = 'Player Stats')  
    fig2.layout.annotations[0].update(x=0.095)
    fig2.layout.annotations[1].update(x=0.65)
    
    st.plotly_chart(fig2, use_container_width=True)
    
  
    
    st.table(players[players['full'] == player_name].groupby(['team'])[['assists', 'goals_scored', 'own_goals', 'penalties_missed',
                   'clean_sheets','red_cards','yellow_cards','penalties_saved']].sum())
   
    
html_name = f""" 
       <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
       <div class='text-center mt-10'><p>April 2021 | Rohan Ahire</p></div>"""
         
   
st.markdown(html_name,  unsafe_allow_html=True) 
