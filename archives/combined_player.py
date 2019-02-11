import pandas as pd
from mongo_to_db import create_master_player_min_df
from model_prep import player_minutes_total
from dataframe_cleaner import transfer_markt_cleaner

# def player_minutes_value(games, players):
#     columns = ['player_id', 'player_name', 'club', 'birthday', 'age', 'foot', 'position_id', 'squad_num',
#            'height', 'total_minutes_played', 'transfer_value(sterlings)', 'transfer_value(USD)']
    
#     players_minutes_df = create_master_player_min_df(games)
#     summed_player_min = player_minutes_total(players_minutes_df)
#     tm_df = transfer_markt_cleaner(players)
#     player_merge_df = pd.merge(summed_player_min, tm_df, on=['club_brev', 'squad_num'])
#     player_merge_df.drop(columns=['_id', 'club_brev'], inplace=True)

#     return player_merge_df[columns]



