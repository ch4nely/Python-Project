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
    