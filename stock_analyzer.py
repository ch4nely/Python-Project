"""
Stock Market Trend Analysis Tool

This module provides comprehensive stock market analysis functionality including:
- Simple Moving Average (SMA) calculations
- Upward and downward runs analysis
- Daily returns computation
- Maximum profit calculation
- Data visualization
- Validation and testing

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
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
        The symbol (str) arguement: Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
        The period (str) arguement: Time period for data ('1y', '2y', '3y', etc.)
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
    
    def calculate_simple_moving_average(self, window: int) -> pd.Series:
        """
        Calculate the Simple Moving Average (SMA) for closing prices.
        
        Args:
            window (int): Number of periods for SMA calculation
            
        Returns:
            pd.Series: SMA values
            
        Raises:
            ValueError: If window size is not positive or exceeds data length
            
        Edge Cases:
            - Window <= 0: Raises ValueError("Window size must be positive")
            - Window > data length: Raises ValueError("Window size cannot be larger than data length")
            - NaN values: Automatically excluded from rolling calculations
        """
        if window <= 0:  # Check if window size is invalid (zero or negative)
            raise ValueError("Window size must be positive")  # Raise error if invalid
        if window > len(self.market_data):  # Check if window is larger than available data
            raise ValueError("Window size cannot be larger than data length")  # Raise error if too large
        
        return self.market_data['Close'].rolling(window=window).mean()  # Calculate rolling mean of closing prices
    
    def analyze_price_runs(self) -> Dict:
        """
        Analyze upward and downward price runs for the stock.
        
        Returns:
            Dict: Dictionary containing run statistics with keys:
                - 'upward_runs': List of upward run lengths
                - 'downward_runs': List of downward run lengths  
                - 'total_upward_days': Total number of upward days
                - 'total_downward_days': Total number of downward days
                - 'longest_upward_streak': Longest consecutive upward days
                - 'longest_downward_streak': Longest consecutive downward days
                - 'upward_run_count': Number of upward runs
                - 'downward_run_count': Number of downward runs
                
        Edge Cases:
            - Zero-change days: Excluded from runs (no direction)
            - Insufficient data: Returns empty lists and zero counts
            - NaN values: Treated as zero changes
        """
        # Calculate daily price changes
        daily_price_changes = self.market_data['Close'].diff()  # Calculate difference between consecutive closing prices
        
        # Identify upward and downward days
        positive_change_days = daily_price_changes > 0  # Boolean array: True where price went up
        negative_change_days = daily_price_changes < 0  # Boolean array: True where price went down
        
        # Find runs (consecutive sequences of same direction)
        bullish_runs = []  # List to store lengths of upward runs
        bearish_runs = []  # List to store lengths of downward runs
        
        current_bullish_run = 0  # Counter for current upward run length
        current_bearish_run = 0  # Counter for current downward run length
        
        for i, is_up in enumerate(positive_change_days):  # Loop through each day's upward status
            if is_up:  # If this day was upward
                current_bullish_run += 1  # Increment upward run counter
                if current_bearish_run > 0:  # If we were in a downward run
                    bearish_runs.append(current_bearish_run)  # Save the downward run length
                    current_bearish_run = 0  # Reset downward run counter
            elif daily_price_changes.iloc[i] < 0:  # If this day was downward (not zero change)
                current_bearish_run += 1  # Increment downward run counter
                if current_bullish_run > 0:  # If we were in an upward run
                    bullish_runs.append(current_bullish_run)  # Save the upward run length
                    current_bullish_run = 0  # Reset upward run counter
            # Skip zero changes (no change days) - don't count them as either direction
        
        # Add final runs (in case the data ends in the middle of a run)
        if current_bullish_run > 0:  # If we ended in an upward run
            bullish_runs.append(current_bullish_run)  # Save the final upward run
        if current_bearish_run > 0:  # If we ended in a downward run
            bearish_runs.append(current_bearish_run)  # Save the final downward run
        
        return {  # Return a dictionary with all the run statistics
            'upward_runs': bullish_runs,  # List of upward run lengths
            'downward_runs': bearish_runs,  # List of downward run lengths
            'total_upward_days': sum(bullish_runs),  # Total number of upward days
            'total_downward_days': sum(bearish_runs),  # Total number of downward days
            'longest_upward_streak': max(bullish_runs) if bullish_runs else 0,  # Longest consecutive upward days
            'longest_downward_streak': max(bearish_runs) if bearish_runs else 0,  # Longest consecutive downward days
            'upward_run_count': len(bullish_runs),  # Number of upward runs
            'downward_run_count': len(bearish_runs)  # Number of downward runs
        }
    
    def compute_daily_returns(self) -> pd.Series:
        """
        Calculate simple daily returns as percentage changes.
        
        Formula: ((Price_t - Price_t-1) / Price_t-1) * 100
        
        Returns:
            pd.Series: Daily returns as percentage
            
        Edge Cases:
            - First day: Returns NaN (no previous day to compare)
            - NaN values: Preserved in output series
            - Zero prices: May result in inf/-inf values
        """
        daily_returns = self.market_data['Close'].pct_change() * 100  # Calculate percentage change and convert to percentage
        return daily_returns  # Return the daily returns series
    
    def calculate_maximum_profit(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        This function will calculate maximum profit using Best Time to Buy and Sell Stock II algorithm.
        
        Implements optimal buy/sell strategy allowing multiple transactions.
        
        Returns:
            Tuple[float, List[Tuple[int, int]]]: 
                - Maximum profit amount
                - List of (buy_day_index, sell_day_index) pairs
                
        Edge Cases:
            - Insufficient data (< 2 days): Returns (0.0, [])
            - All prices decreasing: Returns (0.0, [])
            - All prices increasing: Single transaction from first to last day
        """
        closing_prices = self.market_data['Close'].values  # Get closing prices as numpy array
        total_days = len(closing_prices)  # Get total number of days
        
        if total_days < 2:  # Need at least 2 days to buy and sell
            return 0.0, []  # Return zero profit and empty list if insufficient data
        
        total_profit = 0.0  # Initialize total profit to zero
        transaction_pairs = []  # List to store (buy_day, sell_day) pairs
        current_buy_price = None  # Track current buy price (None means no position)
        current_buy_index = None  # Track current buy day index
        
        for i in range(total_days - 1):  # Loop through all days except the last one
            # If we don't have a position and tomorrow's price is higher, buy today
            if current_buy_price is None and closing_prices[i] < closing_prices[i + 1]:  # No position and price will rise
                current_buy_price = closing_prices[i]  # Set buy price to today's price
                current_buy_index = i  # Remember which day we bought
            
            # If we have a position and tomorrow's price is lower, sell today
            elif current_buy_price is not None and closing_prices[i] > closing_prices[i + 1]:  # Have position and price will fall
                total_profit += closing_prices[i] - current_buy_price  # Add profit from this transaction
                transaction_pairs.append((current_buy_index, i))  # Record this buy/sell pair
                current_buy_price = None  # Clear position
                current_buy_index = None  # Clear buy index
        
        # If we still have a position at the end, sell it
        if current_buy_price is not None:  # If we still own stock on the last day
            total_profit += closing_prices[-1] - current_buy_price  # Sell at last day's price
            transaction_pairs.append((current_buy_index, total_days - 1))  # Record final transaction
        
        return total_profit, transaction_pairs  # Return total profit and all transaction pairs
    
    def visualize_price_and_sma(self, sma_window: int = 20): # VISUALIZAITON FUNCTION
        """
        This function will plot the closing price and SMA on the same chart.
        The sma_window (int) arguement: Window size for SMA calculation
        """
        plt.figure(figsize=(12, 8))
        
        # Calculate SMA
        sma_values = self.calculate_simple_moving_average(sma_window)
        
        # Plot closing price
        plt.plot(self.market_data.index, self.market_data['Close'], label=f'{self.ticker_symbol} Closing Price', linewidth=2)
        
        # Plot SMA
        plt.plot(self.market_data.index, sma_values, label=f'SMA({sma_window})', linewidth=2, alpha=0.8)
        
        plt.title(f'{self.ticker_symbol} Stock Price and Simple Moving Average', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def visualize_price_runs(self): # VISUALIZAITON FUNCTION
        """
        This function will plot the stock price with upward and downward runs highlighted.
        """
        plt.figure(figsize=(15, 8))
        
        # Calculate price changes
        daily_price_changes = self.market_data['Close'].diff()
        
        # Create color map for runs
        segment_colors = []
        for change in daily_price_changes:
            if change > 0:
                segment_colors.append('green')
            elif change < 0:
                segment_colors.append('red')
            else:
                segment_colors.append('gray')
        
        # Plot price line
        plt.plot(self.market_data.index, self.market_data['Close'], color='black', linewidth=1, alpha=0.7)
        
        # Plot colored segments for runs
        for i in range(1, len(self.market_data)):
            if segment_colors[i] != 'gray':
                plt.plot([self.market_data.index[i-1], self.market_data.index[i]], 
                        [self.market_data['Close'].iloc[i-1], self.market_data['Close'].iloc[i]], 
                        color=segment_colors[i], linewidth=3, alpha=0.8)
        
        plt.title(f'{self.ticker_symbol} Stock Price with Upward    (Green) and Downward (Red) Runs', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def visualize_daily_returns(self): # VISUALIZAITON FUNCTION
        """
        This function will plot the daily returns as a histogram and time series.
        """
        daily_returns_data = self.compute_daily_returns()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Histogram
        ax1.hist(daily_returns_data.dropna(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title(f'{self.ticker_symbol} Daily Returns Distribution', fontsize=14)
        ax1.set_xlabel('Daily Returns (%)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Time series
        ax2.plot(self.market_data.index, daily_returns_data, color='purple', linewidth=1)
        ax2.set_title(f'{self.ticker_symbol} Daily Returns Over Time', fontsize=14)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Daily Returns (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()
    
    def create_comprehensive_report(self, sma_window: int = 20): # REPORT FUNCTION
        """
        This function will generate a comprehensive analysis report.
        The sma_window (int) arguement: Window size for SMA calculation
        """
        print(f"\n{'='*60}")
        print(f"STOCK ANALYSIS REPORT FOR {self.ticker_symbol}")
        print(f"{'='*60}")
        
        # Basic statistics
        print(f"\nData Period: {self.market_data.index[0].strftime('%Y-%m-%d')} to {self.market_data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(self.market_data)}")
        print(f"Current Price: ${self.market_data['Close'].iloc[-1]:.2f}")
        print(f"Price Range: ${self.market_data['Close'].min():.2f} - ${self.market_data['Close'].max():.2f}")
        
        # SMA Analysis
        sma_values = self.calculate_simple_moving_average(sma_window)
        current_sma_value = sma_values.iloc[-1]
        print(f"\nSimple Moving Average ({sma_window} days): ${current_sma_value:.2f}")
        
        # Runs Analysis
        runs_data = self.analyze_price_runs()
        print(f"\nRUNS ANALYSIS:")
        print(f"Total Upward Days: {runs_data['total_upward_days']}")
        print(f"Total Downward Days: {runs_data['total_downward_days']}")
        print(f"Longest Upward Streak: {runs_data['longest_upward_streak']} days")
        print(f"Longest Downward Streak: {runs_data['longest_downward_streak']} days")
        print(f"Number of Upward Runs: {runs_data['upward_run_count']}")
        print(f"Number of Downward Runs: {runs_data['downward_run_count']}")
        
        # Daily Returns Analysis
        daily_returns_data = self.compute_daily_returns()
        print(f"\nDAILY RETURNS ANALYSIS:")
        print(f"Average Daily Return: {daily_returns_data.mean():.4f}%")
        print(f"Standard Deviation: {daily_returns_data.std():.4f}%")
        print(f"Best Day: {daily_returns_data.max():.4f}%")
        print(f"Worst Day: {daily_returns_data.min():.4f}%")
        
        # Max Profit Analysis
        max_profit_value, transaction_pairs = self.calculate_maximum_profit()
        print(f"\nMAXIMUM PROFIT ANALYSIS:")
        print(f"Maximum Possible Profit: ${max_profit_value:.2f}")
        print(f"Number of Transactions: {len(transaction_pairs)}")
        
        if transaction_pairs:
            print("Buy/Sell Pairs (Index, Date):")
            for buy_idx, sell_idx in transaction_pairs[:5]:  # Show first 5
                buy_date = self.market_data.index[buy_idx].strftime('%Y-%m-%d')
                sell_date = self.market_data.index[sell_idx].strftime('%Y-%m-%d')
                buy_price = self.market_data['Close'].iloc[buy_idx]
                sell_price = self.market_data['Close'].iloc[sell_idx]
                profit = sell_price - buy_price
                print(f"  Buy: {buy_date} (${buy_price:.2f}) -> Sell: {sell_date} (${sell_price:.2f}) | Profit: ${profit:.2f}")
        
        print(f"\n{'='*60}")


def validate_all_calculations(): # VALIDATION FUNCTION
    """
    This function will validate the calculations with test cases to ensure correctness.
    """
    print("\n" + "="*60)
    print("VALIDATION TESTS")
    print("="*60)
    
    # Test with a well-known stock
    try:
        analyzer = FinancialTrendAnalyzer("AAPL", "1y")
        
        # Test 1: SMA validation against pandas rolling mean
        print("\nTest 1: SMA Validation - Your Implementation vs Pandas Reference")
        print("-" * 60)
        sma_5 = analyzer.calculate_simple_moving_average(5)
        sma_5_pandas = analyzer.market_data['Close'].rolling(window=5).mean()
        sma_match = np.allclose(sma_5.dropna(), sma_5_pandas.dropna(), rtol=1e-10)
        
        # Show side-by-side comparison
        comparison_df = pd.DataFrame({
            'Your SMA(5)': sma_5.tail(10),
            'Pandas SMA(5)': sma_5_pandas.tail(10)
        })
        print("Last 10 values comparison:")
        print(comparison_df.round(4))
        print(f"\n✅ Result: Your implementation {'MATCHES' if sma_match else 'DIFFERS FROM'} pandas reference")
        
        # Test 2: Daily returns validation
        print("\nTest 2: Daily Returns Validation - Your Implementation vs Pandas Reference")
        print("-" * 60)
        returns_custom = analyzer.compute_daily_returns()
        returns_pandas = analyzer.market_data['Close'].pct_change() * 100
        returns_match = np.allclose(returns_custom.dropna(), returns_pandas.dropna(), rtol=1e-10)
        
        # Show side-by-side comparison
        returns_df = pd.DataFrame({
            'Your Returns (%)': returns_custom.tail(10),
            'Pandas Returns (%)': returns_pandas.tail(10)
        })
        print("Last 10 daily returns comparison:")
        print(returns_df.round(4))
        print(f"\n✅ Result: Your implementation {'MATCHES' if returns_match else 'DIFFERS FROM'} pandas reference")
        
        # Test 3: Runs analysis with known data
        print("\nTest 3: Runs Analysis Validation")
        runs = analyzer.analyze_price_runs()
        price_changes = analyzer.market_data['Close'].diff()
        upward_days_manual = (price_changes > 0).sum()
        downward_days_manual = (price_changes < 0).sum()
        print(f"Upward days count matches: {runs['total_upward_days'] == upward_days_manual}")
        print(f"Downward days count matches: {runs['total_downward_days'] == downward_days_manual}")
        
        # Test 3.5: Synthetic data validation for runs/streaks
        print("\nTest 3.5: Synthetic Data Runs Validation")
        # Create synthetic price series: [10, 11, 12, 13, 12, 11, 10, 9, 8, 9, 10, 11, 12]
        # Expected: 3-day upward run, 3-day downward run, 4-day upward run
        synthetic_prices = pd.Series([10, 11, 12, 13, 12, 11, 10, 9, 8, 9, 10, 11, 12])
        synthetic_analyzer = FinancialTrendAnalyzer.__new__(FinancialTrendAnalyzer)
        synthetic_analyzer.market_data = pd.DataFrame({'Close': synthetic_prices})
        synthetic_runs = synthetic_analyzer.analyze_price_runs()
        
        # Expected results based on synthetic data
        expected_upward_runs = [3, 4]  # 3-day run (10->11->12->13), 4-day run (8->9->10->11->12)
        expected_downward_runs = [5]   # 5-day run (13->12->11->10->9->8)
        expected_total_upward_days = 7  # 3 + 4
        expected_total_downward_days = 5  # 5
        expected_longest_upward = 4
        expected_longest_downward = 5
        
        print(f"Synthetic data upward runs: {synthetic_runs['upward_runs']}")
        print(f"Expected upward runs: {expected_upward_runs}")
        print(f"Upward runs match: {synthetic_runs['upward_runs'] == expected_upward_runs}")
        
        print(f"Synthetic data downward runs: {synthetic_runs['downward_runs']}")
        print(f"Expected downward runs: {expected_downward_runs}")
        print(f"Downward runs match: {synthetic_runs['downward_runs'] == expected_downward_runs}")
        
        print(f"Total upward days: {synthetic_runs['total_upward_days']} (expected: {expected_total_upward_days})")
        print(f"Total downward days: {synthetic_runs['total_downward_days']} (expected: {expected_total_downward_days})")
        print(f"Longest upward streak: {synthetic_runs['longest_upward_streak']} (expected: {expected_longest_upward})")
        print(f"Longest downward streak: {synthetic_runs['longest_downward_streak']} (expected: {expected_longest_downward})")
        
        # Comprehensive validation
        synthetic_valid = (
            synthetic_runs['upward_runs'] == expected_upward_runs and
            synthetic_runs['downward_runs'] == expected_downward_runs and
            synthetic_runs['total_upward_days'] == expected_total_upward_days and
            synthetic_runs['total_downward_days'] == expected_total_downward_days and
            synthetic_runs['longest_upward_streak'] == expected_longest_upward and
            synthetic_runs['longest_downward_streak'] == expected_longest_downward
        )
        print(f"✅ Synthetic runs validation: {'PASSED' if synthetic_valid else 'FAILED'}")
        
        # Test 4: Max profit with simple case
        print("\nTest 4: Max Profit Validation")
        # Create a simple test case: [1, 2, 3, 2, 1] should give profit of 2
        test_prices = pd.Series([1, 2, 3, 2, 1])
        test_analyzer = FinancialTrendAnalyzer.__new__(FinancialTrendAnalyzer)
        test_analyzer.market_data = pd.DataFrame({'Close': test_prices})
        test_profit, test_pairs = test_analyzer.calculate_maximum_profit()
        expected_profit = 2.0  # Buy at 1, sell at 3
        print(f"Simple test case profit matches: {abs(test_profit - expected_profit) < 1e-10}")
        
        # Test 5: Edge case - single day data
        print("\nTest 5: Edge Case Validation")
        single_day_data = pd.DataFrame({'Close': [100]}, index=[pd.Timestamp('2023-01-01')])
        test_analyzer.market_data = single_day_data
        try:
            sma_edge = test_analyzer.calculate_simple_moving_average(5)
            print("SMA with insufficient data handled correctly: False")
        except ValueError:
            print("SMA with insufficient data handled correctly: True")
        
        print("\nAll validation tests completed!")
        
    except Exception as e:
        print(f"Validation failed with error: {e}")


if __name__ == "__main__":
    # Example usage
    print("Stock Market Trend Analysis Tool")
    print("=" * 40)
    
    # Validate calculations first
    validate_all_calculations()
    
    # Example analysis
    try:
        # Analyze Apple stock
        analyzer = FinancialTrendAnalyzer("AAPL", "2y")
        
        # Generate comprehensive report
        analyzer.create_comprehensive_report(sma_window=20)
        
        # Create visualizations
        print("\nGenerating visualizations...")
        analyzer.visualize_price_and_sma(sma_window=20)
        analyzer.visualize_price_runs()
        analyzer.visualize_daily_returns()
        
    except Exception as e:
        print(f"Error during analysis: {e}")
