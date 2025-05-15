import pandas as pd
from etl.transform.transform import join_df, calculate_enterprise_value, calculate_yield, calculate_return, clean_data
from etl.transform.transform_tickers import clean_nasdaq_tickers, clean_nyse_tickers


def test_join_df_success():
    df1 = pd.DataFrame({'symbol': ['AAPL', 'MSFT'], 'val1': [1, 2]})
    df2 = pd.DataFrame({'symbol': ['AAPL', 'GOOG'], 'val2': [3, 4]})
    df3 = pd.DataFrame({'symbol': ['AAPL', 'TSLA'], 'val3': [5, 6]})
    df4 = pd.DataFrame({'symbol': ['AAPL', 'MSFT'], 'val4': [7, 8]})

    result = join_df([df1, df2, df3, df4])

    assert result.shape[0] == 2
    assert 'val1' in result.columns
    assert 'val4' in result.columns
    assert 'GOOG' not in result['symbol'].values


def test_calculate_enterprise_value():
    test_data = {
        'mktCap': [1000, 2000],
        'totalDebt': [500, 100],
        'cashAndCashEquivalents': [200, 50]
    }
    df = pd.DataFrame(test_data)

    result_df = calculate_enterprise_value(df)

    expected = [1300, 2050]
    assert 'enterpriseValue' in result_df.columns
    assert result_df['enterpriseValue'].tolist() == expected


def test_calculate_yield():
    test_data = {
        'ebit': [100, 200],
        'enterpriseValue': [1000, 400]
    }
    df = pd.DataFrame(test_data)

    result_df = calculate_yield(df)

    expected = [(100/1000)*100, (200/400)*100]
    assert 'earningsYield' in result_df.columns
    assert result_df['earningsYield'].tolist() == expected


def test_calculate_return():
    test_data = {
        'ebit': [100, 200],
        'propertyPlantEquipmentNet': [400, 300],
        'workingCapital': [100, 100]
    }
    df = pd.DataFrame(test_data)

    result_df = calculate_return(df)

    expected = [
        (100 / (400 + 100)) * 100,
        (200 / (300 + 100)) * 100
    ]

    assert 'returnOnCapital' in result_df.columns
    assert result_df['returnOnCapital'].tolist() == expected


def test_clean_data():
    test_data = {
        'symbol': ['AAPL', 'GOOGL', None],
        'cashAndCashEquivalents': [1000, 0, 200],
        'propertyPlantEquipmentNet': [300, 500, 0],
        'totalDebt': [200, 300, 400],
        'isActivelyTrading': [1, 1, 0],
        'workingCapital': [100, 200, 0],
        'enterpriseValue': [10000, 20000, 0],
        'industry': ['Tech', None, 'Retail'],
        'sector': [None, 'Technology', 'Retail'],
        'ipoDate': ['1980-12-12', '2004-08-19', None]
    }
    df = pd.DataFrame(test_data)

    cleaned_df = clean_data(df)

    assert cleaned_df.shape[0] == 1
    assert 'NA' not in cleaned_df['symbol'].values
    assert 'Not Available' not in cleaned_df['industry'].values
    assert cleaned_df['sector'].iloc[0] == 'Not Available'
    assert 'ipoDate' not in cleaned_df.columns


def test_clean_nasdaq_tickers():
    test_data = {
        'Symbol': ['AAPL', None, 'GOOG'],
        'Test Issue': ['N', 'Y', 'N'],
        'ETF': ['N', 'N', 'Y'],
        'NextShares': ['N', 'N', 'N'],
        'Market Category': ['Q', 'Q', 'Q'],
        'Financial Status': ['N', 'N', 'N'],
        'Round Lot Size': [100, 100, 100]
    }
    df = pd.DataFrame(test_data)
    cleaned_df = clean_nasdaq_tickers(df)

    assert 'AAPL' in cleaned_df.index
    assert 'GOOG' not in cleaned_df.index
    assert all(cleaned_df['Exchange'] == 'NASDAQ')
    for col in ['Test Issue', 'ETF', 'NextShares', 'Market Category', 'Financial Status', 'Round Lot Size']:
        assert col not in cleaned_df.columns


def test_clean_nyse_tickers():
    test_data = {
        'ACT Symbol': ['IBM', 'TSLA', 'FAKE'],
        'Test Issue': ['N', 'Y', 'N'],
        'ETF': ['N', 'N', 'Y'],
        'Exchange': ['N', 'A', 'P'],
        'CQS Symbol': ['IBM', 'TSLA', 'FAKE'],
        'Round Lot Size': [100, 100, 100],
        'NASDAQ Symbol': ['IBM', 'TSLA', 'FAKE']
    }
    df = pd.DataFrame(test_data)

    cleaned_df = clean_nyse_tickers(df)

    assert 'IBM' in cleaned_df.index
    assert 'TSLA' not in cleaned_df.index
    assert 'FAKE' not in cleaned_df.index
    assert cleaned_df.loc['IBM', 'Exchange'] == 'NYSE'
    for col in ['CQS Symbol', 'ETF', 'Round Lot Size', 'Test Issue', 'NASDAQ Symbol']:
        assert col not in cleaned_df.columns
    assert cleaned_df.index.name == 'symbol'
