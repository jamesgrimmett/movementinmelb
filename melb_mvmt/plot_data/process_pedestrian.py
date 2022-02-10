import numpy as np
import pandas as pd
import datetime

def get_weekly_counts(df, weekday_distinct = False):
    """
    """
    #df = df.groupby(['year','week','sensor_id','sensor_name'], as_index = False).hourly_counts.sum()
    df.loc[(df.week == 53) & (df.month == 1), 'week'] = 1
    df.loc[(df.week == 53) & (df.month == 12), 'week'] = 52
    
    if weekday_distinct == True:
        weekdays = [1,2,3,4,5]
        df['weekday'] = df.date_time.dt.weekday.apply(lambda x: x in weekdays)
        df_wk = df.groupby(['year','week','weekday'], as_index = False)['hourly_counts'].mean()
    else:
        df_wk = df.groupby(['year','week'], as_index = False)['hourly_counts'].mean()
    
    df_wk['date_time'] = df_wk.apply(lambda x: datetime.datetime.strptime(f"{int(x['year'])}-{int(x['week'])}-{1}","%Y-%W-%w"), axis = 1)
    return df_wk

def add_weekly_change(df_wk, weekday_distinct = False):
    """

    """
    for i, row in df_wk.iterrows():
        if weekday_distinct == False:
            ref_row = df_wk[(df_wk.week == row['week']) & (df_wk.year == 2019)]
        else:
            ref_row = df_wk[(df_wk.week == row['week']) & (df_wk.year == 2019) & (df_wk.weekday == row['weekday'])]
        if ref_row.empty:
            df_wk.loc[i,'change'] = np.nan 
        else:
            ref = float(ref_row.hourly_counts)
            df_wk.loc[i,'change'] = float((row['hourly_counts'] - ref) / ref * 100.0)

    return df_wk

#def get_rolling_average_change(df, buffer = 7):
#    """
#    """
#    df = df.copy(deep = True)
#    df = df.groupby(['year','month','day','mdate'], as_index = False).hourly_counts.mean()
#    df['date_time'] = df.apply(lambda x: datetime.date(year = x['year'], month = x['month'], day = x['mdate']), axis = 1)
#    df = df.sort_values(by = 'date_time', ignore_index = True)
#
#    df_avg = pd.DataFrame(np.zeros((len(df) - buffer - 1, 2)), columns = ['date','change'])
#    lower = int(np.floor(buffer / 2))
#    upper = int(buffer - lower - 1)
#
#    for i,row in df.iloc[lower:-upper].iterrows():
#        if row.date_time == datetime.date(year = 2020, month = 2, day = 29):
#            dmin0 = row.date_time.replace(year = 2019, day = 28) - datetime.timedelta(days = lower)
#            dmax0 = row.date_time.replace(year = 2019, day = 28) + datetime.timedelta(days = upper)
#        else:
#            dmin0 = row.date_time.replace(year = 2019) - datetime.timedelta(days = lower)
#            dmax0 = row.date_time.replace(year = 2019) + datetime.timedelta(days = upper)
#        dmin1 = row.date_time - datetime.timedelta(days = lower)
#        dmax1 = row.date_time + datetime.timedelta(days = upper)
#        
#        avg0 = df[(df.date_time >= dmin0) & (df.date_time <= dmax0)].hourly_counts.mean()
#        avg1 = df[(df.date_time >= dmin1) & (df.date_time <= dmax1)].hourly_counts.mean()
#        df_avg.loc[i,'change'] = float((avg1 - avg0) / avg0) * 100.0
#        df_avg.loc[i,'date'] = row.date_time
#
#    return df_avg