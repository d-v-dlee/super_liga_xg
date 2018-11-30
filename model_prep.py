import numpy as np
import pandas as pd

def manual_train_split(df, train_sample_size=80):
    """input dataframe of shots, return train_test_split by game_id
    
    input dataframe -> get unique game ids -> take sample of 80/159 (may be some repeasts from 
    np.random.choice)

    first for loop: take those game ids and then add them to games_to_train_on
    second for loop: drop those games from the master 'possible_games' list

    return dataframe of shots (in specific games) to train model on
    --------------------------------------------------------------------
    holdout_test, train = manual_train_split(shots_df)
    returns: game_ids to hold out/predict on, list to train on
    """

    possible_games = list(df['game_id'].unique())
    game_numbers = len(possible_games)

    games_to_sample = np.random.choice(game_numbers, train_sample_size)

    games_to_train_on = []
    for i in games_to_sample:
        games_to_train_on.append(possible_games[i])
    
    for game in games_to_train_on:
        if game in possible_games:
            possible_games.remove(game)
    
    return possible_games, games_to_train_on

def manual_test_split(possible_games, test_sample_size=50):
    """input: possible_games which is game_ids minus the game_ids used for training
    output: list of games_ids to predict and remaining holdout set
    
    first for loop: takes random sample, then corresponding game_ids in list (by position)
    second for loop: removes those sample games from the possible_games list, leaving final holdout_list"""

    games_left = len(possible_games)

    games_to_sample = np.random.choice(games_left, test_sample_size)

    games_to_predict = []
    for i in games_to_sample:
        games_to_predict.append(possible_games[i])

    for game in games_to_predict:
        if game in possible_games:
            possible_games.remove(game)
    
        holdout_games = possible_games.copy()
    
    return holdout_games, games_to_predict
        
def create_training_df(df, train_sample_size=90):
    """input total shot df and return training data split into train_data (x) and train_y (y)
    
    ex: train_data, train_y, indices, hold_test = training_df(shots_df)
    
    """
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    hold_test, train = manual_train_split(df)
    shots_to_train_on = df[df['game_id'].isin(np.array(train))].copy()
    train_data = shots_to_train_on[rf_columns]
    train_y = shots_to_train_on['is_goal']
    indices = shots_to_train_on.index.values

    return train_data, train_y, indices, hold_test

def create_test_df(df, hold_test):
    """input df, and previous hold_test from training_df to return
    test_data and test_y to be run through rf"""
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    holdout, test = manual_test_split(hold_test)
    shots_to_predict = df[df['game_id'].isin(np.array(test))].copy()
    test_data = shots_to_predict[rf_columns]
    test_y = shots_to_predict['is_goal']
    indices1 = shots_to_predict.index.values

    return test_data, test_y, indices1, holdout, test


def create_xG_df(test_data, test_y, model_predictions):
    """create new dataframe with predicted probas and actual goals for predicted shots"""
    df = pd.DataFrame(test_data)
    df['is_goal'] = test_y
    df['xG'] = model_predictions[:, 1]
    df['xA'] = df['assisted_shot'] * df['xG']
    return df

def create_summed_xG_df(df):
    """input xg_df and return dataframe of summed xg and xa for each player"""
    unique_players = df['player_id'].unique()
    contributions = []
    for player in unique_players:
        xgsum = round(df[df['player_id'] == player]['xG'].sum(), 2)
        xasum = round(df[df['player_id'] == player]['xA'].sum(), 2)
        xgxasum = round(xgsum + xasum, 2)
        goals = df[df['player_id'] == player]['is_goal'].sum()
        contributions.append([player, xgsum, xasum, xgxasum, goals])
    by_xG = sorted(contributions, key=lambda x: x[1], reverse=True)
    contribution_df = pd.DataFrame(by_xG, columns=['player_id', 'total_xG', 'total_xA', 'total_xG+xA', 'goals'])
    return contribution_df

### moving from shots to players and minutes


def create_test_min_df(player_df, test):
    """input player_df and the list of games that were predited on to return
    the players and minuts played in the predicted games"""
    min_df = player_df[player_df['game_id'].isin(np.array(test))].copy()
    
    players = min_df['player_id'].unique()
    player_minutes = []
    for player in players:
        total_minutes = min_df[min_df['player_id'] == player]['minutes_played'].sum()
        name = min_df[min_df['player_id'] == player]['name'].iloc[0]
        player_minutes.append([player, total_minutes, name])
    
    player_minutes_df = pd.DataFrame(player_minutes, columns=['player_id', 'total_minutes_played', 'player_name'])
    return player_minutes_df

def merged_dataframes(player_df, contribution_df):
    columns = ['player_name', 'player_id', 'total_xG', 'total_xA', 'total_xG+xA', 'goals', 'xG+xA/90', 'total_minutes_played']
    xg_min = pd.merge(contribution_df, player_df, on='player_id', how='outer')
    xg_min['xG+xA/90'] = xg_min['total_xG+xA'].copy() / (xg_min['total_minutes_played'] / 90)
    xg_final = xg_min[columns]
    return xg_final
