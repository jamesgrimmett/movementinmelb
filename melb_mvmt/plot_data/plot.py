import matplotlib.pyplot as plt
import plotify # https://github.com/jamesgrimmett/plotify

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
        clrs = plotify.colours()
        ax.plot(df_wk_ped.date_time, df_wk_ped.change, color = clrs[0], label = 'pedestrian')
        ax.plot(df_wk_trf.DATE_TIME, df_wk_trf.CHANGE, color = clrs[1], label = 'vehicle')
        ax.legend()

        fig.suptitle('% change relative to same week in 2019', 
                        y = 0.95,
                        size = 12)
        plotify.hide_spines([ax])

    def plot_wkdayvswkend(self, data_type = 'pedestrian'):
        if data_type == 'pedestrian':
            df_wk = self.df_wk_ped
        elif data_type == 'vehicle':
            df_wk = self.df_wk_trf

        fig, ax = plt.subplots(ncols = 1, nrows = 1)
        clrs = plotify.colours()
        ax.plot(df_wk[df_wk.weekday == True].change, color = clrs[0], label = 'weekday')
        ax.plot(df_wk[df_wk.weekday == False].change, color = clrs[1], label = 'weekend')
        ax.legend()

        fig.suptitle('% change relative to same week in 2019', 
                        y = 0.95,
                        size = 12)
        plotify.hide_spines([ax])

    def plot_comparison_rollingavg(self, buffer = 7):
        df_ped = self.df_ped
        df_trf = self.df_trf
        df_ped_avg = process_pedestrian.get_rolling_average_change(df_ped, buffer = buffer)
        df_trf_avg = process_traffic.get_rolling_average_change(df_trf, buffer = buffer)

        fig, ax = plt.subplots()
        ax.plot(df_ped_avg.change, label = 'pedestrians')
        ax.plot(df_trf_avg.CHANGE, label = 'traffic')