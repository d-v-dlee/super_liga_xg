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
            'player_id': float(shot_data['plyrId']),
            'caught_by': shot_data.get('ctchBy', None),
            'shot_coord_x1': shot_data['coord']['1']['x'],
            'shot_coord_y1': shot_data['coord']['1']['y'],
            'shot_coord_z1': shot_data['coord']['1']['z'],
            'shot_coord_x2': shot_data['coord']['2']['x'],
            'shot_coord_y2': shot_data['coord']['2']['y'],
            'shot_coord_z2': shot_data['coord']['2']['z']}

def flatten_goal(goal, game_id):
    """Flatten the schema of a goal record."""
    goal_id = goal[0]
    goal_data = goal[1]

    return {'game_id': game_id,
            'goal_id': goal_id,
            'shot_type': goal_data['type'],
            'team_id': goal_data['team'],
            'player_id': float(goal_data['plyrId']),
            'assisted_by': goal_data.get('assBy', None),
            'shot_coord_x1': goal_data['coord']['1']['x'],
            'shot_coord_y1': goal_data['coord']['1']['y'],
            'shot_coord_z1': goal_data['coord']['1']['z'],
            'shot_coord_x2': goal_data['coord']['2']['x'],
            'shot_coord_y2': goal_data['coord']['2']['y'],
            'shot_coord_z2': goal_data['coord']['2']['z']}

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
            'rec_player': float(pass_data['recvId']),
            'pass_player': float(pass_data['plyrId']),
            'pass_coord_x1': pass_data['coord']['1']['x'],
            'pass_coord_y1': pass_data['coord']['1']['y'],
            'pass_coord_z1': pass_data['coord']['1']['z'],
            'pass_coord_x2': pass_data['coord']['2']['x'],
            'pass_coord_y2': pass_data['coord']['2']['y'],
            'pass_coord_z2': pass_data['coord']['2']['z'] }


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
            'pass_player': float(pass_data['plyrId']),
            'inc_coord_x1': pass_data['coord']['1']['x'],
            'inc_coord_y1': pass_data['coord']['1']['y'],
            'inc_coord_z1': pass_data['coord']['1']['z'],
            'inc_coord_x2': pass_data['coord']['2']['x'],
            'inc_coord_y2': pass_data['coord']['2']['y'],
            'inc_coord_z2': pass_data['coord']['2']['z'] }

