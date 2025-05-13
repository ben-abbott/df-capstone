import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_tickers
from etl.extract.extract import extract_data


def main():
    run_env_setup()

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )
    ticker_df = extract_tickers()
    tickers_list = ticker_df.index.tolist()
    all_api_data = extract_data(tickers_list)
    print(all_api_data)


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
