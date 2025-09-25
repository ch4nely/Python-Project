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
        
    def max_profit(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Calculate maximum profit using Best Time to Buy and Sell Stock II algorithm.
        Allows multiple transactions.
        
        Returns:
            Tuple[float, List[Tuple[int, int]]]: Maximum profit and list of buy/sell pairs
        """
        prices = self.data['Close'].values  # Get closing prices as numpy array
        n = len(prices)  # Get total number of days
        
        if n < 2:  # Need at least 2 days to buy and sell
            return 0.0, []  # Return zero profit and empty list if insufficient data
        
        profit = 0.0  # Initialize total profit to zero
        buy_sell_pairs = []  # List to store (buy_day, sell_day) pairs
        buy_price = None  # Track current buy price (None means no position)
        buy_index = None  # Track current buy day index
        
        for i in range(n - 1):  # Loop through all days except the last one
            # If we don't have a position and tomorrow's price is higher, buy today
            if buy_price is None and prices[i] < prices[i + 1]:  # No position and price will rise
                buy_price = prices[i]  # Set buy price to today's price
                buy_index = i  # Remember which day we bought
            
            # If we have a position and tomorrow's price is lower, sell today
            elif buy_price is not None and prices[i] > prices[i + 1]:  # Have position and price will fall
                profit += prices[i] - buy_price  # Add profit from this transaction
                buy_sell_pairs.append((buy_index, i))  # Record this buy/sell pair
                buy_price = None  # Clear position
                buy_index = None  # Clear buy index
        
        # If we still have a position at the end, sell it
        if buy_price is not None:  # If we still own stock on the last day
            profit += prices[-1] - buy_price  # Sell at last day's price
            buy_sell_pairs.append((buy_index, n - 1))  # Record final transaction
        
        return profit, buy_sell_pairs  # Return total profit and all transaction pairs


    def plot_price_and_sma(self, sma_window: int = 20):
        """
        Plot closing price and SMA on the same chart.

        Args:
            sma_window (int): Window size for SMA calculation
        """
        plt.figure(figsize=(12, 8))

        # Calculate SMA
        sma = self.simple_moving_average(sma_window)

        # Plot closing price
        plt.plot(self.data.index, self.data['Close'], label=f'{self.symbol} Closing Price', linewidth=2)

        # Plot SMA
        plt.plot(self.data.index, sma, label=f'SMA({sma_window})', linewidth=2, alpha=0.8)

        plt.title(f'{self.symbol} Stock Price and Simple Moving Average', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_runs(self):
        """
        Plot stock price with upward and downward runs highlighted.
        """
        plt.figure(figsize=(15, 8))
        
        # Calculate price changes
        price_changes = self.data['Close'].diff()
        
        # Create color map for runs
        colors = []
        for change in price_changes:
            if change > 0:
                colors.append('green')
            elif change < 0:
                colors.append('red')
            else:
                colors.append('gray')
        
        # Plot price line
        plt.plot(self.data.index, self.data['Close'], color='black', linewidth=1, alpha=0.7)
        
        # Plot colored segments for runs
        for i in range(1, len(self.data)):
            if colors[i] != 'gray':
                plt.plot([self.data.index[i-1], self.data.index[i]], 
                        [self.data['Close'].iloc[i-1], self.data['Close'].iloc[i]], 
                        color=colors[i], linewidth=3, alpha=0.8)
        
        plt.title(f'{self.symbol} Stock Price with Upward (Green) and Downward (Red) Runs', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_runs(self):
        """
        Plot stock price with upward and downward runs highlighted.
        """
        plt.figure(figsize=(15, 8))
        
        # Calculate price changes
        price_changes = self.data['Close'].diff()
        
        # Create color map for runs
        colors = []
        for change in price_changes:
            if change > 0:
                colors.append('green')
            elif change < 0:
                colors.append('red')
            else:
                colors.append('gray')
        
        # Plot price line
        plt.plot(self.data.index, self.data['Close'], color='black', linewidth=1, alpha=0.7)
        
        # Plot colored segments for runs
        for i in range(1, len(self.data)):
            if colors[i] != 'gray':
                plt.plot([self.data.index[i-1], self.data.index[i]], 
                        [self.data['Close'].iloc[i-1], self.data['Close'].iloc[i]], 
                        color=colors[i], linewidth=3, alpha=0.8)
        
        plt.title(f'{self.symbol} Stock Price with Upward (Green) and Downward (Red) Runs', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_daily_returns(self):
        """
        Plot daily returns as a histogram and time series.
        """
        returns = self.calculate_daily_returns()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Histogram
        ax1.hist(returns.dropna(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title(f'{self.symbol} Daily Returns Distribution', fontsize=14)
        ax1.set_xlabel('Daily Returns (%)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Time series
        ax2.plot(self.data.index, returns, color='purple', linewidth=1)
        ax2.set_title(f'{self.symbol} Daily Returns Over Time', fontsize=14)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Daily Returns (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()

    def generate_report(self, sma_window: int = 20):
        """
        Generate a comprehensive analysis report.
        
        Args:
            sma_window (int): Window size for SMA calculation
        """
        print(f"\n{'='*60}")
        print(f"STOCK ANALYSIS REPORT FOR {self.symbol}")
        print(f"{'='*60}")
        
        # Basic statistics
        print(f"\nData Period: {self.data.index[0].strftime('%Y-%m-%d')} to {self.data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(self.data)}")
        print(f"Current Price: ${self.data['Close'].iloc[-1]:.2f}")
        print(f"Price Range: ${self.data['Close'].min():.2f} - ${self.data['Close'].max():.2f}")
        
        # SMA Analysis
        sma = self.simple_moving_average(sma_window)
        current_sma = sma.iloc[-1]
        print(f"\nSimple Moving Average ({sma_window} days): ${current_sma:.2f}")
        
        # Runs Analysis
        runs = self.analyze_runs()
        print(f"\nRUNS ANALYSIS:")
        print(f"Total Upward Days: {runs['total_upward_days']}")
        print(f"Total Downward Days: {runs['total_downward_days']}")
        print(f"Longest Upward Streak: {runs['longest_upward_streak']} days")
        print(f"Longest Downward Streak: {runs['longest_downward_streak']} days")
        print(f"Number of Upward Runs: {runs['upward_run_count']}")
        print(f"Number of Downward Runs: {runs['downward_run_count']}")
        
        # Daily Returns Analysis
        returns = self.calculate_daily_returns()
        print(f"\nDAILY RETURNS ANALYSIS:")
        print(f"Average Daily Return: {returns.mean():.4f}%")
        print(f"Standard Deviation: {returns.std():.4f}%")
        print(f"Best Day: {returns.max():.4f}%")
        print(f"Worst Day: {returns.min():.4f}%")
        
        # Max Profit Analysis
        max_profit, buy_sell_pairs = self.max_profit()
        print(f"\nMAXIMUM PROFIT ANALYSIS:")
        print(f"Maximum Possible Profit: ${max_profit:.2f}")
        print(f"Number of Transactions: {len(buy_sell_pairs)}")
        
        if buy_sell_pairs:
            print("Buy/Sell Pairs (Index, Date):")
            for buy_idx, sell_idx in buy_sell_pairs[:5]:  # Show first 5
                buy_date = self.data.index[buy_idx].strftime('%Y-%m-%d')
                sell_date = self.data.index[sell_idx].strftime('%Y-%m-%d')
                buy_price = self.data['Close'].iloc[buy_idx]
                sell_price = self.data['Close'].iloc[sell_idx]
                profit = sell_price - buy_price
                print(f"  Buy: {buy_date} (${buy_price:.2f}) -> Sell: {sell_date} (${sell_price:.2f}) | Profit: ${profit:.2f}")
        
        print(f"\n{'='*60}")


    def validate_calculations():
        """
        Validate calculations with test cases to ensure correctness.
        """
        print("\n" + "="*60)
        print("VALIDATION TESTS")
        print("="*60)
    
        # Test with a well-known stock
        try:
            analyzer = StockAnalyzer("AAPL", "1y")
        
            # Test 1: SMA validation against pandas rolling mean
            print("\nTest 1: SMA Validation - Your Implementation vs Pandas Reference")
            print("-" * 60)
            sma_5 = analyzer.simple_moving_average(5)
            sma_5_pandas = analyzer.data['Close'].rolling(window=5).mean()
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
            returns_custom = analyzer.calculate_daily_returns()
            returns_pandas = analyzer.data['Close'].pct_change() * 100
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
            runs = analyzer.analyze_runs()
            price_changes = analyzer.data['Close'].diff()
            upward_days_manual = (price_changes > 0).sum()
            downward_days_manual = (price_changes < 0).sum()
            print(f"Upward days count matches: {runs['total_upward_days'] == upward_days_manual}")
            print(f"Downward days count matches: {runs['total_downward_days'] == downward_days_manual}")
        
            # Test 4: Max profit with simple case
            print("\nTest 4: Max Profit Validation")
            # Create a simple test case: [1, 2, 3, 2, 1] should give profit of 2
            test_prices = pd.Series([1, 2, 3, 2, 1])
            test_analyzer = StockAnalyzer.__new__(StockAnalyzer)
            test_analyzer.data = pd.DataFrame({'Close': test_prices})
            test_profit, test_pairs = test_analyzer.max_profit()
            expected_profit = 2.0  # Buy at 1, sell at 3
            print(f"Simple test case profit matches: {abs(test_profit - expected_profit) < 1e-10}")
        
            # Test 5: Edge case - single day data
            print("\nTest 5: Edge Case Validation")
            single_day_data = pd.DataFrame({'Close': [100]}, index=[pd.Timestamp('2023-01-01')])
            test_analyzer.data = single_day_data
            try:
                sma_edge = test_analyzer.simple_moving_average(5)
                print("SMA with insufficient data handled correctly: False")
            except ValueError:
                print("SMA with insufficient data handled correctly: True")
        
            print("\nAll validation tests completed!")
        
        except Exception as e:
            print(f"Validation failed with error: {e}")


# =============================================================================
# END OF STOCK ANALYZER CLASS
# =============================================================================


    if __name__ == "__main__":
        # Example usage
        print("Stock Market Trend Analysis Tool")
        print("=" * 40)
    
        # Validate calculations first
        validate_calculations()
    
        # Example analysis
        try:
            # Analyze Apple stock
            analyzer = StockAnalyzer("AAPL", "2y")
        
            # Generate comprehensive report
            analyzer.generate_report(sma_window=20)
        
            # Create visualizations
            print("\nGenerating visualizations...")
            analyzer.plot_price_and_sma(sma_window=20)
            analyzer.plot_runs()
            analyzer.plot_daily_returns()
        
        except Exception as e:
            print(f"Error during analysis: {e}")
       


   




