def flatten_player(player, game_id):
    """Flatten the schema of a player"""
    player_id = player[0]
    player_data = player[1]

    return {'game_id': game_id,
            'player_id': int(player_id),
            'team_id': player_data['teamId'],
            'position_id': player_data['posnId'],
            'name': player_data['name']['shortName'],
            'squad_number': player_data['squadNo']}
    