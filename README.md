# Copy Strategies

Copy Strategies is a simple desktop application for Windows that helps you manage and copy files between three folders:
- **Real-Tick Folder**
- **SPP Folder**
- **Final Folder**

The app shows a preview of files that exist in both the Real-Tick and SPP folders, and allows you to copy them to the Final folder with a single click. It is designed for workflows where you need to synchronize or consolidate files from two sources into a final destination.

## Features
- Modern, user-friendly GUI (Tkinter)
- Preview pane showing which files will be copied
- Remembers your last-used folder paths
- One-click copy operation
- No external dependencies beyond Python and Tkinter

## How to Build the Executable

### Prerequisites
- Python 3.11 or later (Windows)
- [PyInstaller](https://pyinstaller.org/) (will be installed automatically by the build script)

### Steps
1. **Clone the repository and open a terminal in the project root.**
2. **(Optional) Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Build the executable:**
   ```sh
   build.bat
   ```
   This will:
   - Install PyInstaller if needed
   - Clean previous builds
   - Build the app using the provided spec file

4. **Find your executable:**
   - After building, the executable will be in `dist\copy-strategies\copy-strategies.exe`

## Running the App
- Double-click the `.exe` file, or run it from the command line.
- Select your folders, preview the files, and click Start to copy.

## Development
- The main application code is in `copy-strategies.py`.
- The build configuration is in `copy-strategies.spec` and `build.bat`.

## License
This project is provided as-is for personal or internal use. 