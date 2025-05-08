import pandas as pd
# import requests
from etl.transform.transform_tickers import clean_nyse_tickers
from etl.transform.transform_tickers import clean_nasdaq_tickers
from etl.transform.transform_tickers import join_tickers


def get_ticker_lists() -> list:
    nasdaq_tickers = pd.read_csv('data/raw/nasdaq_tickers.txt', sep='|')
    nyse_tickers = pd.read_csv('data/raw/other_tickers.txt', sep='|')
    tickers_list = [nasdaq_tickers, nyse_tickers]
    return tickers_list


def extract_tickers() -> pd.DataFrame:
    nasdaq_tickers = get_ticker_lists()[0]
    nyse_tickers = get_ticker_lists()[1]
    cleaned_nas_tickers = clean_nasdaq_tickers(nasdaq_tickers)
    cleaned_nyse_tickers = clean_nyse_tickers(nyse_tickers)
    all_tickers_clean = join_tickers(cleaned_nas_tickers, cleaned_nyse_tickers)
    return all_tickers_clean
