import numpy as np

def manual_train_split(df, train_sample=80):
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
    rf_columns = ['player_id', 'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']

    possible_games = list(df['game_id'].unique())
    game_numbers = len(possible_games)

    games_to_sample = np.random.choice(game_numbers, train_sample)

    games_to_train_on = []
    for i in games_to_sample:
        games_to_train_on.append(possible_games[i])
    
    for game in games_to_sample:
        if game in possible_games:
            possible_games.remove(game)
    
    return possible_games, games_to_train_on
    
    
    