import pandas as pd
import requests


def get_ticker_list():
    nasdaq_tickers = pd.read_csv('data/raw/nasdaq_tickers.txt', sep='|')
    other_tickers = pd.read_csv('data/raw/other_tickers.txt', sep='|')
    return (len(nasdaq_tickers) + len(other_tickers))
