#!/usr/bin/env python3
"""
Test runner for AutoWater Plant Shop Soil Monitor.

This script runs all tests and provides coverage reporting.
"""

import sys
import os
import subprocess
import argparse

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)


def run_tests(coverage=False, verbose=False, specific_test=None):
    """Run the test suite."""
    cmd = ['python', '-m', 'pytest']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    if specific_test:
        cmd.append(specific_test)
    else:
        cmd.append('tests/')
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=current_dir)
    return result.returncode


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run AutoWater tests')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--test', help='Run specific test file')
    
    args = parser.parse_args()
    
    return_code = run_tests(
        coverage=args.coverage,
        verbose=args.verbose,
        specific_test=args.test
    )
    
    if args.coverage and return_code == 0:
        print("\nCoverage report generated in htmlcov/index.html")
    
    sys.exit(return_code)


if __name__ == '__main__':
    main()