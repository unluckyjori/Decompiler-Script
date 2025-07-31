# Decompiler Script

This Python script automates the process of decompiling .NET game assemblies using the dotnet CLI and ilspycmd. It checks for necessary tools, handles user input, and decompiles specified DLL files.

## Prerequisites

- **.NET SDK**: Ensure that the .NET SDK is installed on your system. You can verify this by running `dotnet --version`.
- **ilspycmd**: The script will check for ilspycmd and install it if not found.
- **Python 3**: Make sure Python 3 is installed on your system.

## Installation

1. Clone this repository to your local machine.
2. Navigate to the directory containing the script.
3. Make the script executable (if not already):
   ```bash
   chmod +x decompile.py
   ```

## Usage

1. Run the script:
   ```bash
   ./decompile.py
   ```
2. Follow the prompts to enter the path to the `.dll` file or a directory containing `.dll` files.
3. Enter the output folder path where the decompiled files should be saved.
4. If a directory is selected, confirm whether to decompile all `.dll` files within it.

## Features

- **Automatic Tool Checks**: The script checks for the .NET SDK and ilspycmd, installing ilspycmd if necessary.
- **Flexible Input**: Accepts both individual `.dll` files and directories containing multiple `.dll` files.
- **User-Friendly**: Provides clear prompts and error messages to guide the user through the process.

## License

This project is licensed under the MIT License.