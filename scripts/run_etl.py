import os
import sys
from config.env_config import setup_env
from etl.extract.extract import get_ticker_list


def main():
    run_env_setup()

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )

    print(get_ticker_list())


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
