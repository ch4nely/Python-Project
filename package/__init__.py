"""
Package initialization file for the dependency management system.

This file makes the 'package' directory a Python package, allowing us to import
functions from other files in this package. The package contains the dependency
management system that handles automatic installation of required Python packages.

The package provides:
- PackageDependencyManager: Main class for managing dependencies
- Convenience functions: ensure_dependencies(), install_missing_packages(), etc.
- Automatic setup functionality for the stock analysis tool

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

# This file makes the 'package' directory a Python package
# It allows us to import functions from other files in this package
# 
# Usage:
#   from package.dependency_manager import ensure_dependencies
#   ensure_dependencies()  # Automatically installs missing packages
