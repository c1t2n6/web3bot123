#!/bin/bash

# Interactive script to set up .env file for the trading bot

# Define the .env file path
ENV_FILE=".env"

# Prompt for API keys and trading parameters
read -p "Enter your HORUS_API_KEY: " HORUS_API_KEY
read -p "Enter your Roostoo API_KEY: " API_KEY
read -p "Enter your Roostoo SECRET_KEY: " SECRET_KEY
read -p "Enter your initial capital (e.g., 50000.0): " INITIAL_CAPITAL

# Optional parameters with defaults
read -p "Enter scan interval in seconds (default: 300): " SCAN_INTERVAL
SCAN_INTERVAL=${SCAN_INTERVAL:-300}

read -p "Enter position check interval in seconds (default: 60): " POSITION_CHECK_INTERVAL
POSITION_CHECK_INTERVAL=${POSITION_CHECK_INTERVAL:-60}

read -p "Enter max open positions (default: 1): " MAX_OPEN_POSITIONS
MAX_OPEN_POSITIONS=${MAX_OPEN_POSITIONS:-1}

read -p "Enter max portfolio drawdown (default: 0.15): " MAX_PORTFOLIO_DRAWDOWN
MAX_PORTFOLIO_DRAWDOWN=${MAX_PORTFOLIO_DRAWDOWN:-0.15}

read -p "Enter minimum risk-reward ratio (default: 2.0): " MIN_RR_RATIO
MIN_RR_RATIO=${MIN_RR_RATIO:-2.0}

read -p "Enter minimum setup confidence (default: 80): " MIN_SETUP_CONFIDENCE
MIN_SETUP_CONFIDENCE=${MIN_SETUP_CONFIDENCE:-80}

# Write to .env file
cat > $ENV_FILE <<EOL
HORUS_API_KEY=$HORUS_API_KEY
API_KEY=$API_KEY
SECRET_KEY=$SECRET_KEY
INITIAL_CAPITAL=$INITIAL_CAPITAL
SCAN_INTERVAL=$SCAN_INTERVAL
POSITION_CHECK_INTERVAL=$POSITION_CHECK_INTERVAL
MAX_OPEN_POSITIONS=$MAX_OPEN_POSITIONS
MAX_PORTFOLIO_DRAWDOWN=$MAX_PORTFOLIO_DRAWDOWN
MIN_RR_RATIO=$MIN_RR_RATIO
MIN_SETUP_CONFIDENCE=$MIN_SETUP_CONFIDENCE
TRADE_LOG_FILE=trades.json
PORTFOLIO_LOG_FILE=portfolio_metrics.json
EOL

# Confirm completion
echo ".env file created successfully!"
echo "You can review it by running: cat $ENV_FILE"
