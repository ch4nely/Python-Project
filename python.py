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
        
    def analyze_runs(self) -> Dict:
        """
        Analyze upward and downward runs in stock prices.
        
        Returns:
            Dict: Dictionary containing run statistics
        """
        # Calculate daily price changes
        price_changes = self.data['Close'].diff()  # Calculate difference between consecutive closing prices
        
        # Identify upward and downward days
        upward_days = price_changes > 0  # Boolean array: True where price went up
        downward_days = price_changes < 0  # Boolean array: True where price went down
        
        # Find runs (consecutive sequences of same direction)
        upward_runs = []  # List to store lengths of upward runs
        downward_runs = []  # List to store lengths of downward runs
        
        current_upward_run = 0  # Counter for current upward run length
        current_downward_run = 0  # Counter for current downward run length
        
        for i, is_up in enumerate(upward_days):  # Loop through each day's upward status
            if is_up:  # If this day was upward
                current_upward_run += 1  # Increment upward run counter
                if current_downward_run > 0:  # If we were in a downward run
                    downward_runs.append(current_downward_run)  # Save the downward run length
                    current_downward_run = 0  # Reset downward run counter
            elif price_changes.iloc[i] < 0:  # If this day was downward (not zero change)
                current_downward_run += 1  # Increment downward run counter
                if current_upward_run > 0:  # If we were in an upward run
                    upward_runs.append(current_upward_run)  # Save the upward run length
                    current_upward_run = 0  # Reset upward run counter
            # Skip zero changes (no change days) - don't count them as either direction
        
        # Add final runs (in case the data ends in the middle of a run)
        if current_upward_run > 0:  # If we ended in an upward run
            upward_runs.append(current_upward_run)  # Save the final upward run
        if current_downward_run > 0:  # If we ended in a downward run
            downward_runs.append(current_downward_run)  # Save the final downward run
        
        return {  # Return a dictionary with all the run statistics
            'upward_runs': upward_runs,  # List of upward run lengths
            'downward_runs': downward_runs,  # List of downward run lengths
            'total_upward_days': sum(upward_runs),  # Total number of upward days
            'total_downward_days': sum(downward_runs),  # Total number of downward days
            'longest_upward_streak': max(upward_runs) if upward_runs else 0,  # Longest consecutive upward days
            'longest_downward_streak': max(downward_runs) if downward_runs else 0,  # Longest consecutive downward days
            'upward_run_count': len(upward_runs),  # Number of upward runs
            'downward_run_count': len(downward_runs)  # Number of downward runs
        }

    def calculate_daily_returns(self) -> pd.Series:
        """
        Calculate simple daily returns.

        Returns:
            pd.Series: Daily returns as percentage
        """
        returns = self.data['Close'].pct_change() * 100  # Calculate percentage change and convert to percentage
        return returns  # Return the daily returns series

