import os
import glob
import pandas as pd
import requests
from .. import definitions

TRAFFIC_DATA_DIR = definitions.TRAFFIC_DATA_DIR
PEDESTRIAN_DATA_DIR = definitions.PEDESTRIAN_DATA_DIR

def generate_traffic():
    """
    Use this function to create the road traffic dataframe.
    The raw data is too large to store in the repository.
    1. Download the Traffic Signal Volume Data from:
        https://discover.data.vic.gov.au/dataset/traffic-signal-volume-data
    2. Unzip the files and place them in ../../data/traffic/raw
    3. Make adjustments if needed and execute this program.
    """
    files = glob.glob(os.path.join(TRAFFIC_DATA_DIR,'raw/*/*'))
    if len(files) == 0:
        raise ValueError(f"No files found in {os.path.join(TRAFFIC_DATA_DIR,'raw')}.\n\
        Download them from https://discover.data.vic.gov.au/dataset/traffic-signal-volume-data")

    df = pd.DataFrame()

    for i,f in enumerate(files):
        print(f'Processed {i+1} / {len(files)}')
        df_ = pd.read_csv(f)
        # Keep only the counts from Melbourne City
        df_ = df_[df_.NM_REGION.isin(['MC1','MC2','MC3'])]
        df_['QT_INTERVAL_COUNT'] = pd.to_datetime(df_.QT_INTERVAL_COUNT)
        # Store the mean count
        df_ = df_[df_.QT_VOLUME_24HOUR >= 0]
        if len(df_) > 0:
            # Find the total 24 hour volume through each site
            df_ = df_.groupby(['QT_INTERVAL_COUNT','NB_SCATS_SITE'],as_index = False)[['QT_VOLUME_24HOUR']].sum()
            # Find the median 24 hour volume of all sites
            df_ = df_.groupby('QT_INTERVAL_COUNT',as_index=False)['QT_VOLUME_24HOUR'].median()
            df = df.append(df_, ignore_index = True)

    df = df.sort_values(by = 'QT_INTERVAL_COUNT', ignore_index = True)
    df.to_csv(os.path.join(TRAFFIC_DATA_DIR,'traffic_volume.csv'))

def load_traffic():
    file_path = os.path.join(TRAFFIC_DATA_DIR, 'traffic_volume.csv')
    if not os.path.isfile(file_path):
        generate_traffic()
    df = pd.read_csv(file_path)
    df['QT_INTERVAL_COUNT'] = pd.to_datetime(df.QT_INTERVAL_COUNT)

    return df

def generate_pedestrian():
    url = 'https://data.melbourne.vic.gov.au/resource/b2ak-trbp.json?$where=year%3E2018'
    #sensor_ids_pt = [
    #                5,  # Princes Bridge
    #                6,  # Flinders Street Station Underpass
    #                13, # Flagstaff Station
    #                22, # Flinders St-Elizabeth St (East)
    #                24, # Spencer St-Collins St (North)
    #                40, # Lonsdale St-Spring St (West)
    #                57, # Bourke St Bridge
    #                58, # Bourke St - Spencer St (North)
    #                62, # La Trobe St (North)
    #]
    #url = url + '%20AND%20(sensor_id=' + '%20OR%20sensor_id='.join([str(id) for id in sensor_ids_pt]) + ')'

    params = {'$limit' : 10000000}
    response = requests.get(url, params)

    if not response.ok:
        raise ValueError(f"API request failed.\n{request.json()['message']}")

    df = pd.DataFrame(response.json())
    df['sensor_id'] = df.sensor_id.astype(int)
    df['date_time'] = pd.to_datetime(df.date_time)
    df['year'] = df.year.astype(int)
    df['hourly_counts'] = df.hourly_counts.astype(int)
    df['week'] = df.date_time.dt.isocalendar().week

    df.to_csv(os.path.join(PEDESTRIAN_DATA_DIR,'pedestrian_volume.csv'))

def load_pedestrian():
    file_path = os.path.join(PEDESTRIAN_DATA_DIR, 'pedestrian_volume.csv')
    if not os.path.isfile(file_path):
        print('Pedestrian data not found. Downloading new data.')
        generate_pedestrian()
    df = pd.read_csv(file_path)
    df['date_time'] = pd.to_datetime(df.date_time)

    return df


    