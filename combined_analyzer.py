"""
Composite FinancialTrendAnalyzer that combines data fetching, computing, and visualization
into a single, importable class via multiple inheritance.

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

from data_fetching import FinancialTrendAnalyzer as DataFetchingMixin
from computing import FinancialTrendAnalyzer as ComputingMixin
from visualizations import FinancialTrendAnalyzer as VisualizationMixin


class FinancialTrendAnalyzer(DataFetchingMixin, ComputingMixin, VisualizationMixin):
    pass


