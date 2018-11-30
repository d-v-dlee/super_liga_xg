import pandas as pd

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
    x_list, y_list = coord_maker(y_start, y_end, y_unit, x_start, x_end, x_unit)
    return pd.DataFrame( {'shot_coord_x1': x_list, 'shot_coord_y1': y_list})

