import yfinance as yf
import pandas as pd
from datetime import datetime

class DataCollector:
    """
    Class for collecting financial data for a portfolio of assets.
    """
    def __init__(self):
        """
        Initialize the DataCollector with empty attributes.
        """
        self.start_date = None
        self.end_date = None
        self.assets = []  # ✅ No default assets
        self.data = None

    def set_parameters(self, start_date, end_date, assets):
        """
        Set the parameters for data fetching.
        """
        try:
            self.start_date = pd.to_datetime(start_date, format="%Y-%m-%d").strftime("%Y-%m-%d")
            self.end_date = pd.to_datetime(end_date, format="%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        if not assets or not isinstance(assets, list) or not all(isinstance(asset, str) for asset in assets):
            raise ValueError("Assets must be a non-empty list of valid ticker symbols.")

        self.assets = assets  # ✅ Only set assets here

    def fetch_data(self):
        """
        Fetch data from Yahoo Finance.
        """
        if not self.assets:
            raise ValueError("No assets specified. Call `set_parameters()` first.")

        try:
            data = yf.download(self.assets, start=self.start_date, end=self.end_date, progress=False)
            print(f"Fetched data index: {data.index}")  # ✅ Debugging
            print(f"Available columns: {data.columns}")

            if "Adj Close" in data.columns:
                self.data = data["Adj Close"].dropna(how="all")
            elif "Close" in data.columns:
                self.data = data["Close"].dropna(how="all")
            else:
                raise KeyError("Neither 'Adj Close' nor 'Close' columns are present.")
        except Exception as e:
            raise ConnectionError(f"Failed to fetch data: {e}")

    def calculate_returns(self):
        """
        Calculate daily returns for the portfolio assets.
        """
        if self.data is None:
            raise ValueError("No data available. Please fetch data first using `fetch_data`.")

        print(f"Raw data before calculating returns:\n{self.data}")  # ✅ Debugging step
        returns = self.data.pct_change().dropna()
        print(f"Calculated returns:\n{returns}")  # ✅ Debugging step
        return returns

    def save_data(self, file_path: str):
        """
        Save the collected data to a CSV file.
        """
        if self.data is None:
            raise ValueError("No data available to save. Please fetch data first using `fetch_data`.")

        self.data.to_csv(file_path)
        print(f"Data saved to {file_path}")