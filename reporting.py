"""
Stock Market Trend Analysis Reporting
Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import matplotlib.pyplot as plt
from combined_analyzer import FinancialTrendAnalyzer as CombinedAnalyzer
from validation import validate_all_calculations


class FinancialTrendAnalyzer(CombinedAnalyzer):
    def create_comprehensive_report(self, sma_window: int = 20):  # REPORT FUNCTION
        """
        Generate and print a comprehensive analysis report for the current ticker.

        Args:
            sma_window (int): Window size (in trading days) used for the Simple Moving Average.

        Returns:
            None
        """
        print(f"\n{'='*60}")
        print(f"STOCK ANALYSIS REPORT FOR {self.ticker_symbol}")
        print(f"{'='*60}")
        print(f"\nData Period: {self.market_data.index[0].strftime('%Y-%m-%d')} to {self.market_data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(self.market_data)}")
        print(f"Current Price: ${self.market_data['Close'].iloc[-1]:.2f}")
        print(f"Price Range: ${self.market_data['Close'].min():.2f} - ${self.market_data['Close'].max():.2f}")
        sma_values = self.calculate_simple_moving_average(sma_window)
        current_sma_value = sma_values.iloc[-1]
        print(f"\nSimple Moving Average ({sma_window} days): ${current_sma_value:.2f}")
        runs_data = self.analyze_price_runs()
        print(f"\nRUNS ANALYSIS:")
        print(f"Total Upward Days: {runs_data['total_upward_days']}")
        print(f"Total Downward Days: {runs_data['total_downward_days']}")
        print(f"Longest Upward Streak: {runs_data['longest_upward_streak']} days")
        print(f"Longest Downward Streak: {runs_data['longest_downward_streak']} days")
        print(f"Number of Upward Runs: {runs_data['upward_run_count']}")
        print(f"Number of Downward Runs: {runs_data['downward_run_count']}")
        daily_returns_data = self.compute_daily_returns()
        print(f"\nDAILY RETURNS ANALYSIS:")
        print(f"Average Daily Return: {daily_returns_data.mean():.4f}%")
        print(f"Standard Deviation: {daily_returns_data.std():.4f}%")
        print(f"Best Day: {daily_returns_data.max():.4f}%")
        print(f"Worst Day: {daily_returns_data.min():.4f}%")
        max_profit_value, transaction_pairs = self.calculate_maximum_profit()
        print(f"\nMAXIMUM PROFIT ANALYSIS:")
        print(f"Maximum Possible Profit: ${max_profit_value:.2f}")
        print(f"Number of Transactions: {len(transaction_pairs)}")
        if transaction_pairs:
            print("Buy/Sell Pairs (Index, Date):")
            for buy_idx, sell_idx in transaction_pairs[:5]:
                buy_date = self.market_data.index[buy_idx].strftime('%Y-%m-%d')
                sell_date = self.market_data.index[sell_idx].strftime('%Y-%m-%d')
                buy_price = self.market_data['Close'].iloc[buy_idx]
                sell_price = self.market_data['Close'].iloc[sell_idx]
                profit = sell_price - buy_price
                print(f"  Buy: {buy_date} (${buy_price:.2f}) -> Sell: {sell_date} (${sell_price:.2f}) | Profit: ${profit:.2f}")


if __name__ == "__main__":
    print("Stock Market Trend Analysis Tool")
    print("=" * 40)
    validate_all_calculations()
    try:
        analyzer = FinancialTrendAnalyzer("AAPL", "2y")
        analyzer.create_comprehensive_report(sma_window=20)
        print("\nGenerating visualizations...")
        analyzer.visualize_price_and_sma(sma_window=20)
        analyzer.visualize_price_runs()
        analyzer.visualize_daily_returns()
    except Exception as e:
        print(f"Error during analysis: {e}")


