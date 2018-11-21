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
            'team_id': shot_data['team'],
            'player_id': shot_data['plyrId'],
            'caught_by': shot_data.get('ctchBy', None),
            'coord_x1': shot_data['coord']['1']['x'],
            'coord_y1': shot_data['coord']['1']['y'],
            'coord_z1': shot_data['coord']['1']['z'],
            'coord_x2': shot_data['coord']['2']['x'],
            'coord_y2': shot_data['coord']['2']['y'],
            'coord_z2': shot_data['coord']['2']['z']}