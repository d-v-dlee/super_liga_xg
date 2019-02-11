import pandas as pd
import numpy as np

def pass_to_shot(shot_df, pass_df, time_elapsed=.16667):
    """
    Links shots to previous passes to 
    try to link assists based on time between pass and shot
    ----------
    shot_df: shot_df of a game
    pass_df: completed_pass_df of a game
    time: fraction of a minute between pass and shot, default 10 seconds (.16667 for 1/6)
    
    Returns
    -------
    shots_df with new column 'passed_from_id' and 'coordinates'
    """
    for indx, row in shot_df.iterrows():
        shooter_id = row['player_id']
        shoot_time = row['time_of_event(min)']
        possible_pass_df =  pass_df[(pass_df['rec_player']== shooter_id) & (pass_df['time_of_event(min)'] < shoot_time) & (pass_df['time_of_event(min)'] > shoot_time - time_elapsed)]
        if len(possible_pass_df) == 0:
            shot_df.loc[indx, 'passed_from_id'] = None
        elif len(possible_pass_df) > 1:
            shot_df.loc[indx, 'passed_from_id'] = possible_pass_df.iloc[-1, :]['pass_player'] 
            shot_df.loc[indx, 'pass_coord_x1'] = possible_pass_df.iloc[-1, :]['pass_coord_x1'] 
            shot_df.loc[indx, 'pass_coord_x2'] = possible_pass_df.iloc[-1, :]['pass_coord_x2'] 
            shot_df.loc[indx, 'pass_coord_y1'] = possible_pass_df.iloc[-1, :]['pass_coord_y1'] 
            shot_df.loc[indx, 'pass_coord_y2'] = possible_pass_df.iloc[-1, :]['pass_coord_y2'] 
            shot_df.loc[indx, 'pass_coord_z1'] = possible_pass_df.iloc[-1, :]['pass_coord_z1'] 
            shot_df.loc[indx, 'pass_coord_z2'] = possible_pass_df.iloc[-1, :]['pass_coord_z2']   
        else:
            shot_df.loc[indx, 'passed_from_id'] = possible_pass_df.iloc[0, :]['pass_player']
            shot_df.loc[indx, 'pass_coord_x1'] = possible_pass_df.iloc[0, :]['pass_coord_x1']
            shot_df.loc[indx, 'pass_coord_x2'] = possible_pass_df.iloc[0, :]['pass_coord_x2']
            shot_df.loc[indx, 'pass_coord_y1'] = possible_pass_df.iloc[0, :]['pass_coord_y1']
            shot_df.loc[indx, 'pass_coord_y2'] = possible_pass_df.iloc[0, :]['pass_coord_y2']
            shot_df.loc[indx, 'pass_coord_z1'] = possible_pass_df.iloc[0, :]['pass_coord_z1']
            shot_df.loc[indx, 'pass_coord_z2'] = possible_pass_df.iloc[0, :]['pass_coord_z2']
    return shot_df
    
def corner_to_shot(shot_df, corner_df, time_elapsed=.27):
    """
    Links shots to previous corners to 
    try to link assists based on time between pass and corner
    ----------
    shot_df: shot_df of a game with passes included
    corner_df: corner_df of a game
    time: fraction of a minute between pass and shot, default 16 seconds (because data has a corner assist at that time)
    
    Returns
    -------
    shots_df with updated column 'passed_from_id' and 'pass_id'
    """
    for indx, row in shot_df.iterrows():
        shooter_id = row['player_id']
        shoot_time = row['time_of_event(min)']
        possible_corner_df =  corner_df[(corner_df['time_of_event(min)'] < shoot_time) & (corner_df['time_of_event(min)'] > shoot_time - time_elapsed)]
        if len(possible_corner_df) == 0:
            # shot_df.loc[indx, 'passed_from_id'] = None
            shot_df.loc[indx, 'corner_kick'] = 0
        elif len(possible_corner_df) > 1:
            shot_df.loc[indx, 'passed_from_id'] = possible_corner_df.iloc[-1, :]['player_id'] 
            shot_df.loc[indx, 'pass_coord_x1'] = possible_corner_df.iloc[-1, :]['ck_coord_x1'] 
            shot_df.loc[indx, 'pass_coord_x2'] = possible_corner_df.iloc[-1, :]['ck_coord_x2'] 
            shot_df.loc[indx, 'pass_coord_y1'] = possible_corner_df.iloc[-1, :]['ck_coord_y1'] 
            shot_df.loc[indx, 'pass_coord_y2'] = possible_corner_df.iloc[-1, :]['ck_coord_y2'] 
            shot_df.loc[indx, 'pass_coord_z1'] = possible_corner_df.iloc[-1, :]['ck_coord_z1'] 
            shot_df.loc[indx, 'pass_coord_z2'] = possible_corner_df.iloc[-1, :]['ck_coord_z2']
            shot_df.loc[indx, 'corner_kick'] = 1  
        else:
            shot_df.loc[indx, 'passed_from_id'] = possible_corner_df.iloc[0, :]['player_id']
            shot_df.loc[indx, 'pass_coord_x1'] = possible_corner_df.iloc[0, :]['ck_coord_x1']
            shot_df.loc[indx, 'pass_coord_x2'] = possible_corner_df.iloc[0, :]['ck_coord_x2']
            shot_df.loc[indx, 'pass_coord_y1'] = possible_corner_df.iloc[0, :]['ck_coord_y1']
            shot_df.loc[indx, 'pass_coord_y2'] = possible_corner_df.iloc[0, :]['ck_coord_y2']
            shot_df.loc[indx, 'pass_coord_z1'] = possible_corner_df.iloc[0, :]['ck_coord_z1']
            shot_df.loc[indx, 'pass_coord_z2'] = possible_corner_df.iloc[0, :]['ck_coord_z2']
            shot_df.loc[indx, 'corner_kick'] = 1 
    return shot_df

def transpose_coordinates(input_df, inplace=True):
    """takes a dataframe and transposes all points on one side so that
    all events occur on right side of the grid"""
    if inplace==False:
        df = input_df.copy()
    else:
        df = input_df
    df.loc[df['shot_coord_x1']< 0, ['shot_coord_x1', 'shot_coord_x2', 'shot_coord_y1', 'shot_coord_y2',
                 'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1', 'pass_coord_y2'] ] *= -1
    return df

def coord_to_yards(input_df, x_normalizer=88.8888, y_normalizer=60.538, inplace=True):
    """take a dataframe and turn the coordinats into yardage coordinates from the goal"""
    if inplace==False:
        df = input_df.copy()
    else:
        df = input_df
    df['shot_coord_x1'] = df['shot_coord_x1'].apply(lambda x: (1 - x) / 2 * x_normalizer).round(2)
    df['shot_coord_x2'] = df['shot_coord_x2'].apply(lambda x: (1 - x) / 2 * x_normalizer).round(2)
    df['pass_coord_x1'] = df['pass_coord_x1'].apply(lambda x: (1 - x) / 2 * x_normalizer).round(2)
    df['pass_coord_x2'] = df['pass_coord_x2'].apply(lambda x: (1 - x) / 2 * x_normalizer).round(2)

    df['shot_coord_y1'] = df['shot_coord_y1'].apply(lambda x: x / 2 * y_normalizer).round(2)
    df['shot_coord_y2'] = df['shot_coord_y2'].apply(lambda x: x / 2 * y_normalizer).round(2)
    df['pass_coord_y1'] = df['pass_coord_y1'].apply(lambda x: x / 2 * y_normalizer).round(2)
    df['pass_coord_y2'] = df['pass_coord_y2'].apply(lambda x: x / 2 * y_normalizer).round(2)
    return df


def shot_distance_angle(input_df):
    """take a dataframe and calculate the distance of each shot from the center of the goal
    and the angle of each shot"""
    input_df['shot_distance'] = np.sqrt((0 - input_df['shot_coord_x1']) ** 2 + (0 - input_df['shot_coord_y1']) ** 2)
    input_df['shot_angle'] = (np.arctan(input_df['shot_coord_y1']/input_df['shot_coord_x1']) * (180/np.pi))
    return input_df

def dummy_columns(input_df):
    """add dummy columns on whether or not a shot was preceded by a direct pass
    add dummy columns on whether or not a shot attempt was a penalty
    input: dataframe
    output: dataframe with dummy columns """
    input_df['assisted_shot'] = input_df['passed_from_id'].notnull().astype(float)
    input_df['is_penalty_attempt'] = input_df['shot_type'].isin([13, 44]).astype(float)
    return input_df

def drop_own_goals(input_df):
    """only return shots that were not own goals"""
    input_df = input_df[input_df['shot_type'] != 10]
    return input_df.copy()

def goal_dummy(input_df):
    """creates dummy variable on whether a shot resulted in a goal or not"""
    input_df['is_goal'] = input_df.loc[:, 'shot_type'].isin([9, 11, 12, 13]).astype(int)
    return input_df

def minutes_played(subs_df, player_df):
    """input dataframe of subsitutions and players for each game and return 
    dataframe with player information + minutes played that game """
    player_df['minutes_played'] = (1 - player_df['substitute']) * 90
    for indx, row1 in subs_df.iterrows():
        player_off = row1['player_off']
        player_on = row1['player_on']
        minute = row1['time_of_event(min)']
        for indx, row2 in player_df.iterrows():
            if player_off == row2['player_id']:
                player_df.loc[indx, 'minutes_played'] = minute
            elif player_on == row2['player_id']:
                player_df.loc[indx, 'minutes_played'] = 90 - minute
    return player_df
    
def turn_into_dollar_value(value, exchange_rate):
    """input value (transfer_value(sterlings) in dataframe) and return dollar amount as float
    
    used as helper function to transfer_markt_cleaner
    """
    if 'm' in value:
        num_value = float(''.join(x for x in value if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']))
    elif 'k' in value:
        num_value = float(''.join(x for x in value if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])) / 1000
    else:
        return None
    return round((num_value * exchange_rate), 2)

def transfer_markt_cleaner(players):
    """input players from db.players.find() and return cleaned dataframe with club_brev and squad_num as floats, 
    transfer_value in USD and age
    
    parameters
    ----------
    players: output from mongodb db.players.find()

    returns
    ------------
    tm_player: dataframe of meta playerdata from transfermarkt

    """
    
    tm_club_brev = {'Squad Club Atlético Boca Juniors': 'BOC' , 'Squad Club Atlético Independiente': 'IND', 'Squad Club Atlético River Plate': 'RIV', 'Squad Racing Club': 'RAC',
       'Squad Club Atlético San Lorenzo de Almagro': 'SLO', 'Squad Club Atlético Lanús': 'LAN', 'Squad Club Atlético Vélez Sarsfield': 'VEL',
       'Squad Club Deportivo Godoy Cruz Antonio Tomba': 'GOD', 'Squad Club Atlético Colón': 'COL', 'Squad Club Social y Deportivo Defensa y Justicia': 'DEF',
       'Squad Club Atlético Rosario Central': 'ROS', 'Squad Club Atlético Talleres': 'TAL', 'Squad Club Atlético Unión (Santa Fe)': 'UNI',
       'Squad Club Estudiantes de La Plata': 'EST', 'Squad Club Atlético Huracán': 'HUR', 'Squad Asociación Atlética Argentinos Juniors': 'ARG',
       'Squad Club Atlético Banfield': 'BAN', 'Squad Club Atlético Belgrano': 'BEL', 'Squad Club Atlético Tigre': 'TIG', "Squad Club Atlético Newell's Old Boys": 'NOB',
       'Squad Club Atlético Tucumán': 'ATT', 'Squad Club de Gimnasia y Esgrima La Plata': 'GIM', 'Squad Club Atlético Aldosivi': 'ALD',
       'Squad Club Atlético San Martín (SJ)': 'SMS', 'Squad Club Atlético San Martín (Tucumán)': 'SMT', 'Squad Club Atlético Patronato de la Juventud Católica': 'PA'}
    
    master_list = []
    for player in players:
        master_list.append(player)
    tm_player = pd.DataFrame(master_list)
    tm_player.loc[tm_player.squad_num == '-', 'squad_num'] = None
    tm_player = tm_player.astype({'squad_num': float})
    tm_player['club_brev'] = tm_player['club'].map(tm_club_brev)
    tm_player['age'] = tm_player.birthday.str[-3:-1].astype(int)
    tm_player['transfer_value(USD)'] = tm_player['transfer_value(sterlings)'].apply(lambda x: turn_into_dollar_value(x, 1.27))

    return tm_player



