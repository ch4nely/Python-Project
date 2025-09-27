@echo off
title Stock Analysis Project
color 0A

echo ================================================================
echo                    STOCK ANALYSIS PROJECT
echo ================================================================
echo.
echo Checking dependencies...

REM Check if dependencies are installed
python -c "from package.dependency_manager import check_setup; exit(0 if check_setup()['all_dependencies_installed'] else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Dependencies not found. Installing automatically...
    echo This may take a few minutes...
    echo.
    python package/dependency_manager.py
    if %errorlevel% neq 0 (
        echo.
        echo Installation failed. Please check your internet connection.
        echo You can manually install dependencies using option 5 in the menu.
        echo.
        pause
    ) else (
        echo.
        echo ✅ Dependencies installed successfully!
        echo.
        pause
    )
) else (
    echo ✅ All dependencies are ready!
    echo.
)

:MAIN_MENU
cls
echo ================================================================
echo                    STOCK ANALYSIS PROJECT
echo ================================================================
echo.
echo Choose an option:
echo.
echo 1. Web Application Interface (Recommended)
echo 2. Demo and Validation Tool
echo 3. Exit
echo.
echo ================================================================
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto WEB_APP
if "%choice%"=="2" goto DEMO
if "%choice%"=="3" goto EXIT
goto INVALID


:WEB_APP
cls
echo ================================================================
echo                    WEB APPLICATION
echo ================================================================
echo.
echo Starting web application...
echo This will automatically install missing packages if needed
echo This will open your web browser automatically
echo The app will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the web app and return to main menu
echo.
streamlit run webapp.py
echo.
echo Web app stopped. Press any key to return to main menu...
pause >nul
goto MAIN_MENU

:DEMO
cls
echo ================================================================
echo            DEMO AND VALIDATION TOOL (INTERACTIVE)
echo ================================================================
echo.
echo Starting demo and validation tool...
echo This provides educational features including:
echo - Interactive demo with plots
echo - Validation tests (your calculations vs reference)
echo - Comprehensive automated demo
echo.
python demo_validation.py
echo.
echo Demo tool completed. Press any key to return to main menu...
pause >nul
goto MAIN_MENU



:INVALID
cls
echo ================================================================
echo                        INVALID CHOICE
echo ================================================================
echo.
echo Please enter a number between 1 and 3
echo.
echo Press any key to try again...
pause >nul
goto MAIN_MENU

:EXIT
cls
echo ================================================================
echo                    THANK YOU!
echo ================================================================
echo.
echo Thanks for using the Stock Analysis Project!
echo.
echo Press any key to exit...
pause >nul
exit

