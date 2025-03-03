from datetime import datetime
from concurrent import futures

import pandas as pd
from pandas import DataFrame
import yfinance as yf
import os

lookback_years = 1

def download_stock(stock, industry):
    """Try to query Yahoo Finance for stock data, handling exceptions."""
    try:
        print(f"Downloading data for: {stock}")
        
        if stock == 'BRK.B':
            stock = 'BRK-B'
        elif stock == 'BF.B':
            stock = 'BF-B'
        
        stock_df = yf.download(stock, start=start_time, end=now_time, interval = '1d')
        
        if stock_df.empty:
            raise ValueError(f"No data found for {stock}")
        stock_df.columns = stock_df.columns.get_level_values(0)

        stock_df['Ticker'] = stock
        stock_df['Industry'] = industry 

        output_name = f"{stock}.csv"

        if not os.path.exists('data'):
            os.makedirs('data', exist_ok=True)

        if not os.path.exists(f'data/{industry}'):
            os.makedirs(f'data/{industry}', exist_ok=True)

        if os.path.exists(f'data/{industry}/{output_name}'): # overwrite prev file
            os.remove(f'data/{industry}/{output_name}')    
        stock_df.to_csv(f'data/{industry}/{output_name}')
    
    except Exception as e:

        print(f"Failed to download data for {stock}: {e}")
        
def download_stock_special(stock, start_time, end_time):
    """Try to query Yahoo Finance for stock data, handling exceptions."""
    try:
        print(f"Downloading data for: {stock}")
        
        if stock == 'BRK.B':
            stock = 'BRK-B'
        elif stock == 'BF.B':
            stock = 'BF-B'
        
        stock_df = yf.download(stock, start=start_time, end=now_time, interval = '1d')
        
        if stock_df.empty:
            raise ValueError(f"No data found for {stock}")
        
        stock_df['Ticker'] = stock
        output_name = f"{stock}.csv"
        
        if not os.path.exists('data'):
            os.makedirs('data', exist_ok=True)
        
        stock_df.to_csv(f'data/{output_name}')
    
    except Exception as e:

        print(f"Failed to download data for {stock}: {e}")

def concat_dfs(data_path='data'):
    """Concatenate all CSV files in the data directory into a single DataFrame."""
    all_data = []
    
    for file in os.listdir(data_path):
        df = pd.read_csv(f'{data_path}/{file}')
        all_data.append(df)
    
    return pd.concat(all_data)

if __name__ == '__main__':

    """ set the download window """
    now_time = datetime.now()
    start_time = datetime(now_time.year - lookback_years, now_time.month , now_time.day)
    
    """ list of s&p companies """

    tickers = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
     
    
    list = tickers.Symbol.to_list()
    
    industry = tickers['GICS Sector'].to_list()
    
    dict = {list[i]: industry[i] for i in range(len(list))}



    # filter dict to only include companies in the Information Technology sector
    dict_temp = {k: v for k, v in dict.items() if v == 'Information Technology'}

    for stock, industry in dict_temp.items():
        download_stock(stock, industry)

    # for stock, industry in dict.items():
    #     download_stock(stock, industry)
          
    # Concatenate all data into a single DataFrame
    # all_data = concat_dfs()
    # all_data.to_csv('all_data_modified.csv', index=False)

    # spy = ['^GSPC']
    # print("Downloading data for S&P 500")
    # download_stock_special(spy[0], datetime(now_time.year - lookback_years, now_time.month , now_time.day), now_time)

    #timing:
    finish_time = datetime.now()
    duration = finish_time - now_time
    minutes, seconds = divmod(duration.seconds, 60)
    print('getSandP_threaded.py')
    print(f'The threaded script took {minutes} minutes and {seconds} seconds to run.')
    #The threaded script took 0 minutes and 31 seconds to run.