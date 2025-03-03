
import os
import pandas as pd
from cointegration_tests import CointData, PairStatistics

from plotting_ts import plot_time_series

lookback_window_months = 6

def get_cointegrated_pairs():

    data_path = 'data'
    temp = ['Information Technology']

    # for industry in os.listdir(data_path):
    for industry in temp:
        if industry.endswith('.csv'):
            continue
        industry_path = os.path.join(data_path, industry)
        print(industry_path)
    
        if os.path.isdir(industry_path):
            close_prices_df = pd.DataFrame()
            
            for stock_file in os.listdir(industry_path):
                stock_data_path = os.path.join(industry_path, stock_file)

                if stock_data_path.endswith('.csv'):
                    stock_data = pd.read_csv(stock_data_path, parse_dates=True)

                    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                    last_date = stock_data['Date'].max()
                    lookback_date = last_date - pd.DateOffset(months=lookback_window_months)
                    stock_data = stock_data[stock_data['Date'] >= lookback_date]

                    if close_prices_df.empty or 'Date' not in close_prices_df.columns:
                        close_prices_df = stock_data[['Date', 'Close']].rename(columns={'Close': stock_file.split('.')[0]})
                    else:
                        close_prices_df = close_prices_df.merge(
                            stock_data[['Date', 'Close']].rename(columns={'Close': stock_file.split('.')[0]}),
                            on='Date',
                            how='outer')

            
            # create temp file to store the close prices
            if not os.path.exists('temp'):
                os.makedirs('temp', exist_ok=True)

            if os.path.exists(f'temp/{industry}_close_prices.csv'):
                os.remove(f'temp/{industry}_close_prices.csv')

            close_prices_df.to_csv(f'temp/{industry}_close_prices.csv')


            ## correlation 
            close_prices_no_date = close_prices_df.drop(columns=['Date'])
            industry_correlation = close_prices_no_date.corr()

    return close_prices_df, industry_correlation

def get_pairs(df):
    df_pairs = pd.DataFrame()
    for col in df.columns:
       list = []
       for row in df.index:
            list.append(row)
            if col != row and df.loc[row, col] > 0.9 and col not in list:
                df_pairs = df_pairs._append({'stock1': col, 'stock2': row}, ignore_index=True)
    return df_pairs
    

def cointegration_test(data_a, data_b, plot = False):

    ps = PairStatistics()

    coint_data_eg = ps.engle_granger_coint(data_a, data_b)
    coint_data_joh = ps.johansen_coint(data_a, data_b)
    
    if coint_data_eg.cointegrated and coint_data_joh.cointegrated:
        print(f"{data_a.columns[0]} & {data_b.columns[0]}:")
        print(f"E-G cointegrated: {coint_data_eg.confidence}, Johansen cointegrated: {coint_data_joh.confidence}")
        print(f"Weights: E-G: {coint_data_eg.weight}, Johansen: {coint_data_joh.weight}")

        if plot:
                # create png file
                if not os.path.exists('cointegrated_png'):
                    os.makedirs('cointegrated_png', exist_ok=True)
                if os.path.exists(f"/cointegrated_png/{data_a.columns[0]} & {data_b.columns[0]}.png"):
                    os.remove(f"/cointegrated_png/{data_a.columns[0]} & {data_b.columns[0]}.png")
                
                plot_time_series(
                data_a,
                data_b,
                f"{data_a.columns[0]} & {data_b.columns[0]}",
                'xlabel',
                'ylabel',
                f"/cointegrated_png/{data_a.columns[0]} & {data_b.columns[0]}.png"
            )
    return

def build_cointegration_matrix():
    #### build info 
    return


if __name__ == '__main__':
    close_prices_df, correlated_pairs_matrix = get_cointegrated_pairs()
    df_pairs = get_pairs(correlated_pairs_matrix)

    for _, pair in df_pairs.iterrows():
        cointegration_test(close_prices_df[[pair['stock1']]] , close_prices_df[[pair['stock2']]], plot = True)


