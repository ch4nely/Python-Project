#!/usr/bin/env python3
"""
YFinance Data Description and Demonstration

This module provides a comprehensive description and demonstration of the yfinance
data structure and capabilities. It shows what data is available, how it's structured,
and provides examples of how to access and use the data.

This is particularly useful for understanding:
- What data fields are available from Yahoo Finance
- How the data is structured in pandas DataFrames
- Data types and formats
- Available time periods and intervals
- Data quality and completeness

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# Import required libraries
import yfinance as yf  # Yahoo Finance data library
import pandas as pd  # Data manipulation library
import numpy as np  # Numerical operations
from datetime import datetime, timedelta  # Date handling
import warnings  # Warning suppression
warnings.filterwarnings('ignore')  # Suppress warnings for cleaner output


def describe_yfinance_data():
    """
    Comprehensive description and demonstration of yfinance data structure.
    
    This function demonstrates:
    - Available data fields and their meanings
    - Data structure and format
    - Data types and quality
    - Time period options
    - Data access methods
    """
    
    print("="*80)
    print("YFINANCE DATA DESCRIPTION AND DEMONSTRATION")
    print("="*80)
    
    # Create a ticker object for demonstration (using Apple stock)
    ticker_symbol = "AAPL"
    ticker = yf.Ticker(ticker_symbol)
    
    print(f"\n📊 ANALYZING DATA FOR: {ticker_symbol}")
    print("-" * 50)
    
    # Get basic stock information
    print("\n1. BASIC STOCK INFORMATION:")
    print("-" * 30)
    try:
        info = ticker.info
        print(f"Company Name: {info.get('longName', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 0):,}")
        print(f"Currency: {info.get('currency', 'N/A')}")
        print(f"Exchange: {info.get('exchange', 'N/A')}")
    except Exception as e:
        print(f"Error getting basic info: {e}")
    
    # Download historical data
    print("\n2. HISTORICAL DATA STRUCTURE:")
    print("-" * 35)
    
    # Download 1 year of data
    data = ticker.history(period="1y")
    
    print(f"Data Shape: {data.shape}")
    print(f"Date Range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"Total Trading Days: {len(data)}")
    
    print("\nData Columns Available:")
    print("-" * 25)
    for i, col in enumerate(data.columns, 1):
        print(f"{i}. {col}")
    
    print("\nColumn Descriptions:")
    print("-" * 20)
    column_descriptions = {
        'Open': 'Opening price for the trading day',
        'High': 'Highest price during the trading day',
        'Low': 'Lowest price during the trading day',
        'Close': 'Closing price for the trading day',
        'Volume': 'Number of shares traded',
        'Dividends': 'Dividend payments (if any)',
        'Stock Splits': 'Stock split information (if any)'
    }
    
    for col, desc in column_descriptions.items():
        if col in data.columns:
            print(f"• {col}: {desc}")
    
    # Show data types
    print("\nData Types:")
    print("-" * 12)
    print(data.dtypes)
    
    # Show first few rows
    print("\nFirst 5 Rows of Data:")
    print("-" * 22)
    print(data.head().round(2))
    
    # Show last few rows
    print("\nLast 5 Rows of Data:")
    print("-" * 21)
    print(data.tail().round(2))
    
    # Data quality analysis
    print("\n3. DATA QUALITY ANALYSIS:")
    print("-" * 28)
    
    print(f"Missing Values per Column:")
    missing_data = data.isnull().sum()
    for col, missing_count in missing_data.items():
        percentage = (missing_count / len(data)) * 100
        print(f"• {col}: {missing_count} missing ({percentage:.1f}%)")
    
    print(f"\nData Completeness: {((len(data) - missing_data.sum()) / (len(data) * len(data.columns))) * 100:.1f}%")
    
    # Statistical summary
    print("\n4. STATISTICAL SUMMARY:")
    print("-" * 25)
    print("Price Statistics (USD):")
    price_stats = data[['Open', 'High', 'Low', 'Close']].describe()
    print(price_stats.round(2))
    
    print("\nVolume Statistics:")
    volume_stats = data['Volume'].describe()
    print(volume_stats.round(0))
    
    # Time period options demonstration
    print("\n5. AVAILABLE TIME PERIODS:")
    print("-" * 30)
    
    time_periods = {
        '1d': '1 day',
        '5d': '5 days',
        '1mo': '1 month',
        '3mo': '3 months',
        '6mo': '6 months',
        '1y': '1 year',
        '2y': '2 years',
        '5y': '5 years',
        '10y': '10 years',
        'ytd': 'Year to date',
        'max': 'Maximum available'
    }
    
    print("Available Period Options:")
    for period, description in time_periods.items():
        print(f"• '{period}': {description}")
    
    # Demonstrate different time periods
    print("\n6. DATA AVAILABILITY BY TIME PERIOD:")
    print("-" * 40)
    
    test_periods = ['1mo', '3mo', '6mo', '1y', '2y', '5y']
    for period in test_periods:
        try:
            test_data = ticker.history(period=period)
            print(f"• {period:>3}: {len(test_data):>4} days ({test_data.index[0].strftime('%Y-%m-%d')} to {test_data.index[-1].strftime('%Y-%m-%d')})")
        except Exception as e:
            print(f"• {period:>3}: Error - {e}")
    
    # Data access examples
    print("\n7. DATA ACCESS EXAMPLES:")
    print("-" * 28)
    
    print("Accessing specific data:")
    print(f"• Current price: ${data['Close'].iloc[-1]:.2f}")
    print(f"• Highest price: ${data['High'].max():.2f}")
    print(f"• Lowest price: ${data['Low'].min():.2f}")
    print(f"• Average volume: {data['Volume'].mean():,.0f}")
    
    print("\nPrice changes:")
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    price_change_pct = (price_change / data['Close'].iloc[0]) * 100
    print(f"• Total change: ${price_change:.2f} ({price_change_pct:+.2f}%)")
    
    # Daily returns calculation
    daily_returns = data['Close'].pct_change() * 100
    print(f"• Average daily return: {daily_returns.mean():.4f}%")
    print(f"• Daily volatility: {daily_returns.std():.4f}%")
    
    # Data for different intervals
    print("\n8. AVAILABLE DATA INTERVALS:")
    print("-" * 30)
    
    intervals = {
        '1m': '1 minute (intraday only)',
        '2m': '2 minutes (intraday only)',
        '5m': '5 minutes (intraday only)',
        '15m': '15 minutes (intraday only)',
        '30m': '30 minutes (intraday only)',
        '60m': '60 minutes (intraday only)',
        '90m': '90 minutes (intraday only)',
        '1h': '1 hour (intraday only)',
        '1d': '1 day (default)',
        '5d': '5 days',
        '1wk': '1 week',
        '1mo': '1 month',
        '3mo': '3 months'
    }
    
    print("Available Interval Options:")
    for interval, description in intervals.items():
        print(f"• '{interval}': {description}")
    
    # Special data fields
    print("\n9. SPECIAL DATA FIELDS:")
    print("-" * 25)
    
    print("Dividend Information:")
    dividends = data['Dividends']
    dividend_days = dividends[dividends > 0]
    if len(dividend_days) > 0:
        print(f"• Dividend payments: {len(dividend_days)} days")
        print(f"• Total dividends: ${dividend_days.sum():.2f}")
        print(f"• Latest dividend: ${dividend_days.iloc[-1]:.2f} on {dividend_days.index[-1].strftime('%Y-%m-%d')}")
    else:
        print("• No dividend payments in this period")
    
    print("\nStock Split Information:")
    splits = data['Stock Splits']
    split_days = splits[splits > 0]
    if len(split_days) > 0:
        print(f"• Stock splits: {len(split_days)} days")
        for date, split_ratio in split_days.items():
            print(f"• {date.strftime('%Y-%m-%d')}: {split_ratio}:1 split")
    else:
        print("• No stock splits in this period")
    
    # Data limitations and considerations
    print("\n10. DATA LIMITATIONS AND CONSIDERATIONS:")
    print("-" * 45)
    
    print("Important Notes:")
    print("• Data is delayed by 15-20 minutes for free users")
    print("• Intraday data (1m, 5m, etc.) only available for recent periods")
    print("• Some stocks may have limited historical data")
    print("• Market holidays result in missing trading days")
    print("• Data quality may vary for different exchanges")
    print("• Free tier has rate limits (requests per minute)")
    
    print("\nBest Practices:")
    print("• Use appropriate time periods for your analysis")
    print("• Check for missing data before analysis")
    print("• Handle weekends and holidays appropriately")
    print("• Consider data freshness for real-time applications")
    print("• Implement error handling for network issues")
    
    # Example usage in our project
    print("\n11. USAGE IN OUR STOCK ANALYSIS PROJECT:")
    print("-" * 45)
    
    print("How we use yfinance data:")
    print("• Download historical OHLCV data for analysis")
    print("• Calculate moving averages from Close prices")
    print("• Compute daily returns for volatility analysis")
    print("• Analyze price runs using High/Low data")
    print("• Implement maximum profit algorithms")
    print("• Create visualizations from price data")
    
    print("\nData flow in our system:")
    print("1. User selects stock symbol and time period")
    print("2. yfinance downloads data from Yahoo Finance")
    print("3. Data stored in pandas DataFrame")
    print("4. Our algorithms process the data")
    print("5. Results displayed in web interface")
    
    print("\n" + "="*80)
    print("YFINANCE DATA DESCRIPTION COMPLETE")
    print("="*80)


def demonstrate_data_access():
    """
    Demonstrate various ways to access and manipulate yfinance data.
    """
    
    print("\n" + "="*60)
    print("DATA ACCESS DEMONSTRATION")
    print("="*60)
    
    # Create ticker for demonstration
    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="3mo")
    
    print(f"\n📈 DATA ACCESS EXAMPLES FOR AAPL (3 months)")
    print("-" * 50)
    
    # Basic data access
    print("1. Basic Data Access:")
    print(f"   • Latest close price: ${data['Close'].iloc[-1]:.2f}")
    print(f"   • First close price: ${data['Close'].iloc[0]:.2f}")
    print(f"   • Price range: ${data['Low'].min():.2f} - ${data['High'].max():.2f}")
    
    # Date-based access
    print("\n2. Date-Based Access:")
    print(f"   • Data starts: {data.index[0].strftime('%Y-%m-%d')}")
    print(f"   • Data ends: {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"   • Total days: {len(data)}")
    
    # Statistical access
    print("\n3. Statistical Access:")
    print(f"   • Mean close price: ${data['Close'].mean():.2f}")
    print(f"   • Median close price: ${data['Close'].median():.2f}")
    print(f"   • Standard deviation: ${data['Close'].std():.2f}")
    
    # Conditional access
    print("\n4. Conditional Access:")
    high_volume_days = data[data['Volume'] > data['Volume'].mean()]
    print(f"   • High volume days: {len(high_volume_days)}")
    print(f"   • Average volume: {data['Volume'].mean():,.0f}")
    
    # Time series operations
    print("\n5. Time Series Operations:")
    data['Price_Change'] = data['Close'].diff()
    data['Price_Change_Pct'] = data['Close'].pct_change() * 100
    print(f"   • Average daily change: ${data['Price_Change'].mean():.2f}")
    print(f"   • Average daily return: {data['Price_Change_Pct'].mean():.4f}%")
    
    # Rolling calculations
    print("\n6. Rolling Calculations:")
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    print(f"   • Current 5-day SMA: ${data['SMA_5'].iloc[-1]:.2f}")
    print(f"   • Current 20-day SMA: ${data['SMA_20'].iloc[-1]:.2f}")
    
    print("\n" + "="*60)


def show_data_structure_example():
    """
    Show a detailed example of the data structure with sample data.
    """
    
    print("\n" + "="*60)
    print("SAMPLE DATA STRUCTURE")
    print("="*60)
    
    # Get sample data
    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="5d")
    
    print(f"\n📊 SAMPLE DATA FOR AAPL (Last 5 Days)")
    print("-" * 40)
    
    # Show the actual data structure
    print("Raw Data Structure:")
    print(data)
    
    print(f"\nDataFrame Info:")
    print(f"• Shape: {data.shape}")
    print(f"• Index type: {type(data.index)}")
    print(f"• Columns: {list(data.columns)}")
    
    print(f"\nData Types:")
    for col in data.columns:
        print(f"• {col}: {data[col].dtype}")
    
    print(f"\nSample Values:")
    for col in data.columns:
        if col in ['Open', 'High', 'Low', 'Close']:
            print(f"• {col}: ${data[col].iloc[-1]:.2f}")
        elif col == 'Volume':
            print(f"• {col}: {data[col].iloc[-1]:,.0f}")
        else:
            print(f"• {col}: {data[col].iloc[-1]}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    """
    Main execution block for yfinance data description.
    
    This script provides comprehensive information about yfinance data structure,
    capabilities, and usage examples. It's designed to help understand what data
    is available and how to work with it effectively.
    """
    
    try:
        # Run the main description
        describe_yfinance_data()
        
        # Demonstrate data access methods
        demonstrate_data_access()
        
        # Show sample data structure
        show_data_structure_example()
        
        print("\n🎉 YFINANCE DATA DESCRIPTION COMPLETE!")
        print("This script demonstrates all aspects of yfinance data structure and usage.")
        
    except Exception as e:
        print(f"\n❌ Error running yfinance data description: {e}")
        print("Please check your internet connection and try again.")
