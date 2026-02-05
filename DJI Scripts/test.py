#!/usr/bin/env python3
"""
A standard Hello World script.
"""

def main():
    """Main entry point for the script."""
    print("Hello, World!")
    try:
        raise ValueError("Invalid input provided")
    except ValueError:
        print("exception handled! Raising anyway...")
        raise

if __name__ == "__main__":
    main()
