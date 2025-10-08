"""
Composite FinancialTrendAnalyzer that combines data fetching, computing, and visualization
into a single, importable class via multiple inheritance.

This module implements the Composite Pattern by combining three separate mixin classes
into one unified FinancialTrendAnalyzer class. Each mixin provides specific functionality:
- DataFetchingMixin: Handles stock data retrieval from Yahoo Finance
- ComputingMixin: Provides financial calculations (SMA, runs, returns, max profit)
- VisualizationMixin: Creates charts and plots for data visualization

The multiple inheritance approach allows for clean separation of concerns while
providing a single, easy-to-use interface for all financial analysis operations.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# Import the three mixin classes that provide different aspects of functionality
from data_fetching import FinancialTrendAnalyzer as DataFetchingMixin  # Handles data retrieval from Yahoo Finance
from computing import FinancialTrendAnalyzer as ComputingMixin  # Provides financial calculations and algorithms
from visualizations import FinancialTrendAnalyzer as VisualizationMixin  # Creates charts and visualizations


class FinancialTrendAnalyzer(DataFetchingMixin, ComputingMixin, VisualizationMixin):
    """
    Composite FinancialTrendAnalyzer class that combines all functionality.
    
    This class uses multiple inheritance to combine three separate mixin classes,
    each providing specific functionality for financial trend analysis:
    
    Inherited from DataFetchingMixin:
        - __init__(symbol, period): Initialize analyzer with stock symbol and time period
        - _fetch_data(): Download historical stock data from Yahoo Finance
        - ticker_symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
        - time_period: Time period for data ('1y', '2y', '3y', etc.)
        - market_data: Pandas DataFrame containing OHLCV stock data
    
    Inherited from ComputingMixin:
        - calculate_simple_moving_average(window): Calculate SMA for given window size
        - analyze_price_runs(): Analyze consecutive upward/downward price movements
        - compute_daily_returns(): Calculate daily percentage returns
        - calculate_maximum_profit(): Find optimal buy/sell strategy for max profit
    
    Inherited from VisualizationMixin:
        - visualize_price_and_sma(sma_window): Plot stock price with moving average
        - visualize_price_runs(): Plot price chart with upward/downward runs highlighted
        - visualize_daily_returns(): Plot daily returns as histogram and time series
    
    Usage Example:
        # Create analyzer instance
        analyzer = FinancialTrendAnalyzer("AAPL", "1y")
        
        # Perform calculations
        sma = analyzer.calculate_simple_moving_average(20)
        runs = analyzer.analyze_price_runs()
        returns = analyzer.compute_daily_returns()
        max_profit, transactions = analyzer.calculate_maximum_profit()
        
        # Generate visualizations
        analyzer.visualize_price_and_sma(20)
        analyzer.visualize_price_runs()
        analyzer.visualize_daily_returns()
    
    Design Pattern: Composite Pattern via Multiple Inheritance
    - Combines multiple classes with different responsibilities
    - Provides unified interface for complex functionality
    - Maintains separation of concerns while offering convenience
    """
    pass  # No additional methods needed - all functionality inherited from mixins


