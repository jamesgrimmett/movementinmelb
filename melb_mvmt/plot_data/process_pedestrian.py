import numpy as np
import pandas as pd
import datetime

def get_weekly_counts(df, weekday_distinct = True):
    """
    """
    #df = df.groupby(['year','week','sensor_id','sensor_name'], as_index = False).hourly_counts.sum()
    df.loc[df.week == 53, 'week'] = 52
    if weekday_distinct == True:
        weekdays = [0,1,2,3,4]
        df['weekday'] = df.date_time.dt.weekday.apply(lambda x: x in weekdays)
        df_wk = df.groupby(['year','week','weekday'], as_index = False)['hourly_counts'].mean()
    else:
        df_wk = df.groupby(['year','week'], as_index = False)['hourly_counts'].mean()
    
    return df_wk

def add_weekly_change(df_wk, weekday_distinct = True):
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

def get_rolling_average(df, buffer = 7):
    """
    """
    df = df.copy(deep = True)
    month_str = {'January'  : 1,
                'February'  : 2,
                'March'     : 3,
                'April'     : 4,
                'May'       : 5,
                'June'      : 6,
                'July'      : 7,
                'August'    : 8,
                'September' : 9,
                'October'   : 10,
                'November'  : 11,
                'December'  : 12}
    df['month'] = df.month.map(month_str)
    df = df.groupby(['year','month','day','mdate'], as_index = False).hourly_counts.sum()
    df['date_time'] = df.apply(lambda x: datetime.date(year = x['year'], month = x['month'], day = x['mdate']), axis = 1)
    df = df.sort_values(by = 'date_time', ignore_index = True)

    for i, row in df.iterrows():
        if row.date_time == datetime.date(year = 2020, month = 2, day = 29):
            ref_row = df[df.date_time == row.date_time.replace(year = 2019, day = 28)] 
        else:
            ref_row = df[df.date_time == row.date_time.replace(year = 2019)]
        if ref_row.empty:
            df.loc[i,'change'] = np.nan
        else:
            ref = float(ref_row.hourly_counts)
            df.loc[i,'change'] = float((row['hourly_counts'] - ref) / ref * 100.0)

    df_avg = pd.DataFrame(np.zeros((len(df) - buffer - 1, 2)), columns = ['date','change'])
    lower = int(np.floor(buffer / 2))
    upper = int(buffer - lower - 1)

    for i,row in df.iloc[lower:-upper].iterrows():
        dmin = row.date_time - datetime.timedelta(days = lower)
        dmax = row.date_time + datetime.timedelta(days = upper)
        
        avg = df[(df.date_time >= dmin) & (df.date_time <= dmax)].change.mean()
        df_avg.loc[i,'change'] = float(avg)
        df_avg.loc[i,'date'] = row.date_time

    return df_avg