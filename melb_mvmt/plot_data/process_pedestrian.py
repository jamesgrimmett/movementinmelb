import numpy as np

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