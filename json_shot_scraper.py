def flatten_shot(shot, game_id):
    """Flatten the schema of a shot record."""
    shot_id = shot[0]
    shot_data = shot[1]
    
    return {'game_id': game_id,
            'shot_id': shot_id,
            'shot_type': shot_data['type'],
            't_half': shot_data['t']['half'],
            't_min': shot_data['t']['m'],
            't_sec': shot_data['t']['s'],
            'time_of_event(min)': (shot_data['t']['m'] + (shot_data['t']['s'] / 60 )), 
            'team_id': shot_data['team'],
            'player_id': shot_data['plyrId'],
            'caught_by': shot_data.get('ctchBy', None),
            'coord_x1': shot_data['coord']['1']['x'],
            'coord_y1': shot_data['coord']['1']['y'],
            'coord_z1': shot_data['coord']['1']['z'],
            'coord_x2': shot_data['coord']['2']['x'],
            'coord_y2': shot_data['coord']['2']['y'],
            'coord_z2': shot_data['coord']['2']['z']}

def flatten_goal(goal, game_id):
    """Flatten the schema of a goal record."""
    goal_id = goal[0]
    goal_data = goal[1]

    return {'game_id': game_id,
            'goal_id': goal_id,
            'shot_type': goal_data['type'],
            'team_id': goal_data['team'],
            'player_id': goal_data['plyrId'],
            'assisted_by': goal_data.get('assBy', None),
            'coord_x1': goal_data['coord']['1']['x'],
            'coord_y1': goal_data['coord']['1']['y'],
            'coord_z1': goal_data['coord']['1']['z'],
            'coord_x2': goal_data['coord']['2']['x'],
            'coord_y2': goal_data['coord']['2']['y'],
            'coord_z2': goal_data['coord']['2']['z']}

def flatten_complete_pass(apass, game_id):
    """Flatten the schema of a completed pass."""
    pass_id = apass[0]
    pass_data = apass[1]

    return {'game_id': game_id,
            'pass_type': pass_data['type'],
            't_half': pass_data['t']['half'],
            't_min': pass_data['t']['m'],
            't_sec': pass_data['t']['s'],
            'time_of_event(min)': (pass_data['t']['m'] + (pass_data['t']['s'] / 60 )),
            'team_id': pass_data['team'],
            'rec_player': pass_data['recvId'],
            'pass_player': pass_data['plyrId'],
            'coord_x1': pass_data['coord']['1']['x'],
            'coord_y1': pass_data['coord']['1']['y'],
            'coord_z1': pass_data['coord']['1']['z'],
            'coord_x2': pass_data['coord']['2']['x'],
            'coord_y2': pass_data['coord']['2']['y'],
            'coord_z2': pass_data['coord']['2']['z'] }


def flatten_incomplete_pass(apass, game_id):
    """Flatten the schema of an incomplete pass."""
    pass_id = apass[0]
    pass_data = apass[1]

    return {'game_id': game_id,
            'pass_type': pass_data['type'],
            't_half': pass_data['t']['half'],
            't_min': pass_data['t']['m'],
            't_sec': pass_data['t']['s'],
            'time_of_event(min)': (pass_data['t']['m'] + (pass_data['t']['s'] / 60 )),
            'team_id': pass_data['team'],
            'pass_player': pass_data['plyrId'],
            'coord_x1': pass_data['coord']['1']['x'],
            'coord_y1': pass_data['coord']['1']['y'],
            'coord_z1': pass_data['coord']['1']['z'],
            'coord_x2': pass_data['coord']['2']['x'],
            'coord_y2': pass_data['coord']['2']['y'],
            'coord_z2': pass_data['coord']['2']['z'] }
