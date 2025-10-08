"""
Stock Market Trend Analysis Reporting

This module provides comprehensive reporting functionality for the FinancialTrendAnalyzer.
It extends the combined analyzer with a detailed reporting method that generates
professional-quality analysis reports suitable for both technical and business audiences.

Key Features:
- Comprehensive analysis reports with formatted output
- Integration of all analysis methods (SMA, runs, returns, max profit)
- Professional formatting with clear sections and metrics
- Transaction analysis with detailed buy/sell information
- CLI-style main function for standalone execution

The reporting module demonstrates how to combine all analysis capabilities into
a single, easy-to-use interface for generating complete stock analysis reports.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import matplotlib.pyplot as plt  # For generating visualizations in reports
from combined_analyzer import FinancialTrendAnalyzer as CombinedAnalyzer  # Import the composite analyzer
from validation import validate_all_calculations  # Import validation for testing


class FinancialTrendAnalyzer(CombinedAnalyzer):
    """
    Extended FinancialTrendAnalyzer with comprehensive reporting capabilities.
    
    This class extends the composite FinancialTrendAnalyzer by adding a comprehensive
    reporting method that generates detailed analysis reports. It combines all analysis
    methods into a single, professional report format suitable for various audiences.
    
    Additional Methods:
        - create_comprehensive_report(): Generates detailed analysis report
    
    Report Features:
        - Executive summary with key metrics
        - Technical analysis with moving averages
        - Statistical analysis with runs and returns
        - Profit analysis with transaction details
        - Professional formatting and clear sections
    
    Example Usage:
        # Create analyzer and generate comprehensive report
        analyzer = FinancialTrendAnalyzer("AAPL", "2y")
        analyzer.create_comprehensive_report(sma_window=20)
        
        # Generate visualizations
        analyzer.visualize_price_and_sma(20)
        analyzer.visualize_price_runs()
        analyzer.visualize_daily_returns()
    """
    
    def create_comprehensive_report(self, sma_window: int = 20):  # REPORT FUNCTION
        """
        Generate and display a comprehensive analysis report for the current ticker.
        
        This method creates a detailed, professional-quality report that combines
        all analysis capabilities into a single, easy-to-read format. The report
        includes executive summary, technical analysis, statistical analysis,
        and profit analysis sections.
        
        Args:
            sma_window (int): Window size for Simple Moving Average calculation.
                             Defaults to 20 days (approximately 1 month of trading).
                             Common values: 5, 10, 20, 50, 100, 200 days
        
        Report Sections:
            1. Executive Summary: Basic stock information and current metrics
            2. Technical Analysis: Moving average analysis and trend indicators
            3. Runs Analysis: Consecutive price movement patterns
            4. Daily Returns Analysis: Statistical analysis of price changes
            5. Profit Analysis: Maximum profit potential and transaction details
        
        Output Format:
            - Formatted console output with clear sections
            - Professional styling with separators and headers
            - Detailed metrics with proper formatting
            - Transaction analysis with dates and prices
        
        Example:
            # Generate report for Apple stock with 20-day SMA
            analyzer = FinancialTrendAnalyzer("AAPL", "1y")
            analyzer.create_comprehensive_report(sma_window=20)
            
            # Generate report with different SMA window
            analyzer.create_comprehensive_report(sma_window=50)
        
        Note:
            The report combines data from all analysis methods, so it provides
            a complete picture of the stock's performance and characteristics.
        """
        # Print report header with stock symbol
        print(f"\n{'='*60}")
        print(f"STOCK ANALYSIS REPORT FOR {self.ticker_symbol}")
        print(f"{'='*60}")
        
        # Executive Summary Section
        print(f"\nData Period: {self.market_data.index[0].strftime('%Y-%m-%d')} to {self.market_data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(self.market_data)}")
        print(f"Current Price: ${self.market_data['Close'].iloc[-1]:.2f}")
        print(f"Price Range: ${self.market_data['Close'].min():.2f} - ${self.market_data['Close'].max():.2f}")
        
        # Technical Analysis Section
        sma_values = self.calculate_simple_moving_average(sma_window)
        current_sma_value = sma_values.iloc[-1]
        print(f"\nSimple Moving Average ({sma_window} days): ${current_sma_value:.2f}")
        
        # Runs Analysis Section
        runs_data = self.analyze_price_runs()
        print(f"\nRUNS ANALYSIS:")
        print(f"Total Upward Days: {runs_data['total_upward_days']}")
        print(f"Total Downward Days: {runs_data['total_downward_days']}")
        print(f"Longest Upward Streak: {runs_data['longest_upward_streak']} days")
        print(f"Longest Downward Streak: {runs_data['longest_downward_streak']} days")
        print(f"Number of Upward Runs: {runs_data['upward_run_count']}")
        print(f"Number of Downward Runs: {runs_data['downward_run_count']}")
        
        # Daily Returns Analysis Section
        daily_returns_data = self.compute_daily_returns()
        print(f"\nDAILY RETURNS ANALYSIS:")
        print(f"Average Daily Return: {daily_returns_data.mean():.4f}%")
        print(f"Standard Deviation: {daily_returns_data.std():.4f}%")
        print(f"Best Day: {daily_returns_data.max():.4f}%")
        print(f"Worst Day: {daily_returns_data.min():.4f}%")
        
        # Maximum Profit Analysis Section
        max_profit_value, transaction_pairs = self.calculate_maximum_profit()
        print(f"\nMAXIMUM PROFIT ANALYSIS:")
        print(f"Maximum Possible Profit: ${max_profit_value:.2f}")
        print(f"Number of Transactions: {len(transaction_pairs)}")
        
        # Transaction Details Section
        if transaction_pairs:
            print("Buy/Sell Pairs (Index, Date):")
            # Display first 5 transactions with detailed information
            for buy_idx, sell_idx in transaction_pairs[:5]:
                buy_date = self.market_data.index[buy_idx].strftime('%Y-%m-%d')
                sell_date = self.market_data.index[sell_idx].strftime('%Y-%m-%d')
                buy_price = self.market_data['Close'].iloc[buy_idx]
                sell_price = self.market_data['Close'].iloc[sell_idx]
                profit = sell_price - buy_price
                print(f"  Buy: {buy_date} (${buy_price:.2f}) -> Sell: {sell_date} (${sell_price:.2f}) | Profit: ${profit:.2f}")


if __name__ == "__main__":
    """
    Main execution block for standalone reporting functionality.
    
    This section allows the reporting module to be run independently,
    providing a complete demonstration of the analysis capabilities.
    It includes validation testing and comprehensive analysis of a sample stock.
    
    Execution Flow:
        1. Run validation tests to ensure algorithm correctness
        2. Create analyzer for Apple stock (AAPL) with 2 years of data
        3. Generate comprehensive report with 20-day SMA
        4. Create visualizations for complete analysis
    
    Usage:
        # Run from command line
        python reporting.py
        
        # This will execute validation tests and generate a complete analysis report
    """
    print("Stock Market Trend Analysis Tool")
    print("=" * 40)
    
    # Run validation tests to ensure all algorithms are working correctly
    validate_all_calculations()
    
    try:
        # Create analyzer for Apple stock with 2 years of data
        analyzer = FinancialTrendAnalyzer("AAPL", "2y")
        
        # Generate comprehensive report with 20-day moving average
        analyzer.create_comprehensive_report(sma_window=20)
        
        # Generate visualizations for complete analysis
        print("\nGenerating visualizations...")
        analyzer.visualize_price_and_sma(sma_window=20)
        analyzer.visualize_price_runs()
        analyzer.visualize_daily_returns()
        
    except Exception as e:
        print(f"Error during analysis: {e}")


