"""
Visualization methods for FinancialTrendAnalyzer

This module provides comprehensive data visualization capabilities for the
FinancialTrendAnalyzer class. It creates various types of charts and plots
to help users understand stock market trends, patterns, and statistical distributions.

Key Visualization Features:
- Price and Moving Average Charts: Shows stock price trends with technical indicators
- Price Runs Analysis: Highlights consecutive upward/downward price movements
- Daily Returns Analysis: Displays return distributions and time series patterns

The visualizations use matplotlib for creating publication-quality charts with
professional styling, proper legends, and clear labeling.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import matplotlib.pyplot as plt  # Primary plotting library for creating charts
import pandas as pd  # Data manipulation library for handling time series data


class FinancialTrendAnalyzer:
    """
    Visualization mixin class for FinancialTrendAnalyzer.
    
    This class provides all visualization methods for the composite FinancialTrendAnalyzer.
    It creates various types of charts to help users understand stock market data through
    visual analysis of price trends, statistical distributions, and pattern recognition.
    
    Visualization Methods:
        - visualize_price_and_sma(): Creates price chart with moving average overlay
        - visualize_price_runs(): Highlights consecutive price movements with color coding
        - visualize_daily_returns(): Shows return distribution and time series patterns
    
    Chart Features:
        - Professional styling with proper legends and labels
        - Interactive elements where applicable
        - Color coding for different data types and trends
        - Grid lines and formatting for readability
        - Responsive sizing for different screen resolutions
    
    Example Usage:
        # Create analyzer and generate visualizations
        analyzer = FinancialTrendAnalyzer("AAPL", "1y")
        
        # Generate different types of charts
        analyzer.visualize_price_and_sma(20)  # Price with 20-day moving average
        analyzer.visualize_price_runs()       # Price runs with color coding
        analyzer.visualize_daily_returns()    # Returns histogram and time series
    """
    
    def visualize_price_and_sma(self, sma_window: int = 20):  # VISUALIZATION FUNCTION
        """
        Create a comprehensive price chart with Simple Moving Average overlay.
        
        This method generates a professional-quality chart showing both the stock's
        closing price and its Simple Moving Average (SMA) over time. The SMA helps
        smooth out short-term price fluctuations to reveal underlying trends.
        
        Args:
            sma_window (int): Window size for SMA calculation in trading days.
                             Defaults to 20 days (approximately 1 month of trading).
                             Common values: 5, 10, 20, 50, 100, 200 days
        
        Chart Features:
            - Stock closing price as primary line (blue, thick)
            - SMA as overlay line (red, semi-transparent)
            - Professional styling with grid and legends
            - Responsive figure size (12x8 inches)
            - Rotated x-axis labels for better readability
        
        Technical Analysis:
            - Price above SMA: Generally bullish trend
            - Price below SMA: Generally bearish trend
            - SMA slope: Indicates trend direction and strength
            - Price-SMA crossover: Potential trend change signals
        
        Example:
            # Create chart with 20-day moving average
            analyzer.visualize_price_and_sma(20)
            
            # Create chart with 50-day moving average
            analyzer.visualize_price_and_sma(50)
        
        Note:
            The SMA calculation requires at least 'sma_window' days of data.
            If insufficient data is available, the method will handle it gracefully.
        """
        # Create figure with professional sizing (12x8 inches)
        plt.figure(figsize=(12, 8))
        
        # Calculate Simple Moving Average using the specified window
        sma_values = self.calculate_simple_moving_average(sma_window)
        
        # Plot closing price as primary line (thick, blue)
        plt.plot(self.market_data.index, self.market_data['Close'], 
                label=f'{self.ticker_symbol} Closing Price', linewidth=2)
        
        # Plot SMA as overlay line (thick, red, semi-transparent)
        plt.plot(self.market_data.index, sma_values, 
                label=f'SMA({sma_window})', linewidth=2, alpha=0.8)
        
        # Chart formatting and styling
        plt.title(f'{self.ticker_symbol} Stock Price and Simple Moving Average', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend()  # Display legend to distinguish between price and SMA
        plt.grid(True, alpha=0.3)  # Add subtle grid for better readability
        plt.xticks(rotation=45)  # Rotate x-axis labels to prevent overlap
        plt.tight_layout()  # Automatically adjust layout to prevent clipping
        plt.show()  # Display the chart
    
    def visualize_price_runs(self):  # VISUALIZATION FUNCTION
        """
        Create a price chart with upward and downward runs highlighted in different colors.
        
        This method generates a sophisticated visualization that shows consecutive
        price movements by coloring segments of the price line based on whether
        the price went up (green), down (red), or remained unchanged (gray).
        
        Chart Features:
            - Black base line showing overall price trend
            - Green segments: Consecutive days of price increases
            - Red segments: Consecutive days of price decreases
            - Gray segments: Days with no price change
            - Thick colored segments (3px) for clear visibility
            - Professional styling with grid and labels
        
        Technical Analysis:
            - Green segments: Bullish momentum periods
            - Red segments: Bearish momentum periods
            - Segment length: Indicates trend strength and duration
            - Pattern analysis: Helps identify market cycles and reversals
        
        Use Cases:
            - Identify momentum periods and trend strength
            - Spot potential reversal points
            - Analyze market psychology and sentiment
            - Compare different stocks' momentum patterns
        
        Example:
            # Generate runs visualization
            analyzer.visualize_price_runs()
            
            # This will show color-coded price movements
            # Green = upward runs, Red = downward runs
        
        Note:
            Zero-change days are excluded from runs analysis as they don't
            represent directional movement in either direction.
        """
        # Create large figure for detailed visualization (15x8 inches)
        plt.figure(figsize=(15, 8))
        
        # Calculate daily price changes to determine run directions
        daily_price_changes = self.market_data['Close'].diff()
        
        # Create color map for runs based on price change direction
        segment_colors = []
        for change in daily_price_changes:
            if change > 0:  # Price increased
                segment_colors.append('green')
            elif change < 0:  # Price decreased
                segment_colors.append('red')
            else:  # No change
                segment_colors.append('gray')
        
        # Plot base price line (black, thin, semi-transparent)
        plt.plot(self.market_data.index, self.market_data['Close'], 
                color='black', linewidth=1, alpha=0.7)
        
        # Plot colored segments for runs (thick, opaque)
        for i in range(1, len(self.market_data)):
            if segment_colors[i] != 'gray':  # Skip zero-change days
                plt.plot([self.market_data.index[i-1], self.market_data.index[i]], 
                        [self.market_data['Close'].iloc[i-1], self.market_data['Close'].iloc[i]], 
                        color=segment_colors[i], linewidth=3, alpha=0.8)
        
        # Chart formatting and styling
        plt.title(f'{self.ticker_symbol} Stock Price with Upward (Green) and Downward (Red) Runs', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)  # Add subtle grid
        plt.xticks(rotation=45)  # Rotate x-axis labels
        plt.tight_layout()  # Adjust layout
        plt.show()  # Display the chart
    
    def visualize_daily_returns(self):  # VISUALIZATION FUNCTION
        """
        Create comprehensive daily returns analysis with histogram and time series.
        
        This method generates a dual-panel visualization showing both the statistical
        distribution of daily returns (histogram) and their time series pattern.
        This helps users understand both the frequency distribution and temporal
        patterns of stock price changes.
        
        Chart Features:
            - Top panel: Histogram showing return distribution
            - Bottom panel: Time series showing returns over time
            - Zero line reference in time series
            - Professional styling with proper labels
            - Responsive sizing (12x10 inches)
        
        Statistical Analysis:
            - Distribution shape: Normal, skewed, or bimodal
            - Volatility: Width of distribution (standard deviation)
            - Outliers: Extreme positive or negative returns
            - Time patterns: Clustering, trends, or cycles
        
        Risk Assessment:
            - Higher volatility = wider distribution = higher risk
            - Skewed distributions indicate asymmetric risk
            - Fat tails suggest higher probability of extreme events
            - Time clustering indicates volatility clustering
        
        Example:
            # Generate daily returns visualization
            analyzer.visualize_daily_returns()
            
            # This will show both histogram and time series
            # Top: Distribution of returns
            # Bottom: Returns over time
        
        Note:
            The first day's return will be NaN (no previous day to compare),
            so it's excluded from the histogram but shown in the time series.
        """
        # Calculate daily returns as percentage changes
        daily_returns_data = self.compute_daily_returns()
        
        # Create dual-panel figure (2 rows, 1 column)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Top panel: Histogram of daily returns distribution
        ax1.hist(daily_returns_data.dropna(), bins=50, alpha=0.7, 
                color='skyblue', edgecolor='black')
        ax1.set_title(f'{self.ticker_symbol} Daily Returns Distribution', fontsize=12)  # Reduced font size
        ax1.set_xlabel('Daily Returns (%)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.grid(True, alpha=0.3)  # Add subtle grid
        
        # Bottom panel: Time series of daily returns
        ax2.plot(self.market_data.index, daily_returns_data, 
                color='purple', linewidth=1)
        ax2.set_title(f'{self.ticker_symbol} Daily Returns Over Time', fontsize=12)  # Reduced font size
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Daily Returns (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)  # Add subtle grid
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)  # Zero line reference
        
        # Adjust layout to prevent overlap with more padding
        plt.tight_layout(pad=2.0)  # Increased padding
        plt.subplots_adjust(hspace=0.4)  # Add extra space between subplots
        plt.show()  # Display the dual-panel chart


