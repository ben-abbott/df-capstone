# import pandas as pd


def join_df(df_list):
    if len(df_list) == 3:
        all_data = df_list[0].merge(df_list[1], on='symbol', how='outer')
        all_data = all_data.merge(df_list[2], on='symbol', how='outer')
    else:
        print('The number of DataFrames to be joined is not 3, can only join 3 DataFrames')
    return all_data


def transform_data():
    pass
