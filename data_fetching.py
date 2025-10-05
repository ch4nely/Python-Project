"""
Data fetching and initializer for FinancialTrendAnalyzer
"""

# Import required libraries for stock analysis
import yfinance as yf  # Library to download stock data from Yahoo Finance
import pandas as pd  # Library for data manipulation and analysis
import numpy as np  # Library for numerical computations
import matplotlib.pyplot as plt  # Library for creating plots and charts
from typing import Tuple, Dict, List  # Type hints for better code documentation
import warnings  # Library to handle warning messages
warnings.filterwarnings('ignore')  # Suppress all warning messages to keep output clean


class FinancialTrendAnalyzer:
    """
    A comprehensive financial market trend analysis tool that provides various
    technical analysis functions and visualizations.
    """
    
    def __init__(self, symbol: str, period: str = "3y"):
        """
        This function will initialize the FinancialTrendAnalyzer with a stock symbol and time period.
        The symbol (str) argument: Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
        The period (str) argument: Time period for data ('1y', '2y', '3y', etc.)
        """
        self.ticker_symbol = symbol.upper()  # Convert symbol to uppercase (e.g., 'aapl' becomes 'AAPL')
        self.time_period = period  # Store the time period (e.g., '3y' for 3 years)
        self.market_data = None  # Initialize data as None, will be filled by _fetch_data()
        self._fetch_data()  # Call the private method to download stock data
    
    def _fetch_data(self):
        """
        This function will fetch the stock data using yfinance API."""
        try:  # Try to download the stock data
            ticker_obj = yf.Ticker(self.ticker_symbol)  # Create a yfinance Ticker object for the stock symbol
            self.market_data = ticker_obj.history(period=self.time_period)  # Download historical data for the specified period
            if self.market_data.empty:  # Check if no data was downloaded
                raise ValueError(f"No data found for symbol {self.ticker_symbol}")  # Raise error if no data
            print(f"Successfully fetched {len(self.market_data)} days of data for {self.ticker_symbol}")  # Print success message with data count
        except Exception as e:  # Catch any error that occurs during download
            raise Exception(f"Error fetching data for {self.ticker_symbol}: {str(e)}")  # Raise the error with details


