"""
Dependency Manager - Centralized dependency installation
This module handles automatic installation of required packages

Group Members: Chanel, Do Tien Son, Marcus, Afiq, Hannah
INF1002 - PROGRAMMING FUNDAMENTALS, LAB-P13-3
"""

import subprocess
import sys
import importlib
import os
from typing import List, Dict, Optional

class PackageDependencyManager:
    """Centralized dependency management for the financial trend analysis tool"""
    
    # Define all required packages with their versions
    REQUIRED_PACKAGES = {
        "streamlit": ">=1.28.0",
        "yfinance": ">=0.2.18", 
        "pandas": ">=1.5.0",
        "numpy": ">=1.21.0",
        "matplotlib": ">=3.5.0",
        "plotly": ">=5.0.0",
        "seaborn": ">=0.11.0"
    }
    
    @classmethod
    def install_if_missing(cls, package: str, version: Optional[str] = None) -> bool:
        """
        Install package if it's not already installed
        
        Args:
            package: Package name to check/install
            version: Optional version requirement
            
        Returns:
            bool: True if package is available, False if installation failed
        """
        try:
            # Try to import the package
            importlib.import_module(package)
            return True
        except ImportError:
            # Package not found, try to install it
            try:
                install_cmd = [sys.executable, "-m", "pip", "install"]
                
                if version:
                    install_cmd.append(f"{package}{version}")
                else:
                    install_cmd.append(package)
                
                print(f"📦 Installing missing package: {package}...")
                result = subprocess.run(install_cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Successfully installed {package}")
                    return True
                else:
                    print(f"❌ Failed to install {package}: {result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error installing {package}: {str(e)}")
                return False
    
    @classmethod
    def ensure_all_dependencies(cls, verbose: bool = True) -> Dict[str, bool]:
        """
        Ensure all required dependencies are installed
        
        Args:
            verbose: Whether to print installation messages
            
        Returns:
            Dict mapping package names to installation success status
        """
        if verbose:
            print("🔧 Checking and installing dependencies...")
        
        results = {}
        
        for package, version in cls.REQUIRED_PACKAGES.items():
            results[package] = cls.install_if_missing(package, version)
        
        if verbose:
            failed_packages = [pkg for pkg, success in results.items() if not success]
            if failed_packages:
                print(f"⚠️  Warning: Failed to install: {', '.join(failed_packages)}")
            else:
                print("✅ All dependencies are ready!")
        
        return results
    
    @classmethod
    def install_from_requirements(cls, requirements_file: str = "requirements.txt") -> bool:
        """
        Install dependencies from requirements.txt file
        
        Args:
            requirements_file: Path to requirements file
            
        Returns:
            bool: True if installation successful, False otherwise
        """
        if not os.path.exists(requirements_file):
            print(f"❌ Requirements file not found: {requirements_file}")
            return False
        
        try:
            print(f"📦 Installing from {requirements_file}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", requirements_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All packages installed successfully!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error during installation: {str(e)}")
            return False
    
    @classmethod
    def check_python_version(cls, min_version: tuple = (3, 7)) -> bool:
        """
        Check if Python version meets minimum requirements
        
        Args:
            min_version: Minimum required Python version (major, minor)
            
        Returns:
            bool: True if version is sufficient
        """
        current_version = sys.version_info[:2]
        if current_version >= min_version:
            return True
        else:
            print(f"❌ Python {min_version[0]}.{min_version[1]}+ required, found {current_version[0]}.{current_version[1]}")
            return False
    
    @classmethod
    def get_missing_packages(cls) -> List[str]:
        """
        Get list of packages that are not installed
        
        Returns:
            List of missing package names
        """
        missing = []
        for package in cls.REQUIRED_PACKAGES.keys():
            try:
                importlib.import_module(package)
            except ImportError:
                missing.append(package)
        return missing
    
    @classmethod
    def is_fully_configured(cls) -> bool:
        """
        Check if all dependencies are properly installed
        
        Returns:
            bool: True if all dependencies are available
        """
        return len(cls.get_missing_packages()) == 0


# Convenience functions for easy import
def ensure_dependencies(verbose: bool = True) -> bool:
    """Quick function to ensure all dependencies are installed"""
    results = PackageDependencyManager.ensure_all_dependencies(verbose)
    return all(results.values())

def install_missing_packages() -> bool:
    """Install only the packages that are missing"""
    missing = PackageDependencyManager.get_missing_packages()
    if not missing:
        return True
    
    success_count = 0
    for package in missing:
        version = PackageDependencyManager.REQUIRED_PACKAGES.get(package)
        if PackageDependencyManager.install_if_missing(package, version):
            success_count += 1
    
    return success_count == len(missing)

def check_setup() -> Dict[str, bool]:
    """Check the setup status of all components"""
    return {
        "python_version_ok": PackageDependencyManager.check_python_version(),
        "all_dependencies_installed": PackageDependencyManager.is_fully_configured(),
        "missing_packages": PackageDependencyManager.get_missing_packages()
    }

def setup_main():
    """Main dependency setup function - can be called directly"""
    print("🔧 Stock Analysis Tool - Dependency Setup")
    print("=" * 50)
    
    # Check Python version
    if not PackageDependencyManager.check_python_version():
        input("\nPress Enter to exit...")
        return False
    
    # Check current setup status
    setup_status = check_setup()
    
    if setup_status["all_dependencies_installed"]:
        print("✅ All dependencies are already installed!")
        print("\n🎉 You're ready to go!")
        print("\nYou can now use any of the options in the menu above!")
        return True
    
    # Show missing packages
    missing = setup_status["missing_packages"]
    if missing:
        print(f"📦 Missing packages: {', '.join(missing)}")
    
    # Try installing from requirements.txt first (faster)
    print("\n📦 Installing from requirements.txt...")
    if PackageDependencyManager.install_from_requirements():
        print("\n🎉 Setup complete!")
        print("\nYou can now use any of the options in the menu above!")
        return True
    
    # Fallback to individual package installation
    print("\n📦 Installing packages individually...")
    results = PackageDependencyManager.ensure_all_dependencies()
    
    if all(results.values()):
        print("\n🎉 Setup complete!")
        print("\nYou can now use any of the options in the menu above!")
        return True
    else:
        failed_packages = [pkg for pkg, success in results.items() if not success]
        print(f"\n❌ Setup incomplete. Failed packages: {', '.join(failed_packages)}")
        print("Please check your internet connection and try again.")
        return False

if __name__ == "__main__":
    """Allow direct execution of dependency setup"""
    success = setup_main()
    if not success:
        input("\nPress Enter to exit...")
