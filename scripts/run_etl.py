import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_tickers
from etl.extract.extract import extract_data
from etl.transform.transform import transform_data
from etl.load.load import load_to_bucket


def main():
    run_env_setup()

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )
    clean_data_file_path = 'data/clean/clean_ranked_data.csv'
    clean_data_file = 'clean_ranked_data.csv'
    ticker_df = extract_tickers()
    all_api_data = extract_data(ticker_df)
    transformed_data = transform_data(all_api_data)
    transformed_data.to_csv(clean_data_file_path, index=False)
    load_to_bucket(clean_data_file_path, clean_data_file)


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
