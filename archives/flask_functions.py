import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from combined_player import player_minutes_value
from html_scraper import db
from mongo_to_db import create_master_df
from model_prep import create_rf_prep, create_xG_df, create_summed_xG_df


def superliga_xgboost_df():
    """return dataframe of top 20 players under 25, with min 300 minutes played,
    sorted by xG+xA/90"""

    #load data from mongoDB
    games = db.games.find()
    players = db.players.find()

    #create player and shot dataframe, turn shots_df into df ready for model
    final_df = player_minutes_value(games, players)
    games = db.games.find()
    shots_df = create_master_df(games)
    model_ready_df = create_rf_prep(shots_df)

    xgb_model = pickle.load(open("xgb.pkl", "rb"))
    columns = ['shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    p_xgboost = xgb_model.predict_proba(model_ready_df[columns])

    #predict probabilities, find total_xG and other stats
    xgb_xg = create_xG_df(model_ready_df, shots_df['is_goal'], p_xgboost)
    xgb_contributions = create_summed_xG_df(xgb_xg)

    #merge the final_df(player information) with xgb_contribubtions (xG stats)
    xgb_sl = pd.merge(xgb_contributions, final_df, on=['player_id'])
    xgb_sl['xG+xA/90'] = xgb_sl['total_xG+xA'] / (xgb_sl['total_minutes_played'] / 90 )

    final_col = ['player_id', 'player_name', 'club', 'birthday', 'age', 'foot', 'squad_num',
       'total_xG', 'total_xA', 'total_xG+xA', 'goals', 'xG+xA/90', 'transfer_value(USD)', 'total_minutes_played']
    
    xgb_sl_final = xgb_sl[final_col]
    return xgb_sl_final


def top_20_young(min_minutes=300, max_age=25):
    """returns scatter plot of 20 young players by xG+xA/90 vs value and age
    as well as dataframe"""
    df = pd.read_csv('xgboost_table.csv')
    top_20_df = df[(df['transfer_value(USD)'] < 8) & (df['total_minutes_played'] >= 300 ) & (df['age'] <= 25)].sort_values(by=['xG+xA/90'], ascending=False).head(20).copy()
    return top_20_df
    
# def top_20_scatter(df):
#     pass    
#     fig, (ax, ax1) = plt.subplots(2, 1)
#     fig.set_figheight(15)
#     fig.set_figwidth(15)

#     ax.scatter(top_20_df['age'], top_20_df['xG+xA/90'], alpha=0.7)
#     ax.set_title('Age vs. xG+xA/90 for Top 20 Young Performers')
#     ax.set_ylabel('xG+xA/90')
#     ax.set_xlabel('Age')
#     ax.plot()

#     ax1.scatter(top_20_df['transfer_value(USD)'], top_20_df['xG+xA/90'], alpha=0.7)
#     ax1.set_title('Transfer Value vs. xG+xA/90 for Top 20 Young Performers')
#     ax1.set_ylabel('xG+xA/90')
#     ax1.set_xlabel('Player Value in Millions (USD)')
#     ax1.plot()

    # return top_20_df


def create_scrollable_table(df):
    trace = go.Table(
        header=dict(values=list(df.columns),
                    fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
        cells=dict(values=[df.player_name, df.club, df.age, df.foot],
                fill = dict(color='#F5F8FF'),
                align = ['left'] * 5))

    data = [trace] 
    py.iplot(data, filename = 'pandas_table')



def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
