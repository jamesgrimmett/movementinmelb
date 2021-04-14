import numpy as np
import pandas as pd
import datetime

def get_weekly_counts(df, weekday_distinct = True):
    """
    """
    df['WEEK'] = df.QT_INTERVAL_COUNT.dt.isocalendar().week
    df.loc[df.WEEK == 53, 'WEEK'] = 52
    df['YEAR'] = df.QT_INTERVAL_COUNT.dt.year
    if weekday_distinct == True:
        weekdays = [0,1,2,3,4]
        df['WEEKDAY'] = df.QT_INTERVAL_COUNT.dt.weekday.apply(lambda x: x in weekdays)
        df_wk = df.groupby(['YEAR','WEEK','WEEKDAY'], as_index = False)['QT_VOLUME_24HOUR'].mean()
    else:
        df_wk = df.groupby(['YEAR','WEEK'], as_index = False)['QT_VOLUME_24HOUR'].mean()
    
    return df_wk

def add_weekly_change(df_wk, weekday_distinct = True):
    """

    """
    for i, row in df_wk.iterrows():
        if weekday_distinct == False:
            ref_row = df_wk[(df_wk.WEEK == row['WEEK']) & (df_wk.YEAR == 2019)]
        else:
            ref_row = df_wk[(df_wk.WEEK == row['WEEK']) & (df_wk.YEAR == 2019) & (df_wk.WEEKDAY == row['WEEKDAY'])]
        if ref_row.empty:
            df_wk.loc[i,'CHANGE'] = np.nan 
        else:
            ref = float(ref_row.QT_VOLUME_24HOUR)
            df_wk.loc[i,'CHANGE'] = float((row['QT_VOLUME_24HOUR'] - ref) / ref * 100.0)

    return df_wk

def get_rolling_average(df, buffer = 7):
    """
    """

    for i, row in df.iterrows():
        if row.QT_INTERVAL_COUNT == datetime.date(year = 2020, month = 2, day = 29):
            ref_row = df[df.QT_INTERVAL_COUNT == row.QT_INTERVAL_COUNT.replace(year = 2019, day = 28)] 
        else:
            ref_row = df[df.QT_INTERVAL_COUNT == row.QT_INTERVAL_COUNT.replace(year = 2019)]
        if ref_row.empty:
            df.loc[i,'CHANGE'] = np.nan
        else:
            ref = float(ref_row.QT_VOLUME_24HOUR)
            df.loc[i,'CHANGE'] = float((row['QT_VOLUME_24HOUR'] - ref) / ref * 100.0)

    df_avg = pd.DataFrame(np.zeros((len(df) - buffer - 1, 2)), columns = ['DATE','CHANGE'])
    lower = int(np.floor(buffer / 2))
    upper = int(buffer - lower - 1)

    for i,row in df.iloc[lower:-upper].iterrows():
        dmin = row.QT_INTERVAL_COUNT - datetime.timedelta(days = lower)
        dmax = row.QT_INTERVAL_COUNT + datetime.timedelta(days = upper)
        
        avg = df[(df.QT_INTERVAL_COUNT >= dmin) & (df.QT_INTERVAL_COUNT <= dmax)].CHANGE.mean()
        df_avg.loc[i,'CHANGE'] = float(avg)
        df_avg.loc[i,'DATE'] = row.QT_INTERVAL_COUNT

    return df_avg

