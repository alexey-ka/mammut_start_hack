import json
import os
from pathlib import Path
import h5py

root_dir = Path(os.getcwd())
data_dir = root_dir/Path('data')
vertical_dir = data_dir/Path('vertical')
vertical_fn = '40587108-e1a8-56ae-8c7f-1853f009b7c6.json'


with open(str(vertical_dir/Path(vertical_fn)), 'r') as data_file:
    df_json = json.load(data_file)
    print(df_json['data']['start_time'])

