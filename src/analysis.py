import numpy as np  
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd

xg_df = pd.read_csv('../data/xgb_df.csv')

def shots_per_game(subset_df, shots_df):
    """
    subset_df - df of interest which represents specific players to focus on - like top_scorers
    shot_df - shots_df with all shot data 
    return shots_per_game for those players of interest """
    unique_players = subset_df['player_id'].unique()

    shots_per_game = []
    for player_id in unique_players:
        games_played = len(shots_df[shots_df['player_id'] == player_id]['game_id'].unique())
        total_shots = len(shots_df[shots_df['player_id'] == player_id])
        spg = round(total_shots/games_played, 2)
        shots_per_game.append(spg)
    return np.mean(shots_per_game).round(2)

def shots_df_average(subset_df, shots_df, category, subset=True):
    """return average based on shots_df, if subset "True"
    only return for unique, if "False" return average for whole population"""
    unique_players = subset_df['player_id'].unique()
    if subset:
        mean_val = shots_df[shots_df['player_id'].isin(unique_players)][category].mean()
        return round(mean_val, 2)
    else:
        mean_val = shots_df[~shots_df['player_id'].isin(unique_players)][category].mean()
        return round(mean_val, 2)

def plot_shot_map(df):
    """input shot df and show shots by color or marks"""
    img1 = mpimg.imread('../data/soccer_field.jpg')
    imgplot = plt.imshow(img1)
    ax = plt.gca()
    ax.scatter((df[df['is_goal']==0]['shot_coord_x1'] * 6 + 50), (df[df['is_goal']==0]['shot_coord_y1'] * 6.58 + 250), alpha=0.2, color='blue', linewidths=0.1)
    ax.scatter(df[df['is_goal']==1]['shot_coord_x1'] * 6 + 50, df[df['is_goal']==1]['shot_coord_y1'] * 6.58 + 250, alpha=0.5, color='red', linewidths=0.1)

def individual_shot_map(shots_df, player_id):
    """input shots_df and player_id and return shot chart for individual player
    multiply coordinate system by 6 instead of 7.32 for distance and representation
    normally 7.32, here 6"""

    player_df = shots_df[shots_df['player_id'] == player_id ]
    xG = round(xg_df[xg_df['player_id'] == player_id]['total_xG'].iloc[0], 2)
    goals = xg_df[xg_df['player_id'] == player_id]['goals'].iloc[0]
    name = xg_df[xg_df['player_id'] == player_id]['player_name'].iloc[0]

    img1 = mpimg.imread('../data/soccer_field.jpg')
    fig, ax = plt.subplots(figsize=(10, 8))
    imgplot = ax.imshow(img1)
    # ax = plt.gca()
    ax.scatter(player_df[player_df['is_goal']==1]['shot_coord_x1'] * 6 + 50, player_df[player_df['is_goal']==1]['shot_coord_y1'] * 6.58 + 250, alpha=0.7, color='red', marker='o' )
    ax.scatter((player_df[player_df['shot_type']==33]['shot_coord_x1'] * 6 + 50), (player_df[player_df['shot_type']==33]['shot_coord_y1'] * 6.58 + 250), alpha=0.4, color='blue', marker='^')
    ax.scatter((player_df[player_df['shot_type']==35]['shot_coord_x1'] * 6 + 50), (player_df[player_df['shot_type']==35]['shot_coord_y1'] * 6.58 + 250), alpha=0.4, color='blue', marker='v')
    ax.scatter((player_df[player_df['shot_type']==34]['shot_coord_x1'] * 6 + 50), (player_df[player_df['shot_type']==34]['shot_coord_y1'] * 6.58 + 250), alpha=0.4, color='blue', marker='>')
    ax.set_title(f'{name}')
    ax.set_axis_off()
    # ax.annotate(f'xG: {xG}, Goals: {goals}', (400, 400))
    ax.text(250, 400, s=f'xG: {xG}, Goals: {goals}', fontdict={'color': 'white', 'size': 16}, weight='bold')
    ax.legend(labels=['Goal', 'Shot on Target', 'Shot off Target', 'Post'])
    ax.figure.savefig(f'../shot_charts/{name}.png')
    # imgplot.figure.savefig('top_shots.png')

def plot_goals_map(df, xG):
    """input shot df and show shots by color or marks
    multiply coordinates by 6 instead of 7.32"""
    img1 = mpimg.imread('../data/soccer_field.jpg')
    imgplot = plt.imshow(img1)
    ax = plt.gca()
    ax.text(200, 400, s=f' Average xG of Shot: {xG}', fontdict={'color': 'white', 'size': 14}, weight='bold')
    ax.set_axis_off()
    # ax.annotate(f'Average xG: {xG}', (400, 400))
    # ax.scatter((df[df['is_goal']==0]['shot_coord_x1'] * 7.32 + 50), (df[df['is_goal']==0]['shot_coord_y1'] * 6.58 + 250), alpha=0.2, color='blue', linewidths=0.1)
    ax.scatter(df[df['is_goal']==1]['shot_coord_x1'] * 6 + 50, df[df['is_goal']==1]['shot_coord_y1'] * 6.58 + 250, alpha=0.5, color='red', linewidths=0.1)
