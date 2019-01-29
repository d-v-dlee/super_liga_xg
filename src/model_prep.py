import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
import matplotlib.pyplot as plt

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
    """input: possible_games which is game_ids minus the game_ids used for training, 
    test_sample_size is 50 games to predict on, usually less due to random sample
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
    train_sample_size is the number of games (will sample 90 with some possible repeats)
    ex: train_data, train_y, indices, hold_test = training_df(shots_df)
    
    """
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    hold_test, train = manual_train_split(df)
    shots_to_train_on = df[df['game_id'].isin(np.array(train))].copy()
    train_data = shots_to_train_on[rf_columns].astype(float)
    train_y = shots_to_train_on['is_goal'].astype(float)
    indices = shots_to_train_on.index.values

    return train_data, train_y, indices, hold_test

def create_test_df(df, hold_test):
    """input df, and previous hold_test from training_df to return
    test_data and test_y to be run through rf"""
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    holdout, test = manual_test_split(hold_test)
    shots_to_predict = df[df['game_id'].isin(np.array(test))].copy()
    test_data = shots_to_predict[rf_columns].astype(float)
    test_y = shots_to_predict['is_goal'].astype(float)
    indices1 = shots_to_predict.index.values

    return test_data, test_y, indices1, holdout, test

def use_holdout_df(df, holdout):
    """insert df and holdout (game_ids not yet predicted) and return df to predict on"""
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']
    shots_to_predict = df[df['game_id'].isin(np.array(holdout))].copy()
    test_data = shots_to_predict[rf_columns].astype(float)
    test_y = shots_to_predict['is_goal'].astype(float)
    indices1 = shots_to_predict.index.values

    return test_data, test_y, indices1 


def create_xG_df(test_data, test_y, model_predictions):
    """create new dataframe with predicted probas and actual goals for predicted shots"""
    df = pd.DataFrame(test_data)
    df['is_goal'] = test_y
    df['xG'] = model_predictions[:, 1]
    df['xA'] = df['assisted_shot'] * df['xG']
    return df

def create_hypothetical_df(test_data, model_predictions):
    """create new dataframe with predicted probas and actual goals for predicted shots"""
    df = pd.DataFrame(test_data)
    df['xG'] = model_predictions[:, 1]
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
        pen_attempts = df[df['player_id'] == player]['is_penalty_attempt'].sum()
        contributions.append([player, xgsum, xasum, xgxasum, pen_attempts, goals])
    by_xG = sorted(contributions, key=lambda x: x[1], reverse=True)
    contribution_df = pd.DataFrame(by_xG, columns=['player_id', 'total_xG', 'total_xA', 'total_xG+xA', 'pen_attempts', 'goals'])
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

def player_minutes_total(players_minutes_df):
    """input player_minutes_df from create_test_min_df so that each row is a unique player"""
    players = players_minutes_df['player_id'].unique()
    player_minutes = []
    for player in players:
        total_minutes = players_minutes_df[players_minutes_df['player_id'] == player]['minutes_played'].sum()
        name = players_minutes_df[players_minutes_df['player_id'] == player]['name'].iloc[0]
        squad_num = players_minutes_df[players_minutes_df['player_id'] == player]['squad_number'].iloc[0]
        club_brev = players_minutes_df[players_minutes_df['player_id'] == player]['club_brev'].iloc[0]
        position_id = players_minutes_df[players_minutes_df['player_id'] == player]['position_id'].iloc[0]
        player_minutes.append([player, total_minutes, name, squad_num, club_brev, position_id])
    summed_player_min = pd.DataFrame(player_minutes, columns=['player_id', 'total_minutes_played', 'player_name', 'squad_num', 'club_brev', 'position_id'])
    return summed_player_min


def create_rf_prep(df):
    """input df, return the appropriate columns to be run through rf"""
    rf_columns = ['shot_distance', 'shot_angle', 'assisted_shot'] #, 'is_penalty_attempt']
    return df[rf_columns].astype(float)

#use to tune classifiers

def stage_score_plot(estimator, X_train, y_train, X_test, y_test):
    '''
    Parameters: estimator: GradientBoostingClassifier or xgBoostClassifier
                X_train: pandas dataframe
                y_train: 1d panda dataframe
                X_test: pandas dataframe
                y_test: 1d panda dataframe

    Returns: A plot of the number of iterations vs the log loss for the model for
    both the training set and test set.
    '''
    # fit estimator
    estimator.fit(X_train, y_train)
    train_logloss_at_stages = []
    test_logloss_at_stages = []
    
    # iterate through all stages for test and train and record log loss lists
    for y1, y2 in zip(estimator.staged_predict_proba(X_train), estimator.staged_predict_proba(X_test)):
        train_logloss = log_loss(y_train, y1)
        train_logloss_at_stages.append(train_logloss)
        
        test_logloss = log_loss(y_test, y2)
        test_logloss_at_stages.append(test_logloss)

    # find the # of trees at which test error is the lowest
    lowest_test_error = np.min(test_logloss_at_stages)
    num_trees_lowest_test_error = np.argmin(test_logloss_at_stages)

    # create xs in order to plot. each x represents n_estimators.
    xs = range(0, len(test_logloss_at_stages))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(xs, train_logloss_at_stages, 
            label="{} Train".format(estimator.__class__.__name__))
    ax.plot(xs, test_logloss_at_stages, 
            label="{} Test".format(estimator.__class__.__name__))
    ax.axvline(num_trees_lowest_test_error)
    ax.legend()
    return lowest_test_error, num_trees_lowest_test_error
    # print(f'lowest test error(log loss): {lowest_test_error}')
    # print(f'num_trees at lowest test error: {num_trees_lowest_test_error}')


    # example of how to use:
    # fig, ax = plt.subplots(figsize=(12, 8))
    # stage_score_plot(gdbr_model, X_train, y_train, X_test, y_test)
    # stage_score_plot(gdbr_model_2, X_train, y_train, X_test, y_test)
    # ax.legend()
    # plt.show()

def add_xg_shotdf(shot_df, model_pred):
    """add predicted xG to shot_df"""
    shot_df['xG'] = model_pred[:, 1]