import sys
sys.path.insert(0, '/Users/david/galvanize/super_liga_xg')
from combined_player import player_minutes_value
from scraping_tools.html_scraper import db
# from html_scraper import db
from mongo_to_db import create_master_df
from model_prep import create_rf_prep, create_xG_df, create_summed_xG_df
import pickle
import pandas as pd

def create_complete_xg_tables():
    """creates complete table of player information + xG statistics based on 
    random_forest, gradient_boost, xgb_boost and ensemble as four dataframes
    
    example: rf_df, gb_df, xgb_df, ens_df = create_complete_xg_tables()
    """

    games = db['games_update'].find()
    players = db.players.find()

    final_df = player_minutes_value(games, players)

    final_df['position_id'] = final_df['position_id'].replace(1, 'Goalie')
    final_df['position_id'] = final_df['position_id'].replace(2, 'Defender')
    final_df['position_id'] = final_df['position_id'].replace(3, 'Midfielder')
    final_df['position_id'] = final_df['position_id'].replace(4, 'Forward')
    final_df['position_id'] = final_df['position_id'].replace(5, 'Defender')

    games = db['games_update'].find()
    shots_df = create_master_df(games)

    rf_model = pickle.load(open("../models/rfc.pkl", "rb"))
    gb_model = pickle.load(open("../models/gb.pkl", "rb"))
    xgb_model = pickle.load(open("../models/xgb.pkl", "rb"))

    model_ready_df = create_rf_prep(shots_df)
    columns = ['shot_distance', 'shot_angle', 'assisted_shot', 'is_penalty_attempt']

    p_random_forest = rf_model.predict_proba(model_ready_df[columns])
    p_gradient_boost =  gb_model.predict_proba(model_ready_df[columns])
    p_xgboost = xgb_model.predict_proba(model_ready_df[columns])
    p_ensemble = (p_random_forest + p_gradient_boost + p_xgboost) / 3

    rf_xg = create_xG_df(model_ready_df, shots_df['is_goal'], p_random_forest)
    rf_contributions = create_summed_xG_df(rf_xg)

    gb_xg = create_xG_df(model_ready_df, shots_df['is_goal'], p_gradient_boost)
    gb_contributions = create_summed_xG_df(gb_xg)

    xgb_xg = create_xG_df(model_ready_df, shots_df['is_goal'], p_xgboost)
    xgb_contributions = create_summed_xG_df(xgb_xg)

    ensemble_xg = create_xG_df(model_ready_df, shots_df['is_goal'], p_ensemble)
    ensemble_contributions = create_summed_xG_df(ensemble_xg)

    rf_sl = pd.merge(rf_contributions, final_df, on=['player_id'])
    gb_sl = pd.merge(gb_contributions, final_df, on=['player_id'])
    xgb_sl = pd.merge(xgb_contributions, final_df, on=['player_id'])
    ens_sl = pd.merge(ensemble_contributions, final_df, on=['player_id'])

    rf_sl['xG+xA/90'] = round(rf_sl['total_xG+xA'] / (rf_sl['total_minutes_played'] / 90 ), 2)
    gb_sl['xG+xA/90'] = round(gb_sl['total_xG+xA'] / (gb_sl['total_minutes_played'] / 90 ), 2)
    xgb_sl['xG+xA/90'] = round(xgb_sl['total_xG+xA'] / (xgb_sl['total_minutes_played'] / 90 ), 2)
    ens_sl['xG+xA/90'] = round(ens_sl['total_xG+xA'] / (ens_sl['total_minutes_played'] / 90 ), 2)

    rf_sl['xG_goal_diff'] = round(rf_sl['goals'] - (rf_sl['total_xG']), 2)
    gb_sl['xG_goal_diff'] = round(gb_sl['goals'] - (gb_sl['total_xG']), 2)
    xgb_sl['xG_goal_diff'] = round(xgb_sl['goals'] - (xgb_sl['total_xG']), 2)
    ens_sl['xG_goal_diff'] = round(ens_sl['goals'] - (ens_sl['total_xG']), 2)

    rf_sl['total_minutes_played'] = round(rf_sl['total_minutes_played'], 2)
    gb_sl['total_minutes_played'] = round(gb_sl['total_minutes_played'], 2)
    xgb_sl['total_minutes_played'] = round(xgb_sl['total_minutes_played'], 2)
    ens_sl['total_minutes_played'] = round(ens_sl['total_minutes_played'], 2)

    final_col = ['player_id', 'player_name', 'club', 'birthday', 'age', 'foot', 'position_id', 'squad_num',
       'total_xG', 'pen_attempts', 'total_xA', 'total_xG+xA', 'goals', 'xG_goal_diff', 'xG+xA/90', 'transfer_value(USD)', 'total_minutes_played']

    rf_df = rf_sl[final_col]
    gb_df = gb_sl[final_col]
    xgb_df = xgb_sl[final_col]
    ens_df = ens_sl[final_col]

    return rf_df, gb_df, xgb_df, ens_df