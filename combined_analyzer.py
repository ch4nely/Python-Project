"""
Composite FinancialTrendAnalyzer that combines data fetching, computing, and visualization
into a single, importable class via multiple inheritance.
"""

from data_fetching import FinancialTrendAnalyzer as DataFetchingMixin
from computing import FinancialTrendAnalyzer as ComputingMixin
from visualizations import FinancialTrendAnalyzer as VisualizationMixin


class FinancialTrendAnalyzer(DataFetchingMixin, ComputingMixin, VisualizationMixin):
    pass


