'''
functions to plot time series data 
'''

import matplotlib.pyplot as plt
import pandas as pd
import os

from typing import List, Tuple
from cointegration_tests import CointData

def plot_time_series(data_a,
                     data_b, 
                     title: str, 
                     xlabel: str, 
                     ylabel: str, 
                     save_path: bool = False) -> None:
    """
    Plot the time series data for two assets
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data_a, label=data_a.columns[0], color='red')
    plt.plot(data_b, label=data_b.columns[0], color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if save_path:
        output_dir = "plots/cointegrated_png"
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, f"{data_a.columns[0]}_{data_b.columns[0]}.png")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        plt.savefig(file_path)
    # plt.show()


def plot_time_series_differenced(coint_data: CointData,
                                close_prices_df: pd.DataFrame,
                                title: str, 
                                xlabel: str, 
                                ylabel: str, 
                                save_path: bool = False) -> None:
    """
    Plot the time series data for two assets
    :param data_a: the first asset's time series data
    :param data_b: the second asset's time series data
    :param close_prices_df: the close prices data
    :param title: the title of the plot
    :param xlabel: the x-axis label
    :param ylabel: the y-axis label
    :param save_path: the path to save the plot
    :return: None
    """

    asset_a = coint_data.asset_a
    asset_b = coint_data.asset_b
    print(coint_data.weight)

    asset_a_data_differenced = close_prices_df[[asset_a]].diff().dropna()
    asset_b_data_differenced = close_prices_df[[asset_b]].diff().dropna()

    plt.figure(figsize=(10, 6))
    plt.plot(asset_b_data_differenced * coint_data.weight, label=asset_b, color='red')
    plt.plot(asset_a_data_differenced, label=asset_a, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if save_path:
        output_dir = "plots/cointegrated_normalized_png"
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, f"{asset_a}_{asset_b}_normalized.png")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        plt.savefig(file_path)
    # plt.show()


def plot_time_series_sum(coint_data: CointData,
                                close_prices_df: pd.DataFrame,
                                title: str, 
                                xlabel: str, 
                                ylabel: str, 
                                save_path: bool = False) -> None:
    
    asset_a = coint_data.asset_a 
    asset_b = coint_data.asset_b 

    plt.figure(figsize=(10, 6))
    plt.plot(close_prices_df[asset_a]- close_prices_df[asset_b] * coint_data.weight , label='Sum', color='green')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if save_path:
        output_dir = "plots/cointegrated_sum_png"
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, f"{asset_a}_{asset_b}_sum.png")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        plt.savefig(file_path)
