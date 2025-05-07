import pandas as pd
# import requests


def get_ticker_list():
    nasdaq_tickers = pd.read_csv('data/raw/nasdaq_tickers.txt', sep='|')
    nyse_tickers = pd.read_csv('data/raw/other_tickers.txt', sep='|')
    tickers_list = [nasdaq_tickers, nyse_tickers]
    return tickers_list


def clean_nasdaq_tickers(df):
    pass


def clean_nyse_tickers(df):
    # Removing test stocks and ETFs keeping 'N' (not etf or test stock)
    df = df[df['Test Issue'] == 'N']
    df = df[df['ETF'] == 'N']
    # Removing columns that aren't needed
    nyse_columns_to_drop = ['Exchange', 'CQS Symbol',
                            'ETF', 'Round Lot Size', 'Test Issue']
    df.drop(labels=nyse_columns_to_drop, axis=1, inplace=True)


def extract_tickers():
    pass
