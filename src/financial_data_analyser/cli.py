import argparse
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Financial Data Analyser")
    parser.add_argument(
        "--streamlit",
        action="store_true",
        help="Run the Streamlit dashboard",
    )
    args = parser.parse_args()

    if args.streamlit:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "src/financial_data_analyser/app.py",
            ],
            check=True,
        )
    else:
        print("Financial Data Analyser package installed successfully.")
        print("Run the dashboard with:")
        print("  uv run -m financial_data_analyser --streamlit")