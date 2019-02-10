from sklearn.ensemble import  RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
import numpy as np
import pandas as pd

class ExpectedGoal():
    def __init__(self, rf, xgb, gb, df, param=None):
        self.param = param
        self.rf_model = rf
        self.xgb_model =  xgb
        self.gb_model = gb
        self.df = df
        self.model_probs = []
        self.ensemble_df = df.copy()
        self.xa_df = df.copy()

    def predict_prob(self):
        """
        predict the probability of any shot being a goal with three different models + ensemble average
        append and save as self.model_probs
        """
        columns = ['shot_distance', 'shot_angle', 'assisted_shot']
        predict_df = self.df[columns]
        p_random_forest = self.rf_model.predict_proba(predict_df)
        p_gradient_boost =  self.gb_model.predict_proba(predict_df)
        p_xgboost = self.xgb_model.predict_proba(predict_df)
        p_ensemble = (p_random_forest + p_gradient_boost + p_xgboost) / 3
        self.model_probs.extend([p_random_forest, p_gradient_boost, p_xgboost, p_ensemble])
        # return self.model_probs

    def xg_ensemble(self):
        """
        return a df with xG and xA added to dataframe
        """
        p_ensemble = self.model_probs[3]
        # ensemble_df = self.df.copy()
        self.ensemble_df['xG'] = p_ensemble[:, 1]
        self.ensemble_df['xA'] = self.ensemble_df['assisted_shot'] * self.ensemble_df['xG']

        self.xa_df = self.ensemble_df.loc[:, ['xA', 'passed_from_id']].copy()
        self.ensemble_df.drop(['xA', 'passed_from_id'], axis=1, inplace=True)
        return self.ensemble_df, self.xa_df
    
    def create_summed_xa(self):
        unique_players = self.ensemble_df['player_id'].unique()
        contributions = []
        for player in unique_players:
            xasum = round(self.xa_df[self.xa_df['passed_from_id'] == player]['xA'].sum(), 2)
            contributions.append([player, xasum])
        assist_df = pd.DataFrame(contributions, columns=['player_id', 'total_xA'])
        return assist_df
    
    def create_summed_xg(self):
        """
        input
        ------
        model_df: the dataframe with predicted proba of respective model

        returns
        ---------
        contribution_df: dataframe grouped by unique player_id with summed up xG and xA
        """
        unique_players = self.ensemble_df['player_id'].unique()
        contributions = []
        for player in unique_players:
            xgsum = round(self.ensemble_df[self.ensemble_df['player_id'] == player]['xG'].sum(), 2)
            goals = self.ensemble_df[self.ensemble_df['player_id'] == player]['is_goal'].sum()
            contributions.append([player, xgsum, goals])
        by_xG = sorted(contributions, key=lambda x: x[1], reverse=True)
        contribution_df = pd.DataFrame(by_xG, columns=['player_id', 'total_xG', 'goals'])
        return contribution_df
    
    def xg_and_xa(self):
        xa_sum = self.create_summed_xa()
        xg_sum = self.create_summed_xg()

        df = pd.merge(xa_sum, xg_sum, on=['player_id'])
        df['total_xG+xA'] = df.loc[:, 'total_xG'] + df.loc[:, 'total_xA']
        return df[['player_id', 'total_xG', 'goals', 'total_xA', 'total_xG+xA']].sort_values('goals', ascending=False)