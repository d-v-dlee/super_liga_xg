import numpy as np  

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

