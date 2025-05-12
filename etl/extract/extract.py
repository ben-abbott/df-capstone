import pandas as pd
import requests
# from pathlib import Path
import os
from etl.transform.transform_tickers import clean_nyse_tickers
from etl.transform.transform_tickers import clean_nasdaq_tickers
from etl.transform.transform_tickers import join_tickers

API_KEY = 'b95993f82e2d0048935cfd947df28088'
NASDAQ_FILE_PATH = os.path.join(
    os.path.dirname(__file__), '../../data/raw/nasdaq_tickers.txt'
)
NYSE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), '../../data/raw/other_tickers.txt'
)

# NASDAQ_FILE_PATH = 'data/raw/nasdaq_tickers.txt'
# NYSE_FILE_PATH = 'data/raw/other_tickers.txt'


def get_ticker_lists() -> list:
    nasdaq_tickers = pd.read_csv(NASDAQ_FILE_PATH, sep='|')
    nyse_tickers = pd.read_csv(NYSE_FILE_PATH, sep='|')
    tickers_list = [nasdaq_tickers, nyse_tickers]
    return tickers_list


def extract_tickers():
    nasdaq_tickers = get_ticker_lists()[0]
    nyse_tickers = get_ticker_lists()[1]
    cleaned_nas_tickers = clean_nasdaq_tickers(nasdaq_tickers)
    cleaned_nyse_tickers = clean_nyse_tickers(nyse_tickers)
    all_tickers_clean = join_tickers(cleaned_nas_tickers, cleaned_nyse_tickers)
    return all_tickers_clean


# Get fundamental data for calculations

def extract_from_balance_sheet(tickers):
    pass

# Get stock info data for insights


def extract_from_company_info(tickers):
    pass


def extract_from_financial_score(tickers):
    pass
