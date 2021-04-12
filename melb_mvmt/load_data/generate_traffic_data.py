import os
import glob
import pandas as pd
from .. import definitions

TRAFFIC_DATA_DIR = definitions.TRAFFIC_DATA_DIR

def generate():
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

    df = df.sort_values(by = 'QT_INTERVAL_COUNT')
    df.to_csv(os.path.join(TRAFFIC_DATA_DIR,'traffic_volume.csv'))

def load():
    file_path = os.path.join(TRAFFIC_DATA_DIR, 'traffic_volume.csv')
    if not os.path.isfile(file_path):
        generate()
    df = pd.read_csv(file_path)

    return df
