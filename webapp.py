"""
Stock Analysis Web App
This is a simple web application using Streamlit for stock market analysis

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# Auto-install dependencies if missing
from package.dependency_manager import ensure_dependencies
ensure_dependencies()

import streamlit as st  # For creating the web interface
import pandas as pd     # For working with data
import matplotlib.pyplot as plt  # For creating charts
import plotly.express as px  # For interactive charts
from combined_analyzer import FinancialTrendAnalyzer
from validation import validate_all_calculations  # Import validation function

# Set the page title and icon
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📈",
    layout="wide"
)

# Create the main title
st.title("📈 Stock Market Analysis Tool")
st.write("Simple tool to analyze stock market trends and patterns")

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Stock Analysis", "Help"])

if page == "Stock Analysis":
    # Main stock analysis page
    st.header("📊 Analyze Stock Data")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        # Popular stock suggestions
        popular_stocks = {
            "AAPL": "Apple Inc.",
            "GOOGL": "Google (Alphabet)",
            "MSFT": "Microsoft",
            "TSLA": "Tesla",
            "AMZN": "Amazon",
            "META": "Meta (Facebook)",
            "NFLX": "Netflix",
            "NVDA": "NVIDIA",
            "JPM": "JPMorgan Chase",
            "JNJ": "Johnson & Johnson",
            "V": "Visa",
            "PG": "Procter & Gamble"
        }
        
        # Single text input for stock symbol
        symbol = st.text_input(
            "Stock Symbol:",
            placeholder="e.g., AAPL, GOOGL, MSFT",
            help="Enter any valid stock symbol. Popular stocks: " + ", ".join(popular_stocks.keys()),
            value="AAPL"  # Default to Apple
        ).upper().strip()
        
        # Show popular stock suggestions
        st.caption("💡 Popular stocks: " + ", ".join([f"{k} ({v})" for k, v in list(popular_stocks.items())[:6]]))
    
    with col2:
        # Dropdown for time period
        period = st.selectbox(
            "Select Time Period:",
            ["1y", "2y", "3y", "5y", "max"],
            help="Choose how much historical data to download"
        )
    
    # Button to analyze the stock
    analyze_button = st.button("🔍 Analyze Stock", type="primary")
    
    if analyze_button:
        try:
            # Show a loading spinner
            with st.spinner("Downloading stock data..."):
                # Create FinancialTrendAnalyzer instance
                analyzer = FinancialTrendAnalyzer(symbol.upper(), period)
                data = analyzer.market_data
            
            # Display success message
            st.success(f"Successfully downloaded {len(data)} days of data for {symbol.upper()}")
            
            # Store analyzer in session state for interactive updates
            st.session_state['analyzer'] = analyzer
            st.session_state['stock_symbol'] = symbol.upper()
            st.session_state['time_period'] = period
            
        except Exception as e:
            # Show error message if something goes wrong
            st.error(f"Error analyzing stock: {str(e)}")
    
    # Check if we have analyzer to display
    if 'analyzer' in st.session_state:
        analyzer = st.session_state['analyzer']
        data = analyzer.market_data
        symbol = st.session_state['stock_symbol']
        period = st.session_state['time_period']
        
        # Create tabs for different analysis
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Price Chart", "📊 Statistics", "📉 Returns", "💰 Profit Analysis", "🔥 Runs Analysis", "🔍 Validation Tests"])
        
        with tab1:
            # Price chart tab
            st.subheader("Stock Price Chart")
            
            # Display current settings
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Stock Symbol", symbol)
            with col2:
                st.metric("Time Period", period)
            
            # Interactive moving average slider
            st.write("**Adjust Moving Average Window:**")
            interactive_sma_window = st.slider(
                "Moving Average Days:",
                min_value=5,
                max_value=min(100, len(data)),
                value=20,  # Default to 20 days
                step=1,
                key="interactive_sma",
                help="Slide to change the moving average window in real-time"
            )
            
            # Calculate moving average using the interactive window
            sma = analyzer.calculate_simple_moving_average(interactive_sma_window)
            
            # Create the chart
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data.index, data['Close'], label=f'{symbol} Price', linewidth=2, color='blue')
            ax.plot(data.index, sma, label=f'SMA({interactive_sma_window})', linewidth=2, alpha=0.8, color='red')
            ax.set_title(f'{symbol} Stock Price and Moving Average ({interactive_sma_window} days)')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Display the chart
            st.pyplot(fig)
            
            # Show some statistics about the moving average
            st.write("**Moving Average Statistics:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current SMA", f"${sma.iloc[-1]:.2f}")
            with col2:
                st.metric("SMA Min", f"${sma.min():.2f}")
            with col3:
                st.metric("SMA Max", f"${sma.max():.2f}")
            
        with tab2:
            # Statistics tab
            st.subheader("Stock Statistics")
            
            # Calculate basic statistics
            current_price = data['Close'].iloc[-1]
            price_range = f"${data['Close'].min():.2f} - ${data['Close'].max():.2f}"
            
            # Display statistics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Price", f"${current_price:.2f}")
                st.metric("Price Range", price_range)
            
            with col2:
                st.metric("Total Days", len(data))
                st.metric("Start Date", data.index[0].strftime('%Y-%m-%d'))
            
            with col3:
                st.metric("End Date", data.index[-1].strftime('%Y-%m-%d'))
                st.metric("Average Volume", f"{data['Volume'].mean():,.0f}")
        
        with tab3:
            # Returns analysis tab
            st.subheader("Daily Returns Analysis")
            
            # Calculate daily returns
            returns = analyzer.compute_daily_returns()
            
            # Display returns statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Average Daily Return", f"{returns.mean():.4f}%")
                st.metric("Best Day", f"{returns.max():.4f}%")
            
            with col2:
                st.metric("Worst Day", f"{returns.min():.4f}%")
                st.metric("Volatility (Std Dev)", f"{returns.std():.4f}%")
            
            # Create returns chart
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data.index, returns, color='purple', linewidth=1)
            ax.set_title(f'{symbol} Daily Returns')
            ax.set_xlabel('Date')
            ax.set_ylabel('Daily Returns (%)')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
            
            # Display the returns chart
            st.pyplot(fig)
        
        with tab4:
            # Profit analysis tab
            st.subheader("Maximum Profit Analysis")
            
            # Calculate maximum profit
            max_profit, _ = analyzer.calculate_maximum_profit()
            
            # Display profit information
            st.metric("Maximum Possible Profit", f"${max_profit:.2f}")
            
            # Calculate runs analysis
            runs = analyzer.analyze_price_runs()
            
            # Display runs statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Upward Days", runs['total_upward_days'])
                st.metric("Longest Upward Streak", f"{runs['longest_upward_streak']} days")
            
            with col2:
                st.metric("Downward Days", runs['total_downward_days'])
                st.metric("Longest Downward Streak", f"{runs['longest_downward_streak']} days")
        
        with tab5:
            # Runs analysis tab with visualization
            st.subheader("Price Runs Analysis")
            
            # Calculate runs data
            runs_data = analyzer.analyze_price_runs()
            
            # Display runs statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Upward Days", runs_data['total_upward_days'])
                st.metric("Number of Upward Runs", runs_data['upward_run_count'])
            
            with col2:
                st.metric("Total Downward Days", runs_data['total_downward_days'])
                st.metric("Number of Downward Runs", runs_data['downward_run_count'])
            
            with col3:
                st.metric("Longest Upward Streak", f"{runs_data['longest_upward_streak']} days")
                st.metric("Longest Downward Streak", f"{runs_data['longest_downward_streak']} days")
            
            # Create runs visualization
            st.write("**Price Chart with Upward (Green) and Downward (Red) Runs Highlighted:**")
            
            # Calculate price changes for coloring
            daily_price_changes = data['Close'].diff()
            
            # Create the chart
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # Plot the main price line
            ax.plot(data.index, data['Close'], color='black', linewidth=1, alpha=0.7, label=f'{symbol} Price')
            
            # Plot colored segments for runs
            for i in range(1, len(data)):
                change = daily_price_changes.iloc[i]
                if change > 0:  # Upward day
                    ax.plot([data.index[i-1], data.index[i]], 
                           [data['Close'].iloc[i-1], data['Close'].iloc[i]], 
                           color='green', linewidth=3, alpha=0.8)
                elif change < 0:  # Downward day
                    ax.plot([data.index[i-1], data.index[i]], 
                           [data['Close'].iloc[i-1], data['Close'].iloc[i]], 
                           color='red', linewidth=3, alpha=0.8)
                # Skip zero changes (no change days)
            
            ax.set_title(f'{symbol} Stock Price with Upward (Green) and Downward (Red) Runs')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Display the chart
            st.pyplot(fig)
            
            # Add explanation
            st.info("""
            **How to Read This Chart:**
            - **Green segments**: Consecutive days where the stock price increased
            - **Red segments**: Consecutive days where the stock price decreased
            - **Black line**: Overall price trend
            - Longer green/red segments indicate stronger momentum in that direction
            """)
            
            # Show detailed runs information
            st.write("**Detailed Runs Information:**")
            
            # Create a summary table
            runs_summary = {
                'Metric': [
                    'Total Upward Days',
                    'Total Downward Days', 
                    'Number of Upward Runs',
                    'Number of Downward Runs',
                    'Longest Upward Streak (days)',
                    'Longest Downward Streak (days)',
                    'Average Upward Run Length',
                    'Average Downward Run Length'
                ],
                'Value': [
                    str(runs_data['total_upward_days']),
                    str(runs_data['total_downward_days']),
                    str(runs_data['upward_run_count']),
                    str(runs_data['downward_run_count']),
                    str(runs_data['longest_upward_streak']),
                    str(runs_data['longest_downward_streak']),
                    f"{runs_data['total_upward_days'] / runs_data['upward_run_count']:.1f}" if runs_data['upward_run_count'] > 0 else "0",
                    f"{runs_data['total_downward_days'] / runs_data['downward_run_count']:.1f}" if runs_data['downward_run_count'] > 0 else "0"
                ]
            }
            
            runs_df = pd.DataFrame(runs_summary)
            st.dataframe(runs_df, width='stretch')

        with tab6:
            # Validation Tests tab
            st.subheader("🔍 Validation Tests")
            
            st.write("""
            This tab demonstrates how our algorithms are validated against trusted sources and known test cases.
            Each validation test ensures our implementation produces correct results.
            """)
            
            # Initialize validation state in session state
            if 'validation_completed' not in st.session_state:
                st.session_state['validation_completed'] = False
            if 'validation_output' not in st.session_state:
                st.session_state['validation_output'] = ""
            
            # Use a form to prevent page refresh and tab jumping
            with st.form("validation_form", clear_on_submit=False):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    run_validation = st.form_submit_button("🧪 Run All Validation Tests", type="primary", use_container_width=True)
            
            # Run validation if button was clicked
            if run_validation:
                with st.spinner("Running validation tests... This may take a moment."):
                    # Capture the output from validate_all_calculations
                    import io
                    import contextlib
                    
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        validate_all_calculations()
                    
                    # Store results in session state
                    st.session_state['validation_output'] = f.getvalue()
                    st.session_state['validation_completed'] = True
                
                # Show completion message
                st.success("🎉 **All validation tests completed!**")
            
            # Display validation results if they exist
            if st.session_state['validation_completed'] and st.session_state['validation_output']:
                st.subheader("📋 Validation Test Results")
                
                # Display the captured output in a nice format
                st.code(st.session_state['validation_output'], language="text")
                
                # Add explanation section
                st.info("""
                **What These Tests Prove:**
                - Our SMA calculation matches pandas (industry standard)
                - Our daily returns formula is mathematically correct
                - Our runs analysis logic counts correctly
                - Our synthetic data tests verify algorithm correctness
                - Our max profit algorithm implements the optimal strategy
                - Our edge case handling prevents invalid operations
                
                These validations ensure our stock analysis tool produces reliable, accurate results.
                """)
                
                # Add a button to clear results
                if st.button("🗑️ Clear Results", type="secondary"):
                    st.session_state['validation_completed'] = False
                    st.session_state['validation_output'] = ""
                    st.rerun()

elif page == "Help":
    # Help page
    st.header("❓ Help and Instructions")
    
    st.subheader("How to Use This Tool:")
    
    st.write("""
    **How to Use This Tool:**
    
    **1. Enter Stock Symbol:**
    - Type any stock symbol (AAPL, GOOGL, MSFT, TSLA, etc.)
    - Popular suggestions are shown below the input field
    - Case doesn't matter - AAPL, aapl, and Apple all work
    
    **2. Choose Time Period:**
    - Select how much historical data you want (1 year, 2 years, etc.)
    
    **3. Analyze:**
    - Click the "🔍 Analyze Stock" button
    - View results in different tabs:
        - Price Chart: Shows stock price and moving average (with interactive slider)
        - Statistics: Basic stock information
        - Returns: Daily percentage changes
        - Profit Analysis: Maximum profit and trend analysis
        - Runs Analysis: Visualizes upward/downward price streaks
        - Validation Tests: Demonstrates algorithm correctness with test cases
    
    **4. Adjust Moving Average:**
    - After analyzing, use the slider in the Price Chart tab
    - Choose moving average period (5-100 days, default: 20 days)
    - Chart updates in real-time as you slide
    
    **Understanding the Results:**
    - **Moving Average**: Smoothed price trend over time
    - **Daily Returns**: How much the price changed each day
    - **Volatility**: How much the price fluctuates (higher = more risky)
    - **Maximum Profit**: Best possible profit if you bought/sold optimally
    - **Runs**: Consecutive days of price increases or decreases
    - **Validation Tests**: Proves our algorithms work correctly with test cases
    
    **Validation Tests Tab:**
    - **Test 1**: SMA validation against pandas reference
    - **Test 2**: Daily returns validation against pandas pct_change()
    - **Test 3**: Runs analysis validation with real stock data
    - **Test 4**: Synthetic data validation with known expected results
    - **Test 5**: Max profit algorithm validation with simple test case
    - **Test 6**: Edge case validation (error handling)
    """)
    
    st.subheader("Common Stock Symbols:")
    st.write("""
    - AAPL: Apple Inc.
    - GOOGL: Google (Alphabet)
    - MSFT: Microsoft
    - TSLA: Tesla
    - AMZN: Amazon
    - META: Meta (Facebook)
    - NFLX: Netflix
    - NVDA: NVIDIA
    """)

# Footer
st.markdown("---")
