#!/usr/bin/env python3
"""
SQLite Tutorial Runner

This script provides a command-line interface to run the SQLite tutorial scripts.
It allows users to run the tutorial scripts without using the Django web interface.
"""

import os
import sys
import subprocess
from pathlib import Path

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent

# Available tutorial scripts
TUTORIALS = {
    '1': {
        'name': 'SQLite Basics',
        'file': 'sqlite_basics.py',
        'description': 'Introduction to SQLite and basic CRUD operations'
    },
    '2': {
        'name': 'Parameterized Queries',
        'file': 'parameterized_queries.py',
        'description': 'Learn about secure query practices and resource management'
    },
    '3': {
        'name': 'Query Optimization',
        'file': 'query_optimization.py',
        'description': 'Understand how to optimize database queries'
    },
    '4': {
        'name': 'Student Database Project',
        'file': 'student_database_project.py',
        'description': 'Hands-on project to build a student database and generate reports'
    }
}

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the tutorial header"""
    print("=" * 80)
    print("SQLite Tutorial Runner".center(80))
    print("=" * 80)
    print()

def print_menu():
    """Print the tutorial menu"""
    print("Available Tutorials:")
    print()
    for key, tutorial in TUTORIALS.items():
        print(f"{key}. {tutorial['name']}")
        print(f"   {tutorial['description']}")
        print()
    print("q. Quit")
    print()

def run_tutorial(tutorial_key):
    """Run the selected tutorial"""
    if tutorial_key not in TUTORIALS:
        print("Invalid selection. Please try again.")
        return
    
    tutorial = TUTORIALS[tutorial_key]
    script_path = BASE_DIR / tutorial['file']
    
    clear_screen()
    print(f"Running: {tutorial['name']}")
    print(f"Description: {tutorial['description']}")
    print("=" * 80)
    print()
    
    try:
        # Run the script
        subprocess.run([sys.executable, str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError running tutorial: {e}")
    except KeyboardInterrupt:
        print("\nTutorial interrupted.")
    
    print("\n" + "=" * 80)
    input("\nPress Enter to return to the menu...")

def main():
    """Main function"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("Enter your choice (1-4, or q to quit): ").strip().lower()
        
        if choice == 'q':
            print("\nThank you for using the SQLite Tutorial Runner!")
            break
        elif choice in TUTORIALS:
            run_tutorial(choice)
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()