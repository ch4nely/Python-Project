"""
Visualization methods for FinancialTrendAnalyzer
Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import matplotlib.pyplot as plt
import pandas as pd


class FinancialTrendAnalyzer:
    def visualize_price_and_sma(self, sma_window: int = 20): # VISUALIZATION FUNCTION
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
    
    def visualize_price_runs(self): # VISUALIZATION FUNCTION
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
    
    def visualize_daily_returns(self): # VISUALIZATION FUNCTION
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


