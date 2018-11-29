import pprint
import json
import pandas as pd
import numpy as np
from json_shot_scraper import flatten_shot, flatten_goal, flatten_complete_pass, flatten_incomplete_pass, flatten_corner
from  player_scraper import flatten_player, flatten_sub
from dataframe_cleaner import (pass_to_shot, corner_to_shot, transpose_coordinates, coord_to_yards, 
                               shot_distance_angle, dummy_columns, drop_own_goals, goal_dummy)
from html_scraper import db

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
       'goal'])
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
        master_df = pd.concat([attach_to_df, df], axis=0, ignore_index=True)
        attach_to_df = master_df.copy()
    return master_df[columns].copy()
