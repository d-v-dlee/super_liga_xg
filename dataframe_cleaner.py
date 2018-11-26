def shot_to_pass(shot_df, pass_df, time_elapsed=.16667):
    """
    Links shots to previous passes to 
    try to link assists based on time between pass and shot
    ----------
    shot_df: shot_df of a game
    pass_df: completed_pass_df of a game
    time: fraction of a minute between pass and shot, default 10 seconds (.16667 for 1/6)
    
    Returns
    -------
    shots_df with new column 'passed_from_id' and 'pass_id'
    """
    for indx, row in shot_df.iterrows():
        shooter_id = row['player_id']
        shoot_time = row['time_of_event(min)']
        possible_pass_df =  pass_df[(pass_df['rec_player']== shooter_id) & (pass_df['time_of_event(min)'] < shoot_time) & (pass_df['time_of_event(min)'] > shoot_time - time_elapsed)]
        if len(possible_pass_df) == 0:
            shot_df.loc[indx, 'passed_from_id'] = None
        elif len(possible_pass_df) > 1:
            shot_df.loc[indx, 'passed_from_id'] = possible_pass_df.iloc[-1, :]['pass_player']   
        else:
            shot_df.loc[indx, 'passed_from_id'] = possible_pass_df.iloc[0, :]['pass_player']
    return shot_df
    