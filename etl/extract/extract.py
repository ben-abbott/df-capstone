import pandas as pd
import requests
# from pathlib import Path
import os
from joblib import Memory
from etl.transform.transform_tickers import clean_nyse_tickers
from etl.transform.transform_tickers import clean_nasdaq_tickers
from etl.transform.transform_tickers import join_tickers
from etl.transform.transform import join_df

API_KEY = os.getenv("API_KEY")
NASDAQ_FILE_PATH = os.path.join(
    os.path.dirname(__file__), '../../data/raw/nasdaq_tickers.txt'
)
NYSE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), '../../data/raw/other_tickers.txt'
)


# Setup a local cache folder
# With ChatGPTs help:
memory = Memory(location='.api_cache', verbose=0)


def get_ticker_lists() -> list:
    nasdaq_tickers = pd.read_csv(NASDAQ_FILE_PATH, sep='|')
    nyse_tickers = pd.read_csv(NYSE_FILE_PATH, sep='|')
    tickers_list = [nasdaq_tickers, nyse_tickers]
    return tickers_list


def extract_tickers() -> pd.DataFrame:
    nasdaq_tickers = get_ticker_lists()[0]
    nyse_tickers = get_ticker_lists()[1]
    cleaned_nas_tickers = clean_nasdaq_tickers(nasdaq_tickers)
    cleaned_nyse_tickers = clean_nyse_tickers(nyse_tickers)
    all_tickers_clean = join_tickers(cleaned_nas_tickers, cleaned_nyse_tickers)
    return all_tickers_clean


# Get fundamental data for calculations
@memory.cache
def extract_from_balance_sheet(tickers):
    print('Calling balance sheet API...')
    balance_sheet_res = []
    for tick in tickers:
        url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{tick}?period=annual&apikey={API_KEY}'
        try:
            res = requests.get(url)
            data = res.json()
            if data:
                balance_sheet_res.append(data[0])
        except Exception as e:
            print(f'Error fetching {tick}: {e}')
    balance_sheet_df = pd.DataFrame(balance_sheet_res)
    balance_sheet_df = balance_sheet_df[['date',
                                        'symbol',
                                         'cashAndCashEquivalents',
                                         'propertyPlantEquipmentNet',
                                         'totalDebt']]
    print('Balance sheet data complete.')
    return balance_sheet_df

# Get stock info data for insights


@memory.cache
def extract_from_company_info(tickers):
    print('Calling company info API...')
    company_info_res = []
    for tick in tickers:
        url = f'https://financialmodelingprep.com/api/v3/profile/{tick}?apikey={API_KEY}'
        try:
            res = requests.get(url)
            data = res.json()
            if data:
                company_info_res.append(data[0])
        except Exception as e:
            print(f'Error fetching {tick}: {e}')
    company_info_df = pd.DataFrame(company_info_res)
    company_info_df = company_info_df[['symbol', 'price', 'mktCap', 'industry',
                                       'sector', 'image', 'ipoDate',
                                       'isActivelyTrading']]
    print('Completed company info.')
    return company_info_df


@memory.cache
def extract_from_financial_score(tickers):
    print('Calling financial score API...')
    score_res = []
    for tick in tickers:
        url = f'https://financialmodelingprep.com/api/v4/score?symbol={tick}&apikey={API_KEY}'
        try:
            res = requests.get(url)
            data = res.json()
            if data:
                score_res.append(data[0])
        except Exception as e:
            print(f'Error fetching {tick}: {e}')
    score_df = pd.DataFrame(score_res)
    score_df = score_df[['symbol', 'ebit', 'workingCapital']]
    print('Completed financial score.')
    return score_df


def extract_df(tickers):
    # calls all individual functions and returns list of data frames
    balance_sheet_df = extract_from_balance_sheet(tickers)
    company_info_df = extract_from_company_info(tickers)
    score_df = extract_from_financial_score(tickers)
    df_list = [balance_sheet_df, company_info_df, score_df]
    return df_list


def extract_data(ticker_df):
    tickers_list = ticker_df['symbol'].tolist()
    df_list = extract_df(tickers_list)
    df_list.append(ticker_df)
    all_data = join_df(df_list)
    return all_data
