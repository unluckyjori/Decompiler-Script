#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil

# --- Configuration ---
# The username is dynamically fetched and used in the PATH export command.
USER = os.environ.get("USER")

# --- Helper Functions ---
def print_error(message):
    """Prints an error message to stderr."""
    print(f"❌ Error: {message}", file=sys.stderr)

def print_info(message):
    """Prints an informational message to stdout."""
    print(f"✅ Info: {message}")

def run_command(command, check=True):
    """
    Runs a command and captures its output.
    
    Args:
        command (list): The command to execute as a list of strings.
        check (bool): If True, raises an exception on non-zero exit codes.

    Returns:
        subprocess.CompletedProcess: The result of the command execution.
    """
    try:
        return subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
    except FileNotFoundError:
        print_error(f"Command not found: '{command[0]}'. Please ensure it's in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}: '{' '.join(command)}'")
        print_error(f"Stderr: {e.stderr.strip()}")
        sys.exit(e.returncode)

# --- Main Script ---
def decompile_dll(dll_path, output_folder):
    """Decompiles a single DLL file."""
    print_info(f"Decompiling '{dll_path}' to '{output_folder}'...")
    run_command(["ilspycmd", "-p", dll_path, "-o", output_folder])
    print_info("Decompilation complete!")
    print_info(f"Output saved to: {os.path.abspath(output_folder)}")

def handle_directory_input(dir_path, output_folder):
    """Handles user input when a directory is provided."""
    print_info(f"The path '{dir_path}' is a directory.")
    try:
        choice = input("Did you mean to select a folder to decompile all .dll files within it? (y/n): ").lower().strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

    if choice != 'y':
        print_info("Operation cancelled. Please re-run the script with a valid file path.")
        sys.exit(0)

    dll_files = [f for f in os.listdir(dir_path) if f.endswith(".dll")]
    
    if not dll_files:
        print_error(f"No .dll files found in '{dir_path}'.")
        sys.exit(1)

    print_info("Found the following .dll files:")
    for dll_file in dll_files:
        print(f"  - {dll_file}")
        
    try:
        confirm_choice = input("Do you want to decompile all of them? (y/n): ").lower().strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

    if confirm_choice == 'y':
        for dll_file in dll_files:
            full_dll_path = os.path.join(dir_path, dll_file)
            # Create a sub-folder for each DLL's output to avoid overwriting
            file_output_folder = os.path.join(output_folder, os.path.splitext(dll_file)[0])
            decompile_dll(full_dll_path, file_output_folder)
        
        print_info("All selected .dll files have been decompiled successfully.")
    else:
        print_info("Operation cancelled. You can re-run the script to select a different path.")

# --- Main Script ---
def main():
    """Main function to orchestrate the decompilation process."""
    # 1. Check for .NET SDK
    print_info("Checking for .NET SDK...")
    try:
        dotnet_version_result = run_command(["dotnet", "--version"])
        print_info(f".NET SDK found: Version {dotnet_version_result.stdout.strip()}")
    except Exception:
        print_error(".NET SDK not found. Please install it to continue.")
        sys.exit(1)

    # 2. Ensure .dotnet/tools is in PATH
    print_info("Ensuring .dotnet/tools is in PATH...")
    dotnet_tools_path = os.path.expanduser("~/.dotnet/tools")
    if dotnet_tools_path not in os.environ["PATH"]:
        print_info(f"Temporarily adding {dotnet_tools_path} to PATH.")
        os.environ["PATH"] = f"{os.environ['PATH']}:{dotnet_tools_path}"

    # 3. Check for ilspycmd
    print_info("Checking for ilspycmd...")
    try:
        run_command(["ilspycmd", "--version"])
        print_info("ilspycmd is already installed.")
    except Exception:
        print_info("ilspycmd not found. Attempting to install it globally...")
        run_command(["dotnet", "tool", "install", "--global", "ilspycmd"])
        print_info("ilspycmd installed successfully.")

    # 4. Get and process user input
    while True:
        try:
            path_input = input("Enter the path to the .dll file or a folder: ").strip()
            output_folder_input = input("Enter the output folder path: ").strip()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)

        # Clean and expand paths
        path = os.path.expanduser(path_input.strip("'\""))
        output_folder = os.path.expanduser(output_folder_input.strip("'\""))

        if os.path.isdir(path):
            handle_directory_input(path, output_folder)
            break
        elif os.path.isfile(path):
            if not path.endswith(".dll"):
                print_error("The selected file is not a .dll file. Please try again.")
                continue 
            decompile_dll(path, output_folder)
            break
        else:
            print_error(f"The path '{path}' is not a valid file or directory. Please try again.")

if __name__ == "__main__":
    main()
