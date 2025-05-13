# import pandas as pd


def join_df(df_list):
    if len(df_list) == 4:
        all_data = df_list[0].merge(df_list[1], on='symbol', how='outer')
        all_data = all_data.merge(df_list[2], on='symbol', how='outer')
        all_data = all_data.merge(df_list[3], on='symbol', how='inner')
    else:
        print('''The number of DataFrames to be 
              joined is not 3, can only join 3 DataFrames''')
    return all_data


def calculate_enterprise_value(df):
    df['enterpriseValue'] = df['mktCap'] + \
        df['totalDebt'] - df['cashAndCashEquivalents']
    return df


def calculate_yield(df):
    df['earningsYield'] = (df['ebit'] / df['enterpriseValue']) * 100
    return df


def calculate_return(df):
    df['returnOnCapital'] = (
        df['ebit'] / (df['propertyPlantEquipmentNet'] + df['workingCapital'])) * 100
    return df


def calculate_rank_fields(df):
    df['rocRank'] = df['returnOnCapital'].rank(ascending=False, method='min')
    df['yieldRank'] = df['earningsYield'].rank(ascending=False, method='min')
    df['rankSum'] = df['rocRank'] + df['yieldRank']
    df['overallRank'] = df['rankSum'].rank(ascending=True, method='min')
    # df['overallRank'] = df['overallRank'].apply(np.int64)
    df.sort_values(by='overallRank', ascending=True, inplace=True)
    return df


def clean_data(df):
    cols_to_clean = ['cashAndCashEquivalents',
                     'propertyPlantEquipmentNet',
                     'totalDebt', 'isActivelyTrading',
                     'workingCapital', 'enterpriseValue']
    # chatgpt helped with this line
    df = df[~(df[cols_to_clean] == 0).any(axis=1)]
    df['symbol'] = df['symbol'].fillna('NA')
    # df = df.dropna(subset=['symbol'])
    df['industry'].fillna('Not Available', inplace=True)
    df['sector'].fillna('Not Available', inplace=True)
    # missing 150 odd ipoDates, not that important for analysis
    # so will just remove the whole column
    df.drop('ipoDate', axis=1, inplace=True)
    return df


def clean_rank(df):
    df = df.dropna(subset=['overallRank'])
    return df


def transform_data(df):
    df_with_ev = calculate_enterprise_value(df)
    df_with_yield = calculate_yield(df_with_ev)
    df_with_roc = calculate_return(df_with_yield)
    clean_data_df = clean_data(df_with_roc)
    ranked_data = calculate_rank_fields(clean_data_df)
    clean_ranked_data = clean_rank(ranked_data)
    return clean_ranked_data
