import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_tickers
from etl.extract.extract import extract_data
from etl.transform.transform import transform_data


def main():
    run_env_setup()

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )
    ticker_df = extract_tickers()
    # tickers_list = ticker_df['symbol'].tolist()
    all_api_data = extract_data(ticker_df)
    # print(ticker_df)
    transformed_data = transform_data(all_api_data)
    transformed_data.to_csv('data/clean/clean_ranked_data4.csv', index=False)


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
