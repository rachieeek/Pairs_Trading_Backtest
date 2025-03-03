
'''
module to plot time series data
'''


import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_time_series(data_a: pd.DataFrame, data_b: pd.DataFrame, title: str, xlabel: str, ylabel: str, save_path: str) -> None:
    """
    Plot the time series data for two assets
    :param data_a: the first asset's time series data
    :param data_b: the second asset's time series data
    :param title: the title of the plot
    :param xlabel: the x-axis label
    :param ylabel: the y-axis label
    :param save_path: the path to save the plot
    :return: None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data_a, label=data_a.columns[0], color='red')
    plt.plot(data_b, label=data_b.columns[0], color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.show()
