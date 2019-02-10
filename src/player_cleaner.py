from dataframe_cleaner import transfer_markt_cleaner
from mongo_to_db import afa_player_dict
import pandas as pd

class PlayerDataframeCreator():
    def __init__(self, games, players):
        self.games = games
        self.players = players
        self.player_df = None
    def create_player_df(self):
        tm_df = transfer_markt_cleaner(self.players)
        player_dict = afa_player_dict(self.games)
        afa_df = pd.DataFrame(data = [item[1] for item in player_dict.items()])

        afa_team_dict = {20: 'VEL', 13: 'NOB', 136: 'TIG', 19: 'SLO', 8: 'GIM', 2: 'ARG',
        137: 'UNI', 122: 'ALD', 869: 'PA', 6: 'COL', 124: 'BEL', 134: 'SMS',
        5: 'BOC', 135: 'TAL', 132: 'GOD', 7: 'EST', 12: 'LAN', 129: 'DEF',
        18: 'ROS', 4: 'BAN', 100: 'HUR', 17: 'RIV', 815: 'ATT', 16: 'RAC', 10: 'IND',
        490: 'SMT'}

        pos_dict = {1: 'Goalie', 2: 'Defender', 3: 'Midfielder', 4: 'Forward', 5: 'Manager/NA'}

        afa_df['club_brev'] = afa_df['team_id'].map(afa_team_dict)
        afa_df['position'] = afa_df['position_id'].map(pos_dict)


        self.player_df = pd.merge(afa_df, tm_df, on=['club_brev', 'squad_num'])
        self.player_df.drop(columns=['_id', 'club_brev', 'player', 'transfer_value(sterlings)', 'position_id'], inplace=True)

        return self.player_df
    

class FinalDataframe():
    def __init__(self, player_df, total_df):
        """
        inputs
        -------------
        player_df: dataframe of player information emerge between transfer markt and afa
        total_df: dataframe of xG, xA etc for each player_id

        """
        self.player_df = player_df
        self.total_df = total_df
        self.final_df = None
        self.final_sub_df = None
    
    def final_df_creator(self):
        self.final_df = pd.merge(self.player_df, self.total_df, on=['player_id'])
        self.final_sub_df = self.final_df[['name', 'position', 'minutes_played', 'age', 'transfer_value(USD)', 'goals', 'total_xG', 'total_xA', 'total_xG+xA']].sort_values('goals', ascending=False).copy()
        return self.final_sub_df
    
    def additional_stats(self):
        alt_df = self.final_sub_df.copy()
        alt_df['xG+xA/90'] = round(alt_df.loc[:, 'total_xG+xA'] / alt_df.loc[:, 'minutes_played'] * 90, 2)
        alt_df['Goals v. Expected'] = alt_df.loc[:, 'goals'] - alt_df.loc[:, 'total_xG']
        return alt_df

 
    

        

    
    