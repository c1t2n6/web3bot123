"""
HK Quant Trading Hackathon - Bot Template
==========================================

This is a basic template for a trading bot that interfaces with Roostoo API.
Customize this template with your trading strategy.

Requirements:
- Python 3.7+
- requests library: pip install requests
"""

import requests
import hmac
import hashlib
import time
import logging
from typing import Optional, Dict, Any

# New imports for multi-asset support, utilities and environment loading
import numpy as np
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ============================================================================
# Configuration
# ============================================================================

BASE_URL = "https://mock-api.roostoo.com"

# TODO: Replace with your API credentials
API_KEY = "your-api-key-here"
SECRET_KEY = "your-secret-key-here"

# Trading configuration
TRADING_PAIR = "BTC/USD"  # Change to your preferred pair
CHECK_INTERVAL = 60  # seconds between strategy checks

# ============================================================================
# MULTI-ASSET PORTFOLIO CONFIGURATION
# ============================================================================
AVAILABLE_PAIRS = []
PORTFOLIO_COINS = {}

CANDLE_HISTORY_SIZE = 100
OHLC_HISTORY = {}

PRIMARY_TIMEFRAME = '15m'
CONFIRMATION_TIMEFRAME = '1h'
ALTERNATIVE_TIMEFRAMES = ['5m', '4h', '1d']

SCAN_INTERVAL = 300
POSITION_CHECK_INTERVAL = 60

GLOBAL_PORTFOLIO_RISK = 0.02
MAX_OPEN_POSITIONS = 1
MAX_PORTFOLIO_DRAWDOWN = 0.15
MIN_RR_RATIO = 2.0
MIN_SETUP_CONFIDENCE = 80

TRADE_LOG_FILE = 'trades.json'
PORTFOLIO_LOG_FILE = 'portfolio_metrics.json'

HORUS_API_KEY = os.getenv('HORUS_API_KEY')
HORUS_BASE_URL = "https://api.horusdata.xyz/v1"
DATA_SOURCE_PRIMARY = 'HORUS'
DATA_SOURCE_FALLBACK = 'COINGECKO'

HORUS_REQUEST_TIMEOUT = 15
HORUS_RETRY_LIMIT = 3
HORUS_CACHE_DURATION = 60

MIN_VOLUME_FILTER = 100000
MIN_PRICE = 0.0001

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# API Helper Functions
# ============================================================================

def _get_timestamp() -> int:
    """Get current timestamp in milliseconds (13 digits)"""
    return int(time.time() * 1000)


def _get_signed_headers(payload: Dict[str, Any]) -> tuple:
    """
    Generate signed headers for RCL_TopLevelCheck endpoints
    
    Args:
        payload: dict of parameters
        
    Returns:
        tuple: (headers dict, final_payload dict, total_params_string)
    """
    # Add timestamp
    payload['timestamp'] = _get_timestamp()
    
    # Sort parameters and create query string
    sorted_params = sorted(payload.items())
    total_params_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    # Generate HMAC SHA256 signature
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        total_params_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Create headers
    headers = {
        'RST-API-KEY': API_KEY,
        'MSG-SIGNATURE': signature
    }
    
    return headers, payload, total_params_string


def get_server_time() -> Optional[Dict]:
    """Get server time (Auth: RCL_TSCheck)"""
    url = f"{BASE_URL}/v3/server_time"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting server time: {e}")
        return None


def get_ticker(pair: str) -> Optional[Dict]:
    """Get market ticker (Auth: RCL_TSCheck)"""
    url = f"{BASE_URL}/v3/ticker"
    params = {
        'pair': pair,
        'timestamp': _get_timestamp()
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting ticker: {e}")
        return None


def get_balance() -> Optional[Dict]:
    """Get account balance (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/balance"
    
    payload = {}
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting balance: {e}")
        return None


def place_order(
    pair: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None
) -> Optional[Dict]:
    """
    Place a new order (Auth: RCL_TopLevelCheck)
    
    Args:
        pair: Trading pair (e.g., "BTC/USD")
        side: "BUY" or "SELL"
        order_type: "MARKET" or "LIMIT"
        quantity: Amount to trade (string)
        price: Required if order_type="LIMIT"
    """
    url = f"{BASE_URL}/v3/place_order"
    
    payload = {
        'pair': pair,
        'side': side.upper(),
        'type': order_type.upper(),
        'quantity': str(quantity)
    }
    
    # Validate LIMIT order has price
    if order_type.upper() == "LIMIT":
        if price is None:
            logger.error("LIMIT order requires price parameter")
            return None
        payload['price'] = str(price)
    elif price is not None:
        logger.warning("price parameter ignored for MARKET order")
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response: {e.response.text}")
        return None


def query_order(
    order_id: Optional[str] = None,
    pair: Optional[str] = None,
    pending_only: Optional[bool] = None
) -> Optional[Dict]:
    """Query orders (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/query_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair
        if pending_only is not None:
            payload['pending_only'] = 'TRUE' if pending_only else 'FALSE'
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error querying order: {e}")
        return None


def cancel_order(order_id: Optional[str] = None, pair: Optional[str] = None) -> Optional[Dict]:
    """Cancel orders (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/cancel_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error canceling order: {e}")
        return None


# ============================================================================
# Trading Strategy (CUSTOMIZE THIS SECTION)
# ============================================================================

class TradingStrategy:
    """Base trading strategy class - customize with your logic"""
    
    def __init__(self):
        self.name = "Template Strategy"
        # Add your strategy parameters here
        self.min_balance_ratio = 0.1  # Keep 10% cash reserve
        
    def should_buy(self, ticker: Dict, balance: Dict) -> bool:
        """
        Determine if bot should buy
        
        Args:
            ticker: Market ticker data
            balance: Account balance
            
        Returns:
            bool: True if should buy
        """
        # TODO: Implement your buy logic here
        # Example: Buy if price is below some threshold
        current_price = ticker.get('Ticker', {}).get('LastPrice', 0)
        
        # Placeholder logic - replace with your strategy
        return False
    
    def should_sell(self, ticker: Dict, balance: Dict) -> bool:
        """
        Determine if bot should sell
        
        Args:
            ticker: Market ticker data
            balance: Account balance
            
        Returns:
            bool: True if should sell
        """
        # TODO: Implement your sell logic here
        # Example: Sell if price is above some threshold or take profit
        
        # Placeholder logic - replace with your strategy
        return False
    
    def calculate_buy_quantity(self, ticker: Dict, balance: Dict) -> Optional[str]:
        """
        Calculate how much to buy
        
        Args:
            ticker: Market ticker data
            balance: Account balance
            
        Returns:
            str: Quantity to buy, or None if shouldn't buy
        """
        # TODO: Implement position sizing logic
        # Consider:
        # - Available balance
        # - Commission (0.1%)
        # - Risk management
        # - Portfolio allocation
        
        current_price = ticker.get('Ticker', {}).get('LastPrice', 0)
        if current_price == 0:
            return None
        
        # Get quote currency (e.g., USD in BTC/USD)
        quote_currency = TRADING_PAIR.split('/')[1]
        available = balance.get('Balance', {}).get(quote_currency, {}).get('Available', 0)
        
        if available < 100:  # Minimum order size
            return None
        
        # Use 90% of available balance to account for commission
        max_spend = available * 0.9
        quantity = max_spend / current_price * 0.999  # Account for 0.1% commission
        
        return str(quantity)
    
    def calculate_sell_quantity(self, ticker: Dict, balance: Dict) -> Optional[str]:
        """
        Calculate how much to sell
        
        Args:
            ticker: Market ticker data
            balance: Account balance
            
        Returns:
            str: Quantity to sell, or None if shouldn't sell
        """
        # TODO: Implement position sizing logic
        
        # Get base currency (e.g., BTC in BTC/USD)
        base_currency = TRADING_PAIR.split('/')[0]
        available = balance.get('Balance', {}).get(base_currency, {}).get('Available', 0)
        
        if available < 0.001:  # Minimum order size
            return None
        
        # Sell 90% of available to keep some reserve
        quantity = available * 0.9
        
        return str(quantity)
    
    def get_order_type(self) -> str:
        """Get preferred order type (MARKET or LIMIT)"""
        # TODO: Implement logic to choose between MARKET and LIMIT
        return "MARKET"
    
    def get_limit_price(self, ticker: Dict, side: str) -> Optional[str]:
        """
        Get limit price if using LIMIT orders
        
        Args:
            ticker: Market ticker data
            side: "BUY" or "SELL"
            
        Returns:
            str: Limit price, or None for MARKET orders
        """
        # TODO: Implement limit price calculation
        # Example: Buy slightly below market, sell slightly above
        current_price = ticker.get('Ticker', {}).get('LastPrice', 0)
        
        if side == "BUY":
            # Buy 0.5% below market
            return str(current_price * 0.995)
        else:
            # Sell 0.5% above market
            return str(current_price * 1.005)


# ============================================================================
# Trading Bot Main Loop
# ============================================================================

class TradingBot:
    """Main trading bot class"""
    
    def __init__(self, strategy: TradingStrategy):
        self.strategy = strategy
        self.running = False
        self.stats = {
            'total_orders': 0,
            'successful_orders': 0,
            'failed_orders': 0,
            'last_check': 0.0
        }
    
    def initialize(self) -> bool:
        """Initialize bot - test API connection"""
        logger.info("Initializing bot...")
        
        # Test server time
        server_time = get_server_time()
        if not server_time:
            logger.error("Failed to connect to Roostoo API")
            return False
        
        logger.info(f"Connected to Roostoo API. Server time: {server_time.get('ServerTime')}")
        
        # Test balance
        balance = get_balance()
        if not balance or not balance.get('Success'):
            logger.error("Failed to get account balance")
            return False
        
        logger.info("Bot initialized successfully")
        return True
    
    def run_iteration(self):
        """Run one iteration of the trading strategy"""
        try:
            # 1. Get market data
            ticker = get_ticker(TRADING_PAIR)
            if not ticker or not ticker.get('Success'):
                logger.error("Failed to get ticker data")
                return
            
            # 2. Get balance
            balance = get_balance()
            if not balance or not balance.get('Success'):
                logger.error("Failed to get balance")
                return
            
            current_price = ticker.get('Ticker', {}).get('LastPrice', 0)
            logger.info(f"Current {TRADING_PAIR} price: {current_price}")
            
            # 3. Check for buy signal
            if self.strategy.should_buy(ticker, balance):
                quantity = self.strategy.calculate_buy_quantity(ticker, balance)
                if quantity:
                    order_type = self.strategy.get_order_type()
                    price = None
                    if order_type == "LIMIT":
                        price = self.strategy.get_limit_price(ticker, "BUY")
                    
                    logger.info(f"Buy signal: {quantity} {TRADING_PAIR} @ {order_type}")
                    order = place_order(TRADING_PAIR, "BUY", order_type, quantity, price)
                    
                    self.stats['total_orders'] += 1
                    if order and order.get('Success'):
                        self.stats['successful_orders'] += 1
                        order_id = order.get('OrderDetail', {}).get('OrderID')
                        logger.info(f"Buy order placed successfully: {order_id}")
                    else:
                        self.stats['failed_orders'] += 1
                        error_msg = order.get('ErrMsg', 'Unknown error') if order else 'No response'
                        logger.error(f"Buy order failed: {error_msg}")
            
            # 4. Check for sell signal
            elif self.strategy.should_sell(ticker, balance):
                quantity = self.strategy.calculate_sell_quantity(ticker, balance)
                if quantity:
                    order_type = self.strategy.get_order_type()
                    price = None
                    if order_type == "LIMIT":
                        price = self.strategy.get_limit_price(ticker, "SELL")
                    
                    logger.info(f"Sell signal: {quantity} {TRADING_PAIR} @ {order_type}")
                    order = place_order(TRADING_PAIR, "SELL", order_type, quantity, price)
                    
                    self.stats['total_orders'] += 1
                    if order and order.get('Success'):
                        self.stats['successful_orders'] += 1
                        order_id = order.get('OrderDetail', {}).get('OrderID')
                        logger.info(f"Sell order placed successfully: {order_id}")
                    else:
                        self.stats['failed_orders'] += 1
                        error_msg = order.get('ErrMsg', 'Unknown error') if order else 'No response'
                        logger.error(f"Sell order failed: {error_msg}")
            
            # 5. Check pending orders
            pending = query_order(pair=TRADING_PAIR, pending_only=True)
            if pending and pending.get('Success'):
                pending_count = len(pending.get('OrderMatched', []))
                if pending_count > 0:
                    logger.info(f"Pending orders: {pending_count}")
            
            # 6. Update stats
            self.stats['last_check'] = time.time()
            
        except Exception as e:
            logger.error(f"Error in trading iteration: {e}", exc_info=True)
    
    def run(self):
        """Main bot loop"""
        if not self.initialize():
            logger.error("Bot initialization failed. Exiting.")
            return
        
        self.running = True
        logger.info(f"Starting trading bot with strategy: {self.strategy.name}")
        logger.info(f"Trading pair: {TRADING_PAIR}")
        logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
        
        try:
            while self.running:
                self.run_iteration()
                
                # Log stats periodically
                if self.stats['total_orders'] % 10 == 0 and self.stats['total_orders'] > 0:
                    success_rate = (self.stats['successful_orders'] / self.stats['total_orders']) * 100
                    logger.info(f"Stats: {self.stats['total_orders']} orders, "
                              f"{self.stats['successful_orders']} successful "
                              f"({success_rate:.1f}%)")
                
                # Sleep before next iteration
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error in bot loop: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info("Bot stopped")
            logger.info(f"Final stats: {self.stats}")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point"""
    # Create strategy instance
    strategy = TradingStrategy()
    
    # Create bot instance
    bot = TradingBot(strategy)
    
    # Run bot
    bot.run()


if __name__ == "__main__":
    main()
