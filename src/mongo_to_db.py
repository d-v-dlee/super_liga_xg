import pprint
import json
import pandas as pd
import numpy as np
from json_shot_scraper import flatten_shot, flatten_goal, flatten_complete_pass, flatten_incomplete_pass, flatten_corner
from  player_scraper import flatten_player, flatten_sub
from dataframe_cleaner import (pass_to_shot, corner_to_shot, transpose_coordinates, coord_to_yards, 
                               shot_distance_angle, dummy_columns, drop_own_goals, goal_dummy, minutes_played)
# from ..scraping_tools.html_scraper import db

def game_to_cleaned_df(game):
    """input game pulled from mongoDB 'db' and run through cleaning functions
    output: pandas dataframe"""
    shots = list(game['incidences']['shots'].items())
    game_id = game['match']['matchId']
    shot_list_dicts = [flatten_shot(shot, game_id) for shot in shots]
    shot_df = pd.DataFrame(shot_list_dicts)
    
    completed_passes = list(game['incidences']['correctPasses'].items())
    completed_list_dicts = [flatten_complete_pass(apass, game_id) for apass in completed_passes]
    completed_passes_df = pd.DataFrame(completed_list_dicts)

    shot_pass_df = pass_to_shot(shot_df, completed_passes_df)

    corners = list(game['incidences']['cornerKicks'].items())
    if len(corners) > 0:
        corner_dicts = [flatten_corner(kick, game_id) for kick in corners]
        corner_df = pd.DataFrame(corner_dicts)

        shot_pass_corner = corner_to_shot(shot_pass_df, corner_df)
        transposed_df = transpose_coordinates(shot_pass_corner)
    else:
        transposed_df = transpose_coordinates(shot_pass_df)

    yard_df = coord_to_yards(transposed_df)

    shot_distance_df = shot_distance_angle(yard_df)

    df = dummy_columns(shot_distance_df)
    df_no_own = drop_own_goals(df)
    df_final = goal_dummy(df_no_own)
    return df_final

def create_frame():
    """create dataframe to concat new dataframes to"""
    attach_to_df = pd.DataFrame(columns=['game_id', 'player_id', 'shot_coord_x1', 'shot_coord_x2',
       'shot_coord_y1', 'shot_coord_y2', 'shot_coord_z1', 'shot_coord_z2',
       'shot_id', 'shot_type', 'team_id', 'time_of_event(min)',
       'passed_from_id', 'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1',
       'pass_coord_y2', 'pass_coord_z1', 'pass_coord_z2', 'corner_kick',
       'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt',
       'is_goal'])
    return attach_to_df


def create_master_df(games):
    """input games from mongodb by db.games.find() and return a cleaned dataframe
    """
    columns = ['game_id', 'player_id', 'shot_coord_x1', 'shot_coord_x2',
       'shot_coord_y1', 'shot_coord_y2', 'shot_coord_z1', 'shot_coord_z2',
       'shot_id', 'shot_type', 'team_id', 'time_of_event(min)',
       'passed_from_id', 'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1',
       'pass_coord_y2', 'pass_coord_z1', 'pass_coord_z2', 'corner_kick',
       'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt',
       'is_goal']
    attach_to_df = create_frame()
    for game in games:
        df = game_to_cleaned_df(game)
        final_df = pd.concat([attach_to_df, df], axis=0, ignore_index=True, sort=True)
        ### may get a warning because a game doesn't have corner_kick values ###
        attach_to_df = final_df[columns].copy()
    return final_df[columns].copy()

###below is for players

def game_to_player_df(game):
    """input game from db and output pandas dataframe with plaer information + minutes played"""
    game_id = game['match']['matchId']
    
    players = list(game['players'].items())
    player_list_dicts = [flatten_player(player, game_id) for player in players]
    player_df = pd.DataFrame(player_list_dicts)

    subs = list(game['incidences']['substitutions'].items())
    subs_dicts = [flatten_sub(sub, game_id) for sub in subs]
    subs_df = pd.DataFrame(subs_dicts)

    minutes_player_df = minutes_played(subs_df, player_df)
    return minutes_player_df


def afa_player_dict(games):
    """
    turns game from mongodb into pd --> back into dictionary
    
    parameters
    ----------------
    game: a game from mongodb

    returns:
    dictionary of player_info and total_minutes player
    """
    player_dict = {}
    for game in games:
        temp_df = game_to_player_df(game)
        for player in temp_df['player_id'].unique():
            if player not in player_dict:
                player_dict[player] = {'name': temp_df[temp_df['player_id'] == player]['name'].values[0] , 'position_id':  temp_df[temp_df['player_id'] == player]['position_id'].values[0],
                                        'squad_num':  temp_df[temp_df['player_id'] == player]['squad_number'].values[0], 'team_id':  temp_df[temp_df['player_id'] == player]['team_id'].values[0],
                                        'minutes_played':  temp_df[temp_df['player_id'] == player]['minutes_played'].values[0], 'player_id': temp_df[temp_df['player_id'] == player]['player_id'].values[0] }
            else:
                player_dict[player]['minutes_played'] += temp_df.loc[temp_df['player_id']==player, 'minutes_played'].values[0]
    return player_dict

def create_player_min_frame():
    """return a dataframe to concat to for player_sub_information"""
    attach_to_df = pd.DataFrame(columns = ['game_id', 'name', 'player_id', 'position_id', 'squad_number',
       'substitute', 'team_id', 'minutes_played'])
    return attach_to_df

def create_master_player_min_df(games):
    """input games from mongodb by db.games.find() and return a cleaned dataframe with club
    abbreviation instead of club_id"""
    
    columns = ['game_id', 'name', 'player_id', 'position_id', 'squad_number',
       'substitute', 'team_id', 'minutes_played']
    
    afa_team_dict = {20: 'VEL', 13: 'NOB', 136: 'TIG', 19: 'SLO', 8: 'GIM', 2: 'ARG',
    137: 'UNI', 122: 'ALD', 869: 'PA', 6: 'COL', 124: 'BEL', 134: 'SMS',
    5: 'BOC', 135: 'TAL', 132: 'GOD', 7: 'EST', 12: 'LAN', 129: 'DEF',
    18: 'ROS', 4: 'BAN', 100: 'HUR', 17: 'RIV', 815: 'ATT', 16: 'RAC', 10: 'IND',
    490: 'SMT'}

    attach_df = create_player_min_frame()
    for game in games:
        df = game_to_player_df(game)
        merged_df = pd.concat([attach_df, df], axis=0, ignore_index=True)
        attach_df = merged_df.copy()
    
    merged_df['club_brev'] = merged_df['team_id'].map(afa_team_dict)

    return merged_df

