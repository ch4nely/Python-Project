"""
Data fetching and initializer for FinancialTrendAnalyzer

This module handles the initialization and data retrieval functionality for the
FinancialTrendAnalyzer class. It provides the foundation for all financial analysis
by downloading historical stock data from Yahoo Finance using the yfinance library.

Key Responsibilities:
- Initialize analyzer with stock symbol and time period
- Download historical OHLCV (Open, High, Low, Close, Volume) data
- Handle data validation and error cases
- Store market data in pandas DataFrame format

The data fetching process uses Yahoo Finance as the data source, which provides
free access to historical stock data for most publicly traded companies.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# Import required libraries for stock analysis
import yfinance as yf  # Library to download stock data from Yahoo Finance API
import pandas as pd  # Library for data manipulation and analysis (DataFrame operations)
import numpy as np  # Library for numerical computations and array operations
import matplotlib.pyplot as plt  # Library for creating plots and charts
from typing import Tuple, Dict, List  # Type hints for better code documentation and IDE support
import warnings  # Library to handle warning messages
warnings.filterwarnings('ignore')  # Suppress all warning messages to keep output clean


class FinancialTrendAnalyzer:
    """
    A comprehensive financial market trend analysis tool that provides various
    technical analysis functions and visualizations.
    
    This class serves as the data fetching mixin for the composite FinancialTrendAnalyzer.
    It handles the initialization and data retrieval process, downloading historical
    stock data from Yahoo Finance and storing it in a pandas DataFrame for further analysis.
    
    Attributes:
        ticker_symbol (str): Stock symbol in uppercase (e.g., 'AAPL', 'GOOGL')
        time_period (str): Time period for data retrieval ('1y', '2y', '3y', '5y', 'max')
        market_data (pd.DataFrame): Historical OHLCV data with datetime index
    
    Data Structure:
        The market_data DataFrame contains the following columns:
        - Open: Opening price for each trading day
        - High: Highest price during the trading day
        - Low: Lowest price during the trading day
        - Close: Closing price for each trading day
        - Volume: Number of shares traded
        - Dividends: Dividend payments (if any)
        - Stock Splits: Stock split information (if any)
    
    Example Usage:
        # Create analyzer for Apple stock with 1 year of data
        analyzer = FinancialTrendAnalyzer("AAPL", "1y")
        
        # Access the downloaded data
        print(f"Downloaded {len(analyzer.market_data)} days of data")
        print(f"Current price: ${analyzer.market_data['Close'].iloc[-1]:.2f}")
    
    Error Handling:
        - Invalid stock symbols: Raises Exception with descriptive message
        - Network issues: Raises Exception with error details
        - Empty data: Raises ValueError if no data found for symbol
    """
    
    def __init__(self, symbol: str, period: str = "3y"):
        """
        Initialize the FinancialTrendAnalyzer with a stock symbol and time period.
        
        This constructor sets up the analyzer by storing the stock symbol and time period,
        then automatically downloads the historical data by calling the private _fetch_data method.
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT', 'TSLA')
                         Case insensitive - will be converted to uppercase
            period (str, optional): Time period for data retrieval. Defaults to "3y".
                                   Valid options: '1y', '2y', '3y', '5y', 'max'
        
        Raises:
            Exception: If data fetching fails due to invalid symbol or network issues
            ValueError: If no data is found for the given symbol
        
        Example:
            # Initialize with Apple stock for 1 year of data
            analyzer = FinancialTrendAnalyzer("AAPL", "1y")
            
            # Initialize with Google stock for maximum available data
            analyzer = FinancialTrendAnalyzer("GOOGL", "max")
        
        Note:
            The period parameter uses Yahoo Finance's standard period format:
            - '1y': 1 year of data
            - '2y': 2 years of data  
            - '3y': 3 years of data
            - '5y': 5 years of data
            - 'max': Maximum available data (typically 10+ years)
        """
        self.ticker_symbol = symbol.upper()  # Convert symbol to uppercase for consistency (e.g., 'aapl' becomes 'AAPL')
        self.time_period = period  # Store the time period (e.g., '3y' for 3 years)
        self.market_data = None  # Initialize data as None, will be filled by _fetch_data()
        self._fetch_data()  # Call the private method to download stock data immediately
    
    def _fetch_data(self):
        """
        Private method to fetch stock data using yfinance API.
        
        This method handles the actual data retrieval process from Yahoo Finance.
        It creates a yfinance Ticker object for the specified stock symbol and
        downloads historical OHLCV data for the specified time period.
        
        The method includes comprehensive error handling for common issues:
        - Invalid stock symbols
        - Network connectivity problems
        - Empty data responses
        - API rate limiting
        
        Raises:
            ValueError: If no data is found for the stock symbol
            Exception: If any other error occurs during data fetching
        
        Data Format:
            The downloaded data is stored in self.market_data as a pandas DataFrame
            with datetime index and columns: Open, High, Low, Close, Volume, Dividends, Stock Splits
        
        Example:
            # This method is called automatically during initialization
            analyzer = FinancialTrendAnalyzer("AAPL", "1y")
            # _fetch_data() is called internally and populates analyzer.market_data
        
        Note:
            This is a private method (indicated by the underscore prefix) and should
            not be called directly by users. It's automatically called during initialization.
        """
        try:  # Try to download the stock data
            # Create a yfinance Ticker object for the stock symbol
            # This object provides access to various financial data for the stock
            ticker_obj = yf.Ticker(self.ticker_symbol)
            
            # Download historical data for the specified period
            # The history() method returns OHLCV data as a pandas DataFrame
            self.market_data = ticker_obj.history(period=self.time_period)
            
            # Check if no data was downloaded (empty DataFrame)
            if self.market_data.empty:
                raise ValueError(f"No data found for symbol {self.ticker_symbol}")
            
            # Print success message with data count for user feedback
            print(f"Successfully fetched {len(self.market_data)} days of data for {self.ticker_symbol}")
            
        except Exception as e:  # Catch any error that occurs during download
            # Raise the error with details for debugging
            raise Exception(f"Error fetching data for {self.ticker_symbol}: {str(e)}")


