# Copy Strategies

A little Windows app to help coping files between three folders:
- Real-Tick
- SPP
- Final

You pick the folders, see which files match, and copy them to the Final folder with one click. Super simple.

## Features
- GUI (Tkinter)
- Preview pane showing which files will be copied
- Remembers your last-used folder paths
- One-click copy operation
- No external dependencies beyond Python and Tkinter

## How to Build/Run
1. Make sure you have Python 3.11+ (Windows).
2. Open a terminal here.
3. (Optional) Run this to make a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
4. Build it:
   ```cmd/powershell
   build.bat
   ```
   (This grabs PyInstaller and builds the .exe for you.)
5. Find your app in `dist/copy-strategies.exe` and double-click it!

That's it. Main code is in `copy-strategies.py` if you want to poke around.

## Development
- The main application code is in `copy-strategies.py`.
- The build configuration is in `copy-strategies.spec` and `build.bat`.
