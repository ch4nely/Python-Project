#!/usr/bin/env python3
"""
Comprehensive Demo and Validation Tool for Stock Analysis System

This script provides a complete demonstration and validation platform for the
FinancialTrendAnalyzer system. It combines interactive demonstrations, comprehensive
testing, and educational content into a single, user-friendly interface.

Key Features:
- Interactive demo with user choice of stocks and time periods
- Comprehensive validation testing with detailed results
- Multi-stock analysis with comparative insights
- Educational content explaining algorithms and concepts
- Automatic dependency management and setup
- Professional visualization and reporting

The demo tool serves multiple purposes:
1. Educational: Teaches users about financial analysis concepts
2. Validation: Proves algorithm correctness with test cases
3. Demonstration: Shows all system capabilities
4. Testing: Provides comprehensive testing framework

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# Auto-install dependencies if missing - ensures all required packages are available
from package.dependency_manager import ensure_dependencies
ensure_dependencies()

# Import core analysis components
from combined_analyzer import FinancialTrendAnalyzer  # Main analysis class with all functionality
from validation import validate_all_calculations  # Comprehensive validation testing

# Import visualization and data processing libraries
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better display compatibility
import matplotlib.pyplot as plt  # Primary plotting library
import pandas as pd  # Data manipulation and analysis
import numpy as np  # Numerical computations
import seaborn as sns  # Enhanced matplotlib styling and statistical plots


def show_main_menu():
    """
    Display the main menu with all available options.
    
    This function presents the user with a clear, formatted menu showing
    all available demo and validation options. It provides a professional
    interface for navigating the different functionalities of the system.
    
    Menu Options:
        1. Interactive Demo: User chooses stocks and sees plots
        2. Validation Tests Only: Run comprehensive algorithm testing
        3. Comprehensive Demo: Full automated demonstration
        4. Exit: Close the application
    
    The menu uses visual separators and emojis to make it user-friendly
    and easy to navigate.
    """
    print("\n" + "="*80)
    print("🎯 STOCK ANALYSIS - DEMO & VALIDATION TOOL")
    print("="*80)
    print("\nChoose what you'd like to do:")
    print("\n1. 🎮 Interactive Demo (Choose Stocks + See Plots)")
    print("2. 🔍 Run Validation Tests Only")
    print("3. 📊 Run Comprehensive Demo (All Features)")
    print("4. 🚪 Exit")
    print("\n" + "="*80)


def run_validation_only():
    """
    Execute comprehensive validation tests to verify algorithm correctness.
    
    This function runs all validation tests to ensure that every algorithm
    in the FinancialTrendAnalyzer is working correctly. It provides detailed
    information about what tests are being performed and what they validate.
    
    Validation Coverage:
        - SMA validation against pandas reference implementation
        - Daily returns validation against pandas pct_change()
        - Runs analysis validation with real stock data
        - Synthetic data validation with known expected results
        - Max profit algorithm validation with simple test cases
        - Edge case testing for error handling
    
    The function provides educational context about what each test validates
    and why it's important for ensuring algorithm correctness.
    """
    print("\n🔍 RUNNING VALIDATION TESTS")
    print("-" * 50)
    print("""
    📋 VALIDATION TESTS INCLUDE:
    • SMA validation against pandas reference
    • Daily returns validation against pandas pct_change()
    • Runs analysis validation with real stock data
    • Synthetic data validation for runs/streaks (known expected results)
    • Max profit algorithm validation with simple test case
    • Edge case testing:
      - SMA window > dataset length
      - Insufficient data handling
      - Error handling verification
    
    🎯 EDGE CASES TESTED:
    • Window size validation (positive, not exceeding data length)
    • NaN value handling in all calculations
    • Insufficient data scenarios (< 2 days for max profit)
    • Zero-change days in runs analysis
    """)
    validate_all_calculations()


def run_comprehensive_demo():
    """
    Execute a complete automated demonstration of all system capabilities.
    
    This function provides a comprehensive showcase of the entire FinancialTrendAnalyzer
    system, including validation testing, multi-stock analysis, detailed reporting,
    and educational content. It demonstrates the full range of capabilities in
    a structured, educational format.
    
    Demo Components:
        1. Validation Testing: Ensures all algorithms work correctly
        2. Multi-Stock Analysis: Analyzes multiple popular stocks
        3. Detailed Analysis: Deep dive into Apple stock with comprehensive report
        4. Algorithm Explanations: Educational content about financial concepts
        5. Key Insights: Comparative analysis and market insights
    
    The demo is designed to be educational, showing users how to interpret
    financial data and understand the algorithms behind the analysis.
    """
    print("\n" + "="*80)
    print("STOCK MARKET TREND ANALYSIS - COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    
    # Step 1: Run validation tests
    print("\n🔍 STEP 1: Running Validation Tests")
    print("-" * 50)
    print("Testing all algorithms including edge cases and synthetic data validation...")
    validate_all_calculations()
    
    # Step 2: Analyze multiple stocks
    print("\n📊 STEP 2: Multi-Stock Analysis")
    print("-" * 50)
    
    stocks_to_analyze = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    for symbol in stocks_to_analyze:
        try:
            print(f"\nAnalyzing {symbol}...")
            analyzer = FinancialTrendAnalyzer(symbol, "1y")
            
            # Quick stats
            runs = analyzer.analyze_price_runs()
            max_profit, transactions = analyzer.calculate_maximum_profit()
            returns = analyzer.compute_daily_returns()
            
            print(f"  📈 Current Price: ${analyzer.market_data['Close'].iloc[-1]:.2f}")
            print(f"  📊 Price Range: ${analyzer.market_data['Close'].min():.2f} - ${analyzer.market_data['Close'].max():.2f}")
            print(f"  🔥 Longest Upward Streak: {runs['longest_upward_streak']} days")
            print(f"  📉 Longest Downward Streak: {runs['longest_downward_streak']} days")
            print(f"  💰 Max Possible Profit: ${max_profit:.2f}")
            print(f"  📈 Average Daily Return: {returns.mean():.4f}%")
            print(f"  📊 Volatility (Std Dev): {returns.std():.4f}%")
            
        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")
    
    # Step 3: Detailed analysis of one stock
    print("\n🔬 STEP 3: Detailed Analysis - Apple Inc. (AAPL)")
    print("-" * 50)
    
    try:
        analyzer = FinancialTrendAnalyzer("AAPL", "2y")
        analyzer.create_comprehensive_report(sma_window=20)
        
        # Show detailed transaction analysis
        max_profit, transaction_pairs = analyzer.calculate_maximum_profit()
        print(f"\n💼 DETAILED TRANSACTION ANALYSIS:")
        print(f"Total Transactions: {len(transaction_pairs)}")
        print(f"Average Profit per Transaction: ${max_profit/len(transaction_pairs):.2f}" if transaction_pairs else "No transactions")
        
        if transaction_pairs:
            print(f"\nFirst 10 Transactions:")
            print("-" * 80)
            print(f"{'#':<3} {'Buy Date':<12} {'Buy Price':<10} {'Sell Date':<12} {'Sell Price':<10} {'Profit':<10}")
            print("-" * 80)
            
            for i, (buy_idx, sell_idx) in enumerate(transaction_pairs[:10], 1):
                buy_date = analyzer.market_data.index[buy_idx].strftime('%Y-%m-%d')
                sell_date = analyzer.market_data.index[sell_idx].strftime('%Y-%m-%d')
                buy_price = analyzer.market_data['Close'].iloc[buy_idx]
                sell_price = analyzer.market_data['Close'].iloc[sell_idx]
                profit = sell_price - buy_price
                
                print(f"{i:<3} {buy_date:<12} ${buy_price:<9.2f} {sell_date:<12} ${sell_price:<9.2f} ${profit:<9.2f}")
        
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
    
    # Step 4: Algorithm explanation
    print("\n🔬 STEP 4: Algorithm Explanations")
    print("-" * 50)
    print("""
    📊 SIMPLE MOVING AVERAGE (SMA):
    • Formula: SMA = (P1 + P2 + ... + Pn) / n
    • Purpose: Smooths out price fluctuations to show trend direction
    • Example: 20-day SMA averages the last 20 closing prices
    • Interpretation: Price above SMA = bullish trend, below = bearish trend
    
    📈 DAILY RETURNS CALCULATION:
    • Formula: Return = ((Today's Price - Yesterday's Price) / Yesterday's Price) × 100
    • Purpose: Measures daily percentage change in stock price
    • Use: Risk assessment and volatility analysis
    • Example: Stock goes from $100 to $105 = 5% daily return
    
    🔥 RUNS ANALYSIS:
    • Purpose: Identifies consecutive days of price increases or decreases
    • Method: Counts consecutive days where price moves in same direction
    • Use: Trend strength and momentum analysis
    • Example: 5-day upward run = 5 consecutive days of price increases
    
    💰 MAXIMUM PROFIT ALGORITHM:
    • Purpose: Finds optimal buy/sell points for maximum profit
    • Method: Dynamic programming approach
    • Logic: Buy at local minimums, sell at local maximums
    • Complexity: O(n) time complexity for n data points
    
    🛡️ EDGE CASE HANDLING:
    • SMA Window > Data Length: Raises ValueError with clear message
    • Insufficient Data (< 2 days): Returns zero profit, empty transactions
    • NaN Values: Automatically excluded from calculations
    • Zero-Change Days: Excluded from runs analysis (no direction)
    • Invalid Window Sizes: Validates positive integers only
    
    🎯 KEY INSIGHTS:
    • Volatility: Higher standard deviation = more price fluctuation
    • Trend Strength: Longer runs indicate stronger momentum
    • Profit Potential: Maximum profit shows theoretical best-case scenario
    • Risk Assessment: Higher volatility = higher risk/reward potential
    """)
    
    # Step 5: Key insights
    print("\n🎯 STEP 5: Key Insights")
    print("-" * 50)
    try:
        insights = []
        for symbol in ["AAPL", "GOOGL", "MSFT"]:
            try:
                analyzer = FinancialTrendAnalyzer(symbol, "1y")
                runs = analyzer.analyze_price_runs()
                max_profit, _ = analyzer.calculate_maximum_profit()
                returns = analyzer.compute_daily_returns()
                insights.append({
                    'symbol': symbol,
                    'volatility': returns.std(),
                    'max_profit': max_profit,
                    'longest_up': runs['longest_upward_streak'],
                    'longest_down': runs['longest_downward_streak']
                })
            except:
                continue
        if insights:
            print("📊 VOLATILITY COMPARISON:")
            for insight in sorted(insights, key=lambda x: x['volatility'], reverse=True):
                print(f"  {insight['symbol']}: {insight['volatility']:.2f}% daily volatility")
            print("\n💰 PROFIT POTENTIAL:")
            for insight in sorted(insights, key=lambda x: x['max_profit'], reverse=True):
                print(f"  {insight['symbol']}: ${insight['max_profit']:.2f} max possible profit")
            print("\n🔥 TREND STRENGTH:")
            for insight in insights:
                print(f"  {insight['symbol']}: {insight['longest_up']} day up streak, {insight['longest_down']} day down streak")
    except Exception as e:
        print(f"Error generating insights: {e}")
    print("\n" + "="*80)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("="*80)
    print("""
    This project demonstrates:
    ✅ Real-time stock data fetching with yfinance
    ✅ Technical analysis calculations (SMA, runs, returns)
    ✅ Advanced algorithm implementation (max profit optimization)
    ✅ Comprehensive data visualization
    ✅ Robust validation and testing
    ✅ Professional code structure and documentation
    
    The tool is ready for educational use and can be extended
    with additional technical indicators and analysis methods.
    """)


def run_interactive_demo_with_plots():
    """
    Execute an interactive demonstration where users choose stocks and see visualizations.
    
    This function provides an interactive experience where users can:
    - Choose from popular tech stocks or enter their own stock symbols
    - Select different time periods for analysis
    - View comprehensive analysis results for each stock
    - See professional visualizations including price charts, runs analysis, and returns
    
    Interactive Features:
        - Stock selection: Popular tech stocks or custom input
        - Time period selection: 1y, 2y, 3y, 5y, or max
        - Real-time analysis: Immediate results and statistics
        - Professional visualizations: Price charts, runs, and returns
        - User-friendly interface: Clear prompts and error handling
    
    The function handles user input validation and provides helpful error messages
    for invalid stock symbols or other issues.
    """
    print("\n🎮 INTERACTIVE DEMO WITH PLOTS")
    print("-" * 50)
    while True:
        print("\nChoose stocks to analyze:")
        print("1. Popular Tech Stocks (AAPL, GOOGL, MSFT, TSLA, AMZN)")
        print("2. Enter Your Own Stocks")
        print("3. Return to Main Menu")
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == "1":
            stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
            print(f"\nAnalyzing popular tech stocks: {', '.join(stocks)}")
            break
        elif choice == "2":
            print("\nEnter stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT or just AAPL):")
            stock_input = input("Stocks: ").strip().upper()
            stocks = [s.strip() for s in stock_input.split(',') if s.strip()]
            if not stocks:
                print("❌ No valid stocks entered. Please try again.")
                continue
            print(f"\nAnalyzing your stocks: {', '.join(stocks)}")
            break
        elif choice == "3":
            print("Returning to main menu...")
            return
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            continue
    print("\nChoose time period:")
    print("1. 1 year")
    print("2. 2 years") 
    print("3. 3 years")
    print("4. 5 years")
    print("5. Maximum available")
    while True:
        period_choice = input("\nEnter your choice (1-5): ").strip()
        if period_choice == "1":
            period = "1y"
            break
        elif period_choice == "2":
            period = "2y"
            break
        elif period_choice == "3":
            period = "3y"
            break
        elif period_choice == "4":
            period = "5y"
            break
        elif period_choice == "5":
            period = "max"
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")
    for symbol in stocks:
        try:
            print(f"\n📊 Analyzing {symbol} ({period})...")
            analyzer = FinancialTrendAnalyzer(symbol, period)
            runs = analyzer.analyze_price_runs()
            max_profit, _ = analyzer.calculate_maximum_profit()
            returns = analyzer.compute_daily_returns()
            print(f"  📈 Current Price: ${analyzer.market_data['Close'].iloc[-1]:.2f}")
            print(f"  📊 Price Range: ${analyzer.market_data['Close'].min():.2f} - ${analyzer.market_data['Close'].max():.2f}")
            print(f"  🔥 Longest Upward Streak: {runs['longest_upward_streak']} days")
            print(f"  📉 Longest Downward Streak: {runs['longest_downward_streak']} days")
            print(f"  💰 Max Possible Profit: ${max_profit:.2f}")
            print(f"  📈 Average Daily Return: {returns.mean():.4f}%")
            print(f"  📊 Volatility: {returns.std():.4f}%")
            print(f"\n📈 Generating plots for {symbol}...")
            print("  📊 Displaying Price & Moving Average Chart...")
            analyzer.visualize_price_and_sma(20)
            input("  Press Enter to continue to next plot...")
            print("  🔥 Displaying Runs Analysis Chart...")
            analyzer.visualize_price_runs()
            input("  Press Enter to continue to next plot...")
            print("  📈 Displaying Daily Returns Chart...")
            analyzer.visualize_daily_returns()
            input("  Press Enter to continue...")
            print(f"✅ All plots displayed for {symbol}")
        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")
    print(f"\n🎉 Interactive demo completed! Analyzed {len(stocks)} stock(s) with plots.")


def main():
    """
    Main application entry point with comprehensive user interface.
    
    This function serves as the primary entry point for the demo and validation tool.
    It provides a continuous loop interface where users can navigate between different
    options and run various demonstrations and validations.
    
    Application Flow:
        1. Display welcome message and main menu
        2. Process user input and route to appropriate function
        3. Handle user choices with proper error handling
        4. Provide option to return to main menu or exit
        5. Graceful exit with thank you message
    
    The function includes comprehensive error handling for invalid user input
    and provides a user-friendly experience with clear prompts and feedback.
    """
    print("🎯 STOCK ANALYSIS - DEMO & VALIDATION TOOL")
    print("Welcome! This tool demonstrates all features of the stock analysis system.")
    while True:
        show_main_menu()
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            run_interactive_demo_with_plots()
        elif choice == "2":
            run_validation_only()
        elif choice == "3":
            run_comprehensive_demo()
        elif choice == "4":
            print("\n👋 Thank you for using the Stock Analysis Demo & Validation Tool!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-4.")
        if choice in ["1", "2", "3"]:
            continue_choice = input("\nWould you like to return to the main menu? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Thank you for using the Stock Analysis Demo & Validation Tool!")
                break


if __name__ == "__main__":
    try:
        plt.style.use('seaborn-v0_8')
    except OSError:
        plt.style.use('default')
    plt.ion()
    main()


