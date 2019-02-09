import pandas as pd
from xlg import game_to_single_df, create_frame


class ConvertData():
    def __init__(self, param=None):
        self.param = param
    
    def games_to_df(self, games):
        """
        This function calls upon 'create_frame' and 'game_to_cleaned_df' functions above.

        Parameters
        -----------------
        games: games are json data from mongodb by db.games.find

        Returns
        -----------------
        final_df: a dataframe with shots as rows; columns include 'shot_distance',
        'shot_angle', 'assisted_shot', 'is_penalty_attempt', 'is_goal'
        
        """
        columns = ['game_id', 'player_id', 'shot_coord_x1', 'shot_coord_x2',
        'shot_coord_y1', 'shot_coord_y2', 'shot_coord_z1', 'shot_coord_z2',
        'shot_id', 'shot_type', 'team_id', 'time_of_event(min)',
        'passed_from_id', 'pass_coord_x1', 'pass_coord_x2', 'pass_coord_y1',
        'pass_coord_y2', 'pass_coord_z1', 'pass_coord_z2', 'corner_kick',
        'shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt',
        'is_goal']
        attach_to_df = create_frame()
        for game in games:
            df = game_to_single_df(game)
            final_df = pd.concat([attach_to_df, df], axis=0, ignore_index=True, sort=True)
            ### may get a warning because a game doesn't have corner_kick values ###
            attach_to_df = final_df[columns].copy()
        return final_df[columns].copy()
    
    def drop_penalties(self, df):
        """
        
        Parameters
        -----------
        df: dataframe of shot data from games_to_df function

        Returns
        ----------------
        df_no_pen: dataframe of shot data without penalties
        """
        df_no_pen = df[df['is_penalty_attempt'] == 0].copy()
        return df_no_pen
    
    def create_rf_prep(self, df):
        """
        Parameters
        -----------
        df: dataframe of shot data 

        Returns
        ----------------
        df[rf_columns]: dataframe of only features that model will predict on
        
        """
        rf_columns = ['shot_distance', 'shot_angle', 'assisted_shot']
        return df[rf_columns].astype(float)
