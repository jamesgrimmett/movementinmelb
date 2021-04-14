import matplotlib.pyplot as plt

from ..load_data import load
from . import process_pedestrian
from . import process_traffic

class Plot(object):
    def __init__(self):
        df_ped = load.load_pedestrian()
        df_trf = load.load_traffic()
        df_wk_ped = process_pedestrian.get_weekly_counts(df_ped)
        df_wk_ped = process_pedestrian.add_weekly_change(df_wk_ped)
        df_wk_trf = process_traffic.get_weekly_counts(df_trf)
        df_wk_trf = process_traffic.add_weekly_change(df_wk_trf)

        self.df_ped = df_ped
        self.df_trf = df_trf
        self.df_wk_ped = df_wk_ped
        self.df_wk_trf = df_wk_trf

    def plot_comparison(self):
        df_wk_ped = self.df_wk_ped
        df_wk_trf = self.df_wk_trf

        fig, ax = plt.subplots(ncols = 1, nrows = 1)
        ax.plot(df_wk_ped[df_wk_ped.weekday == True].change, color = 'red', label = 'weekday')
        ax.plot(df_wk_ped[df_wk_ped.weekday == False].change, color = 'red', ls = 'dashed', label = 'weekend')
        ax.plot(df_wk_trf[df_wk_trf.WEEKDAY == True].CHANGE, color = 'blue', label = 'weekday')
        ax.plot(df_wk_trf[df_wk_trf.WEEKDAY == False].CHANGE, color = 'blue', ls = 'dashed', label = 'weekend')
        ax.legend()

    def plot_comparison_rollingavg(self, buffer = 14):
        df_ped = self.df_ped
        df_trf = self.df_trf
        df_ped_avg = process_pedestrian.get_rolling_average(df_ped, buffer = buffer)
        df_trf_avg = process_traffic.get_rolling_average(df_trf, buffer = buffer)

        fig, ax = plt.subplots()
        ax.plot(df_trf_avg.CHANGE, label = 'traffic')
        ax.plot(df_ped_avg.change, label = 'pedestrians')