import numpy as np

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