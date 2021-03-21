import json
import datetime
import os
from pathlib import Path
import h5py
import pandas as pd

root_dir = Path(os.getcwd())
data_dir = root_dir/Path('data')
vertical_dir = data_dir/Path('vertical')
vertical_fn = '40587108-e1a8-56ae-8c7f-1853f009b7c6.h5'

def make_analysis():
    statistics = {}
    f = h5py.File(vertical_dir/vertical_fn, 'r')
    height_profile = list(f['climbs']['0']['height_profile'])
    datetime.datetime.fromtimestamp(list(f['climbs']['0']['moves_LH'])[0][0])
    df_json_l = {}
    df_json_r = {}
    columns_l = ['start_time_lh','end_time_lh','duration_lh','hand_on_lh']
    columns_r = ['start_time_rh','end_time_rh','duration_rh','hand_on_rh']
    for col in columns_l:
        df_json_l[col] = []
    for col in columns_r:
        df_json_r[col] = []

    for lh_move in list(f['climbs']['0']['moves_LH']):
        df_json_l['start_time_lh'].append(datetime.datetime.fromtimestamp(lh_move[0]))
        df_json_l['end_time_lh'].append(datetime.datetime.fromtimestamp(lh_move[1]))
        df_json_l['duration_lh'].append(lh_move[2])
        df_json_l['hand_on_lh'].append(lh_move[3])

    for rh_move in list(f['climbs']['0']['moves_RH']):
        df_json_r['start_time_rh'].append(datetime.datetime.fromtimestamp(rh_move[0]))
        df_json_r['end_time_rh'].append(datetime.datetime.fromtimestamp(rh_move[1]))
        df_json_r['duration_rh'].append(rh_move[2])
        df_json_r['hand_on_rh'].append(rh_move[3])

    df_r = pd.DataFrame(df_json_r)
    df_r['start_time_min'] = df_r['start_time_rh'].map(lambda x:str(x.hour)+':'+str(x.minute))
    df_r_agg = df_r.groupby('start_time_min').agg({'duration_rh':['mean','count']}).reset_index()
    movement_duration_r_mean = df_r_agg[(   'duration_rh', 'mean')].mean()
    movement_per_minute_r = df_r_agg[(   'duration_rh', 'count')].mean()

    df_l = pd.DataFrame(df_json_l)
    df_l['start_time_min'] = df_l['start_time_lh'].map(lambda x:str(x.hour)+':'+str(x.minute))
    df_l_agg = df_l.groupby('start_time_min').agg({'duration_lh':['mean','count']}).reset_index()
    movement_duration_l_mean = df_l_agg[(   'duration_lh', 'mean')].mean()
    movement_per_minute_l = df_l_agg[(   'duration_lh', 'count')].mean()

    movement_per_minute_avg = (movement_per_minute_r+movement_per_minute_l)/2
    mean_movement_duration = (movement_duration_r_mean+movement_duration_l_mean)/2

    min_start_time = min(df_l['start_time_lh'][0],df_r['start_time_rh'][0])
    max_end_time = min(df_l['end_time_lh'][len(df_l)-1],df_r['end_time_rh'][len(df_r)-1])

    
    total_time_seconds = (max_end_time-min_start_time).seconds
    mean_height_meas_time = len(height_profile)/total_time_seconds
    max_index = height_profile.index(max(height_profile))
    height_diff = max(height_profile) - min(height_profile)
    mean_climbing_speed = round(height_diff/max_index*mean_height_meas_time,3)

    n_climbs = len(list(f['climbs'])) - 1

    statistics['mean_movement_duration'] = mean_movement_duration
    statistics['movement_per_minute_avg'] = movement_per_minute_avg
    statistics['mean_climbing_speed'] = mean_climbing_speed
    statistics['n_climbs'] = n_climbs
    statistics['overall_index'] = height_diff/mean_movement_duration + mean_climbing_speed
    statistics['overall_index_normalised'] = (statistics['overall_index']/4)*5
    return statistics

