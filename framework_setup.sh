#!/bin/bash

# Define the root directory name
ROOT_DIR="framework"

# Create root directory
mkdir -p $ROOT_DIR

# Create subdirectories
mkdir -p $ROOT_DIR/{data,analytics,utils,cli,tests}

# Create __init__.py files for Python modules
touch $ROOT_DIR/data/__init__.py
touch $ROOT_DIR/analytics/__init__.py
touch $ROOT_DIR/utils/__init__.py
touch $ROOT_DIR/cli/__init__.py
touch $ROOT_DIR/tests/__init__.py

# Create other necessary files
touch $ROOT_DIR/data/fetcher.py
touch $ROOT_DIR/analytics/indicators.py
touch $ROOT_DIR/utils/config.py
touch $ROOT_DIR/cli/main.py
touch $ROOT_DIR/tests/test_data.py
touch $ROOT_DIR/tests/test_analytics.py

# Create additional root files
touch $ROOT_DIR/README.md
touch $ROOT_DIR/.gitignore
touch $ROOT_DIR/requirements.txt
touch $ROOT_DIR/setup.py

echo "Project structure for MarketVisor has been set up in $ROOT_DIR."

