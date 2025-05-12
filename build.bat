@echo off
REM Build script for Copy Strategies (using copy-strategies.spec)

REM Check for PyInstaller, install if missing
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous build artifacts
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Build the executable using the .spec file
pyinstaller copy-strategies.spec

REM Show result
if exist dist\copy-strategies\copy-strategies.exe (
    echo Build successful! Executable is in the dist\copy-strategies folder.
) else (
    echo Build failed. Check the output above for errors.
) 