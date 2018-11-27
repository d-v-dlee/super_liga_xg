import pandas as pd

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
            shot_df.loc[indx, 'pass_coord_yz'] = possible_pass_df.iloc[0, :]['pass_coord_z1']
            shot_df.loc[indx, 'pass_coord_y2'] = possible_pass_df.iloc[0, :]['pass_coord_z2']
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
            shot_df.loc[indx, 'pass_coord_yz'] = possible_corner_df.iloc[0, :]['ck_coord_z1']
            shot_df.loc[indx, 'pass_coord_y2'] = possible_corner_df.iloc[0, :]['ck_coord_z2']
            shot_df.loc[indx, 'corner_kick'] = 1 
    return shot_df

def transpose_coordinates(input_df, inplace=True):
    """takes a dataframe and transposes all points on one side so that
    all events occur on one side of the grid"""
    if inplace==False:
        df = input_df.copy()
    else:
        df = input_df
    df.loc[df['shot_coord_x1']< 0, ['shot_coord_x1', 'shot_coord_x2', 'shot_coord_y1', 'shot_coord_y2',
                 'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1', 'pass_coord_y2'] ] *= -1
    return df

    # pos_df = df.loc[df['shot_coord_x1']>= 0, :]
    # neg_df = df.loc[df['shot_coord_x1'] < 0, :].copy()
    # neg_df.loc[:,['shot_coord_x1', 'shot_coord_x2', 'shot_coord_y1', 'shot_coord_y2',
    #             'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1', 'pass_coord_y2']] *= -1
    # transposed_shot_df = pd.concat([neg_df, pos_df], axis=0)
    # return transposed_shot_df
