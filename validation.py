"""
Validation module for verifying calculations of FinancialTrendAnalyzer.

This module provides comprehensive validation testing to ensure all financial
analysis algorithms are working correctly. It compares our implementations
against trusted references like pandas and uses synthetic data with known
expected results to verify algorithm correctness.

Key Validation Features:
- SMA validation against pandas rolling mean
- Daily returns validation against pandas pct_change()
- Runs analysis validation with real and synthetic data
- Maximum profit algorithm validation with test cases
- Edge case testing for error handling
- Comprehensive test coverage with detailed output

The validation system ensures that all calculations produce accurate results
and handle edge cases gracefully, providing confidence in the analysis results.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import pandas as pd  # For data manipulation and reference calculations
import numpy as np  # For numerical operations and comparisons
from combined_analyzer import FinancialTrendAnalyzer  # Import the composite analyzer


def validate_all_calculations():  # VALIDATION FUNCTION
    """
    Comprehensive validation function that tests all calculation methods.
    
    This function performs extensive testing of all financial analysis algorithms
    to ensure they produce correct results. It includes multiple validation
    approaches:
    
    1. Reference Validation: Compare against pandas implementations
    2. Synthetic Data Testing: Use known data with expected results
    3. Edge Case Testing: Test error handling and boundary conditions
    4. Real Data Testing: Validate with actual stock market data
    
    Validation Tests:
        - Test 1: SMA validation against pandas rolling mean
        - Test 2: Daily returns validation against pandas pct_change()
        - Test 3: Runs analysis validation with real stock data
        - Test 3.5: Synthetic data validation for runs/streaks
        - Test 4: Max profit algorithm validation with simple test case
        - Test 5: Edge case validation (error handling)
    
    Output:
        - Detailed test results with pass/fail status
        - Side-by-side comparisons where applicable
        - Clear indication of any failures or discrepancies
    
    Example:
        # Run all validation tests
        validate_all_calculations()
        
        # This will output detailed test results for all algorithms
    
    Note:
        All tests use numpy.allclose() for floating-point comparisons
        with appropriate tolerance levels to account for numerical precision.
    """
    print("\n" + "="*60)
    print("VALIDATION TESTS")
    print("="*60)
    
    # Test with a well-known stock (Apple Inc.)
    try:
        analyzer = FinancialTrendAnalyzer("AAPL", "1y")
        
        # Test 1: SMA validation against pandas rolling mean
        print("\nTest 1: SMA Validation - Your Implementation vs Pandas Reference")
        print("-" * 60)
        sma_5 = analyzer.calculate_simple_moving_average(5)
        sma_5_pandas = analyzer.market_data['Close'].rolling(window=5).mean()
        sma_match = np.allclose(sma_5.dropna(), sma_5_pandas.dropna(), rtol=1e-10)
        
        # Show side-by-side comparison for transparency
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
        
        # Show side-by-side comparison for transparency
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
        
        # Expected results based on synthetic data analysis
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
        
        # Comprehensive validation of synthetic data
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


