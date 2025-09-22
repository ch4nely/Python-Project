# Import required libraries for stock analysis
import yfinance as yf  # Library to download stock data from Yahoo Finance
import pandas as pd  # Library for data manipulation and analysis
import numpy as np  # Library for numerical computations
import matplotlib.pyplot as plt  # Library for creating plots and charts
import seaborn as sns  # Library for statistical data visualization
from typing import Tuple, Dict, List  # Type hints for better code documentation
import warnings  # Library to handle warning messages
warnings.filterwarnings('ignore')  # Suppress all warning messages to keep output clean

class StockAnalyzer:
    """
    A comprehensive stock market analysis tool that provides various
    technical analysis functions and visualizations.
    """
    
    def __init__(self, symbol: str, period: str = "3y"):
        """
        Initialize the StockAnalyzer with a stock symbol and time period.
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
            period (str): Time period for data ('1y', '2y', '3y', etc.)
        """
        self.symbol = symbol.upper()  # Convert symbol to uppercase (e.g., 'aapl' becomes 'AAPL')
        self.period = period  # Store the time period (e.g., '3y' for 3 years)
        self.data = None  # Initialize data as None, will be filled by _fetch_data()

        self._fetch_data()  # Call the private method to download stock data
        
def _fetch_data(self):
        """Fetch stock data using yfinance."""
        try:  # Try to download the stock data
            ticker = yf.Ticker(self.symbol)  # Create a yfinance Ticker object for the stock symbol
            self.data = ticker.history(period=self.period)  # Download historical data for the specified period
            if self.data.empty:  # Check if no data was downloaded
                raise ValueError(f"No data found for symbol {self.symbol}")  # Raise error if no data
            print(f"Successfully fetched {len(self.data)} days of data for {self.symbol}")  # Print success message with data count
        except Exception as e:  # Catch any error that occurs during download
            raise Exception(f"Error fetching data for {self.symbol}: {str(e)}")  # Raise error with details


def simple_moving_average(self, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA) for closing prices.

    Args:
        window (int): Number of periods for SMA calculation

    Returns:
        pd.Series: SMA values
    """
    if window <= 0:  # Check if window size is invalid (zero or negative)
        raise ValueError("Window size must be positive")  # Raise error if invalid
    if window > len(self.data):  # Check if window is larger than available data
        raise ValueError("Window size cannot be larger than data length")  # Raise error if too large