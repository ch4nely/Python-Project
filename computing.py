"""
Computation methods for FinancialTrendAnalyzer

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


class FinancialTrendAnalyzer:
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
            raise ValueError(f"Window size ({window}) cannot be larger than data length ({len(self.market_data)}). Please choose a smaller window size.")  # Raise error if too large
        
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


