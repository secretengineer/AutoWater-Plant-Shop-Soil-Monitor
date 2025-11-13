#!/usr/bin/env python3
"""
Entry point for the AutoWater Plant Shop Soil Monitor application.

This script initializes and starts the complete monitoring system including:
- Sensor data collection
- Data processing and analysis  
- Web dashboard interface
- System health monitoring

Usage:
    python run.py
    
Environment Variables:
    AUTOWATER_CONFIG_DIR: Directory containing configuration files (default: config/)
    AUTOWATER_LOG_LEVEL: Logging level (default: INFO)
"""

import sys
import os

# Ensure the src directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from src.main import main
except ImportError as e:
    print(f"Error importing main module: {e}")
    print("Please ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
