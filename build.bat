@echo off
REM Build script for Copy Strategies (copy-strategies.py)

REM Check for PyInstaller, install if missing
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous build artifacts
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist copy-strategies.spec del copy-strategies.spec

REM Build the executable
pyinstaller --noconfirm --onefile --windowed --name copy-strategies copy-strategies.py

REM Show result
if exist dist\copy-strategies.exe (
    echo Build successful! Executable is in the dist folder.
) else (
    echo Build failed. Check the output above for errors.
) 