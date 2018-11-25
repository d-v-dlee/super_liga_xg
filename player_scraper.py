def flatten_player(player, game_id):
    """Flatten the schema of a player"""
    player_id = player[0]
    player_data = player[1]

    return {'game_id': game_id,
            'player_id': int(player_id),
            'team_id': player_data['teamId'],
            'position_id': player_data['posnId'],
            'substitute': player_data['substitute'],
            'name': player_data['name']['shortName'],
            'squad_number': player_data['squadNo']}
    
def flatten_sub(sub, game_id):
    """Flatten the schema of a sub"""
    sub_id = sub[0]
    sub_data = sub[1]

    return {'game_id': game_id,
            'sub_id': sub_id,
            'sub_type': sub_data['type'],
            'time_of_event(min)': (sub_data['t']['m'] + (sub_data['t']['s'] / 60 )),
            'team_id': sub_data['team'],
            'player_off': sub_data['offId'],
            'player_on': sub_data['inId']
            }