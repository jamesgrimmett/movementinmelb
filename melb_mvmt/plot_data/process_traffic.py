import numpy as np
import pandas as pd
import datetime

def get_weekly_counts(df, weekday_distinct = False):
    """
    """
    df['WEEK'] = df.QT_INTERVAL_COUNT.dt.isocalendar().week
    df['MONTH'] = df.QT_INTERVAL_COUNT.dt.month
    df.loc[(df.WEEK == 53) & (df.MONTH == 1), 'WEEK'] = 1
    df.loc[(df.WEEK == 53) & (df.MONTH == 12), 'WEEK'] = 52
    df['YEAR'] = df.QT_INTERVAL_COUNT.dt.year
    if weekday_distinct == True:
        weekdays = [1,2,3,4,5]
        df['WEEKDAY'] = df.QT_INTERVAL_COUNT.dt.weekday.apply(lambda x: x in weekdays)
        df_wk = df.groupby(['YEAR','WEEK','WEEKDAY'], as_index = False)['QT_VOLUME_24HOUR'].mean()
    else:
        df_wk = df.groupby(['YEAR','WEEK'], as_index = False)['QT_VOLUME_24HOUR'].mean()
    
    df_wk['DATE_TIME'] = df_wk.apply(lambda x: datetime.datetime.strptime(f"{int(x['YEAR'])}-{int(x['WEEK'])}-{1}","%Y-%W-%w"), axis = 1)
    return df_wk

def add_weekly_change(df_wk, weekday_distinct = False):
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

#def get_rolling_average_change(df, buffer = 7):
#    df_avg = pd.DataFrame(np.zeros((len(df) - buffer - 1, 2)), columns = ['DATE','CHANGE'])
#    lower = int(np.floor(buffer / 2))
#    upper = int(buffer - lower - 1)
#
#    for i,row in df.iloc[lower:-upper].iterrows():
#        if row.QT_INTERVAL_COUNT == datetime.date(year = 2020, month = 2, day = 29):
#            dmin0 = row.QT_INTERVAL_COUNT.replace(year = 2019, day = 28) - datetime.timedelta(days = lower)
#            dmax0 = row.QT_INTERVAL_COUNT.replace(year = 2019, day = 28) + datetime.timedelta(days = upper)
#        else:
#            dmin0 = row.QT_INTERVAL_COUNT.replace(year = 2019) - datetime.timedelta(days = lower)
#            dmax0 = row.QT_INTERVAL_COUNT.replace(year = 2019) + datetime.timedelta(days = upper)
#
#        avg0 = df[(df.QT_INTERVAL_COUNT >= dmin0) & (df.QT_INTERVAL_COUNT <= dmax0)].QT_VOLUME_24HOUR.mean()
#        dmin1 = row.QT_INTERVAL_COUNT - datetime.timedelta(days = lower)
#        dmax1 = row.QT_INTERVAL_COUNT + datetime.timedelta(days = upper)
#        avg1 = df[(df.QT_INTERVAL_COUNT >= dmin1) & (df.QT_INTERVAL_COUNT <= dmax1)].QT_VOLUME_24HOUR.mean()
#
#        df_avg.loc[i,'CHANGE'] = float((avg1 - avg0) / avg0) * 100.0
#        df_avg.loc[i,'DATE'] = row.QT_INTERVAL_COUNT
#
#    return df_avg


