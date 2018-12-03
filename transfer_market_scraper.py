import string 


def flatten_player_info(key, row):
    """Flatten the schema of a players information from transfermarkt."""
    if key != '_id':
        player_name = key
    if row[key]['squad_num'] == '-':
        squad_number = 3.14
    else:
        squad_number = float(row[key]['squad_num'])
    
        return {'name': player_name,
                'club': string.capwords(row[key]['club'].replace('-', ' ')),
                'squad_number': squad_number,
                'age': row[key]['birthday'][-3:-1],
                'dob': row[key]['birthday'][:-5],
                'transfer_value(sterlings)': row[key]['transfer_value(sterlings)']}
            


        
