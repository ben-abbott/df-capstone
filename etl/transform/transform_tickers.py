import pandas as pd


def clean_nasdaq_tickers(df) -> pd.DataFrame:
    # Clean nasdaq ticker data
    df = df[df['Test Issue'] == 'N']
    df = df[df['ETF'] == 'N']
    df = df[df['NextShares'] == 'N']
    df['Exchange'] = 'NASDAQ'
    # Still 1 missing ticker symbol after exploring dataset in ipynb
    # after googling, found the symbol is NA for this company, no other stock
    # has that ticker so will replace the null with NA
    df['Symbol'] = df['Symbol'].fillna('NA')
    # lose unneeded columns
    nasdaq_columns_to_drop = ['Market Category', 'Test Issue',
                              'Financial Status', 'Round Lot Size',
                              'ETF', 'NextShares']
    df.drop(labels=nasdaq_columns_to_drop, axis=1, inplace=True)
    # make the ticker the index and rename to Ticker
    df.rename(columns={'Symbol': 'symbol'}, inplace=True)
    df.set_index('symbol')
    return df


def clean_nyse_tickers(df) -> pd.DataFrame:
    exchange_map = {
        'A': 'AMEX',
        'N': 'NYSE',
        'P': 'ARCA',
        'V': 'IEX',
        'Z': 'BATS'
    }
    # Removing test stocks and ETFs keeping 'N' (not etf or test stock)
    df = df[df['Test Issue'] == 'N']
    df = df[df['ETF'] == 'N']
    # Replace single letter with string of exchange
    df['Exchange'] = df['Exchange'].map(exchange_map)
    # Removing columns that aren't needed
    nyse_columns_to_drop = ['CQS Symbol',
                            'ETF', 'Round Lot Size',
                            'Test Issue', 'NASDAQ Symbol']
    df.drop(labels=nyse_columns_to_drop, axis=1, inplace=True)
    # rename symbol to ticker and make it index
    df.rename(columns={'ACT Symbol': 'symbol'}, inplace=True)
    df.set_index('symbol')
    return df

# check if any tickers exist in both dataframes, they don't in this
# example but could implement this in the future to handle duplicates

# def check_for_duplicates_between_df(df1, df2) -> bool:
#     pass


def join_tickers(df1, df2):
    all_tickers = pd.concat([df1, df2])
    return all_tickers.sort_values(by='symbol', ascending=True)
