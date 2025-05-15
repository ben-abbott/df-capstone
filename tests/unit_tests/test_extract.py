import pandas as pd
from unittest.mock import patch, Mock
from etl.extract.extract import get_ticker_lists, extract_tickers, extract_from_balance_sheet, extract_from_company_info, extract_from_financial_score


def test_get_ticker_lists():
    test_nasdaq = pd.DataFrame({
        'symbol': ['AAPL', 'MSFT'],
        'exchange': ['NASDAQ', 'NASDAQ']
    })

    test_nyse = pd.DataFrame({
        'symbol': ['IBM', 'GE'],
        'exchange': ['NYSE', 'NYSE']
    })

    with patch('etl.extract.extract.pd.read_csv', side_effect=[test_nasdaq, test_nyse]):
        result = get_ticker_lists()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].equals(test_nasdaq)
    assert result[1].equals(test_nyse)


def test_extract_tickers():
    test_nasdaq = pd.DataFrame({'symbol': ['AAPL'], 'exchange': ['NASDAQ']})
    test_nyse = pd.DataFrame({'symbol': ['IBM'], 'exchange': ['NYSE']})

    cleaned_nasdaq = pd.DataFrame({'symbol': ['AAPL'], 'exchange': ['NASDAQ']})
    cleaned_nyse = pd.DataFrame({'symbol': ['IBM'], 'exchange': ['NYSE']})

    joined = pd.concat([cleaned_nasdaq, cleaned_nyse], ignore_index=True)

    with patch('etl.extract.extract.get_ticker_lists', return_value=[test_nasdaq, test_nyse]), \
            patch('etl.extract.extract.clean_nasdaq_tickers', return_value=cleaned_nasdaq), \
            patch('etl.extract.extract.clean_nyse_tickers', return_value=cleaned_nyse), \
            patch('etl.extract.extract.join_tickers', return_value=joined):

        result = extract_tickers()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'symbol' in result.columns
    assert set(result['symbol']) == {'AAPL', 'IBM'}


@patch('etl.extract.extract.requests.get')
def test_extract_from_balance_sheet(mock_get):
    test_res = [{
        'date': '2023-12-31',
        'symbol': 'AAPL',
        'cashAndCashEquivalents': 50000,
        'propertyPlantEquipmentNet': 100000,
        'totalDebt': 25000
    }]

    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = test_res

    tickers = ['AAPL']
    df = extract_from_balance_sheet(tickers)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert all(col in df.columns for col in [
        'date', 'symbol', 'cashAndCashEquivalents',
        'propertyPlantEquipmentNet', 'totalDebt'
    ])
    assert df.iloc[0]['symbol'] == 'AAPL'
    assert df.iloc[0]['cashAndCashEquivalents'] == 50000


@patch('etl.extract.extract.requests.get')
def test_extract_from_company_info(mock_get):
    test_res = [{
        'symbol': 'AAPL',
        'price': 150.0,
        'mktCap': 2500000000000,
        'industry': 'Consumer Electronics',
        'sector': 'Technology',
        'image': '',
        'ipoDate': '1980-12-12',
        'isActivelyTrading': True
    }]

    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = test_res

    tickers = ['AAPL']
    df = extract_from_company_info(tickers)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    expected_columns = [
        'symbol', 'price', 'mktCap', 'industry', 'sector',
        'image', 'ipoDate', 'isActivelyTrading'
    ]
    assert all(col in df.columns for col in expected_columns)
    assert df.iloc[0]['symbol'] == 'AAPL'
    assert df.iloc[0]['price'] == 150.0


@patch('etl.extract.extract.requests.get')
def test_extract_from_financial_score(mock_get):
    test_res = [{
        'symbol': 'AAPL',
        'ebit': 80000000000,
        'workingCapital': 60000000000
    }]

    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = test_res

    tickers = ['AAPL']
    df = extract_from_financial_score(tickers)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    expected_columns = ['symbol', 'ebit', 'workingCapital']
    assert all(col in df.columns for col in expected_columns)
    assert df.iloc[0]['symbol'] == 'AAPL'
    assert df.iloc[0]['ebit'] == 80000000000
    assert df.iloc[0]['workingCapital'] == 60000000000
