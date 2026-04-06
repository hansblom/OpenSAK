"""
src/opensak/utils/run_tests.py — CLI wrapper for the pytest test suite.

Collects and executes all tests located in the project's tests directory.
Passes additional command-line arguments directly to the pytest engine.
"""

import pytest
import sys

def run():
    """
    Entry point for 'opensak-test'.
    Runs all tests found in the /tests directory.
    """
    args = ["tests"] + sys.argv[1:]
    
    # Run pytest and exit with its return code
    print(f"OpenSAK Test Suite")
    sys.exit(pytest.main(args))