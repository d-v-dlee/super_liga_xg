import pandas as pd
from dataframe_cleaner import shot_distance_angle
import matplotlib.pyplot as plt

def coord_maker(y_start, y_end, y_unit, x_start, x_end, x_unit):
    y_co = list(range(y_start, y_end + y_unit, y_unit))
    x_co = list(range(x_start, x_end + x_unit, x_unit))

    x_len = len(x_co)
    y_len = len(y_co)
    y_list = y_co * x_len

    x_list = []
    for num in x_co:
        x_list.extend([num for x in range(y_len)])
    return x_list, y_list 

def coord_table(y_start, y_end, y_unit, x_start, x_end, x_unit):
    """create x and y-coords for shot distances
    
    six_yard_shot = coord_table(-10, 10, 2, 2, 6, 2)
    eighteen_yard_shot = coord_table(-10, 10, 2, 8, 18, 2)
    beyond_eighteen_yard_shot = coord_table(-22, 22, 2, 20, 30, 2)
    left_six_yard_shot = coord_table(12, 22, 2, 3, 18, 3)
    right_six_yard_shot = coord_table(-12, -22, -2, 3, 18, 3)
    
    """
    x_list, y_list = coord_maker(y_start, y_end, y_unit, x_start, x_end, x_unit)
    return pd.DataFrame( {'shot_coord_x1': x_list, 'shot_coord_y1': y_list})

def distance_pred(df, player_id, assisted=0):
    df['assisted_shot'] = assisted
    df['is_penalty_attempt'] = 0
    df_2 = shot_distance_angle(df)
    df_final = df_2.drop(columns=['shot_coord_x1', 'shot_coord_y1'])
    df_final['player_id'] = player_id
    return df_final
    

def shot_probability_player(player_id):
    six_yard_shot = coord_table(-10, 10, 2, 2, 6, 2)
    eighteen_yard_shot = coord_table(-10, 10, 2, 8, 18, 2)
    beyond_eighteen_yard_shot = coord_table(-22, 22, 2, 20, 30, 2)
    left_six_yard_shot = coord_table(12, 22, 2, 3, 18, 3)
    right_six_yard_shot = coord_table(-12, -22, -2, 3, 18, 3)

    six = distance_pred(six_yard_shot, player_id)
    eighteen = distance_pred(eighteen_yard_shot, player_id)
    eighteen_plus = distance_pred(beyond_eighteen_yard_shot, player_id)
    left_box = distance_pred(left_six_yard_shot, player_id)
    right_box = distance_pred(right_six_yard_shot, player_id)

    return six, eighteen, eighteen_plus, left_box, right_box


