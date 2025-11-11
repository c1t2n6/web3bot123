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
from typing import Optional, Dict, Any, cast

# New imports for multi-asset support, utilities and environment loading
import numpy as np
from datetime import datetime
from collections import deque
from enum import Enum
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


def get_ohlc_from_horus(pair: str, timeframe: str = '15m', limit: int = 50) -> Optional[list]:
    """Fetch historical OHLC candlestick data from Horus API

    Args:
        pair: Trading pair (e.g., 'BTC/USD')
        timeframe: Candle timeframe '1m', '5m', '15m', '1h', '4h', '1d'
        limit: Number of candles to fetch (default 50)

    Returns:
        list: OHLC candles with timestamp, open, high, low, close, volume
        Returns None if API call fails
    """
    horus_pair = pair.replace('/', '-')
    url = f"{HORUS_BASE_URL}/ohlc"

    headers = {
        'Authorization': f'Bearer {HORUS_API_KEY}',
        'Content-Type': 'application/json'
    }

    params = {
        'pair': horus_pair,
        'interval': timeframe,
        'limit': limit
    }

    try:
        logger.debug(f"Fetching OHLC from Horus: {pair} {timeframe}")
        response = requests.get(url, headers=headers, params=params, timeout=HORUS_REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data.get('success') or data.get('data'):
            candles_raw = data.get('data', data.get('candles', []))
            candles = []

            for candle in candles_raw:
                # Normalize timestamp (some APIs return ms)
                ts = candle.get('timestamp', 0)
                if isinstance(ts, (int, float)) and ts > 1000000000000:
                    ts = int(ts / 1000)
                candles.append({
                    'timestamp': int(ts),
                    'open': float(candle.get('open', 0)),
                    'high': float(candle.get('high', 0)),
                    'low': float(candle.get('low', 0)),
                    'close': float(candle.get('close', 0)),
                    'volume': float(candle.get('volume', 0))
                })

            if not candles:
                logger.warning(f"No candle data returned from Horus for {pair}")
                return None

            logger.debug(f"Fetched {len(candles)} candles for {pair}")
            if timeframe not in OHLC_HISTORY:
                OHLC_HISTORY[timeframe] = {}
            OHLC_HISTORY[timeframe][pair] = deque(candles, maxlen=CANDLE_HISTORY_SIZE)
            return candles
        else:
            error_msg = data.get('error', data.get('message', 'Unknown error'))
            logger.error(f"Horus API error for {pair}: {error_msg}")
            return None

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout fetching OHLC from Horus for {pair}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error to Horus API: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching OHLC from Horus for {pair}: {e}")
        return None


def get_horus_available_pairs() -> Optional[list]:
    """Fetch list of available trading pairs from Horus"""
    url = f"{HORUS_BASE_URL}/pairs"
    headers = {
        'Authorization': f'Bearer {HORUS_API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        pairs = data.get('data', data.get('pairs', []))

        if pairs:
            logger.info(f"Fetched {len(pairs)} available pairs from Horus")
            return pairs
        else:
            logger.warning("No pairs returned from Horus")
            return None
    except Exception as e:
        logger.error(f"Error fetching pairs from Horus: {e}")
        return None


# ---------------------------------------------------------------------------
# Fallbacks and Aggregators
# ---------------------------------------------------------------------------

def get_ohlc_from_coingecko(pair: str, limit: int) -> Optional[list]:
    """Fallback: Fetch from CoinGecko if Horus unavailable"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
        coin_symbol = pair.split('/')[0]
        coin_map = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'XRP': 'ripple',
            'ADA': 'cardano', 'SOL': 'solana', 'DOGE': 'dogecoin',
            'LTC': 'litecoin', 'BCH': 'bitcoin-cash', 'LINK': 'chainlink',
            'BNB': 'binancecoin', 'MATIC': 'matic-network', 'ATOM': 'cosmos'
        }

        coin_id = coin_map.get(coin_symbol, coin_symbol.lower())
        response = requests.get(
            url.format(coin_id=coin_id),
            params={'vs_currency': 'usd', 'days': 7},
            timeout=10
        )
        response.raise_for_status()

        ohlc_array = response.json()
        candles = []
        # CoinGecko returns [timestamp, open, high, low, close]
        for item in ohlc_array[-limit:]:
            if len(item) >= 5:
                timestamp, o, h, l, c = item
                candles.append({
                    'timestamp': int(timestamp / 1000),
                    'open': float(o), 'high': float(h), 'low': float(l), 'close': float(c), 'volume': 0
                })
        return candles if candles else None
    except Exception as e:
        logger.warning(f"CoinGecko fallback failed: {e}")
        return None


def get_historical_ohlc(pair: str, timeframe: str = '15m', limit: int = 50) -> Optional[list]:
    """Fetch historical OHLC data - PRIMARY: Horus, FALLBACK: CoinGecko"""
    logger.debug(f"Attempting to fetch {pair} from Horus...")
    candles_horus = get_ohlc_from_horus(pair, timeframe, limit)

    if candles_horus and len(candles_horus) >= 30:
        logger.info(f"Successfully fetched {pair} candles from Horus")
        return candles_horus

    logger.warning(f"Horus unavailable for {pair}, trying CoinGecko fallback...")
    candles_cg = get_ohlc_from_coingecko(pair, limit)

    if candles_cg:
        logger.info(f"Successfully fetched {pair} candles from CoinGecko (fallback)")
        return candles_cg

    logger.error(f"Could not fetch candles for {pair} from any source")
    return None


def get_available_pairs() -> list:
    """Fetch available trading pairs from Horus or use hardcoded list"""
    pairs_from_horus = get_horus_available_pairs()

    if pairs_from_horus:
        global AVAILABLE_PAIRS
        AVAILABLE_PAIRS = pairs_from_horus
        return pairs_from_horus

    logger.warning("Horus unavailable, using hardcoded pairs list")
    AVAILABLE_PAIRS = [
        'BTC/USD', 'ETH/USD', 'XRP/USD', 'BCH/USD', 'LTC/USD',
        'BNB/USD', 'EOS/USD', 'TRX/USD', 'ATOM/USD', 'DOGE/USD',
        'LINK/USD', 'ADA/USD', 'ZRX/USD', 'BAT/USD', 'ETC/USD',
        'ZEC/USD', 'DASH/USD', 'MATIC/USD'
    ]
    return AVAILABLE_PAIRS


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

class TradeStatus(Enum):
    """Enumeration for trade lifecycle states"""
    CLOSED = "closed"
    PENDING_BUY = "pending_buy"
    OPEN = "open"
    PENDING_SELL = "pending_sell"
    STOPPED_OUT = "stopped_out"
    PROFIT_TAKEN = "profit_taken"

class TechnicalAnalysis:
    """Implements Craig Percoco's technical analysis framework"""

    @staticmethod
    def detect_fair_value_gap(candles: list) -> dict:
        """Detect Fair Value Gaps (FVG)"""
        if len(candles) < 3:
            return {'bullish_fvgs': [], 'bearish_fvgs': []}

        bullish_fvgs = []
        bearish_fvgs = []

        for i in range(len(candles) - 2):
            c1 = candles[i]
            c2 = candles[i + 1]
            c3 = candles[i + 2]

            c1_body_low = min(c1['open'], c1['close'])
            c1_body_high = max(c1['open'], c1['close'])
            c3_body_low = min(c3['open'], c3['close'])
            c3_body_high = max(c3['open'], c3['close'])

            if (c1['close'] > c1['open'] and c2['close'] > c2['open'] and
                c3['close'] > c3['open'] and c1_body_low > c3_body_high):
                bullish_fvgs.append({
                    'start_idx': i,
                    'gap_high': c1_body_low,
                    'gap_low': c3_body_high,
                    'midpoint': (c1_body_low + c3_body_high) / 2,
                    'timestamp': c3.get('timestamp')
                })

            elif (c1['close'] < c1['open'] and c2['close'] < c2['open'] and
                  c3['close'] < c3['open'] and c1_body_high < c3_body_low):
                bearish_fvgs.append({
                    'start_idx': i,
                    'gap_high': c3_body_low,
                    'gap_low': c1_body_high,
                    'midpoint': (c3_body_low + c1_body_high) / 2,
                    'timestamp': c3.get('timestamp')
                })

        return {'bullish_fvgs': bullish_fvgs, 'bearish_fvgs': bearish_fvgs}

    @staticmethod
    def detect_change_of_character(candles: list, lookback: int = 10) -> dict:
        """Detect Change of Character (CHOCH)"""
        if len(candles) < lookback + 2:
            return {'bullish_choch': None, 'bearish_choch': None}

        recent = candles[-lookback:]
        highs = [max(c['open'], c['close']) for c in recent]
        lows = [min(c['open'], c['close']) for c in recent]

        bullish_choch = None
        bearish_choch = None

        if len(highs) >= 3 and highs[-1] > max(highs[-3:-1]):
            bullish_choch = {
                'level': highs[-1],
                'index': len(candles) - 1,
                'type': 'higher_high'
            }

        if len(lows) >= 3 and lows[-1] < min(lows[-3:-1]):
            bearish_choch = {
                'level': lows[-1],
                'index': len(candles) - 1,
                'type': 'lower_low'
            }

        return {'bullish_choch': bullish_choch, 'bearish_choch': bearish_choch}

    @staticmethod
    def detect_trend_structure(candles: list, lookback: int = 20) -> dict:
        """Analyze trend structure and support/resistance"""
        if len(candles) < lookback:
            return {'trend': None, 'support_levels': [], 'resistance_levels': [], 'current_high': 0, 'current_low': 0}

        recent = candles[-lookback:]
        lows = [min(c['open'], c['close']) for c in recent]
        highs = [max(c['open'], c['close']) for c in recent]

        support_levels = []
        for i in range(1, len(lows) - 1):
            if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                support_levels.append(lows[i])

        resistance_levels = []
        for i in range(1, len(highs) - 1):
            if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                resistance_levels.append(highs[i])

        trend = None
        if len(highs) >= 2 and len(lows) >= 2:
            if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
                trend = 'uptrend'
            elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
                trend = 'downtrend'
            else:
                trend = 'range'

        return {
            'trend': trend,
            'support_levels': sorted(set(support_levels), reverse=True)[:3],
            'resistance_levels': sorted(set(resistance_levels), reverse=True)[:3],
            'current_high': highs[-1],
            'current_low': lows[-1]
        }

    @staticmethod
    def calculate_fibonacci_levels(swing_high: float, swing_low: float, direction: str = 'retracement') -> dict:
        """Calculate Fibonacci levels"""
        diff = swing_high - swing_low

        if direction == 'retracement':
            return {
                '23.6%': swing_high - (diff * 0.236),
                '38.2%': swing_high - (diff * 0.382),
                '50.0%': swing_high - (diff * 0.500),
                '61.8%': swing_high - (diff * 0.618),
                '78.6%': swing_high - (diff * 0.786),
            }
        else:
            return {
                '127.2%': swing_low - (diff * 0.272),
                '161.8%': swing_low - (diff * 0.618),
                '261.8%': swing_low - (diff * 1.618),
            }

    @staticmethod
    def calculate_atr(candles: list, period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(candles) < period:
            return 0

        tr_values = []
        for i in range(len(candles) - period, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i-1]['close'] if i > 0 else candles[i]['close']
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            tr_values.append(tr)

        return sum(tr_values) / len(tr_values) if tr_values else 0


class PortfolioManager:
    """Manages portfolio-level metrics and performance tracking"""

    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.portfolio_value_history = [initial_capital]
        self.trades_history = []
        self.returns_history = []

    def get_portfolio_metrics(self) -> dict:
        """Calculate Sharpe, Sortino, Calmar ratios and portfolio performance"""
        if len(self.portfolio_value_history) < 2:
            return {
                'total_return': 0, 'sharpe_ratio': 0, 'sortino_ratio': 0,
                'calmar_ratio': 0, 'max_drawdown': 0, 'current_drawdown': 0,
                'current_value': self.portfolio_value_history[-1], 'risk_adjusted_score': 0
            }

        returns = []
        for i in range(1, len(self.portfolio_value_history)):
            ret = ((self.portfolio_value_history[i] - self.portfolio_value_history[i-1]) /
                   self.portfolio_value_history[i-1])
            returns.append(ret)

        returns_array = np.array(returns)
        mean_return = np.mean(returns_array)
        std_return = np.std(returns_array)

        sharpe = mean_return / std_return if std_return > 0 else 0

        downside_returns = returns_array[returns_array < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0
        sortino = mean_return / downside_std if downside_std > 0 else 0

        peak = self.portfolio_value_history[0]
        max_dd = 0
        current_dd = 0

        for i, value in enumerate(self.portfolio_value_history):
            if value > peak:
                peak = value
            dd = (peak - value) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)
            if i == len(self.portfolio_value_history) - 1:
                current_dd = dd

        annual_return = mean_return * 252
        calmar = annual_return / max_dd if max_dd > 0 else 0

        total_return = ((self.portfolio_value_history[-1] - self.initial_capital) /
                        self.initial_capital)

        risk_adjusted_score = (0.4 * sortino) + (0.3 * sharpe) + (0.3 * calmar)

        return {
            'total_return': total_return, 'sharpe_ratio': sharpe,
            'sortino_ratio': sortino, 'calmar_ratio': calmar,
            'max_drawdown': max_dd, 'current_drawdown': current_dd,
            'current_value': self.portfolio_value_history[-1],
            'risk_adjusted_score': risk_adjusted_score
        }

    def get_current_drawdown(self, current_value: float) -> float:
        """Calculate current drawdown"""
        peak = max(self.portfolio_value_history) if self.portfolio_value_history else current_value
        if peak == 0:
            return 0.0
        return max(0.0, (peak - current_value) / peak)

    def can_open_new_position(self, current_positions_open: int) -> bool:
        """Check if can open new position"""
        if current_positions_open >= MAX_OPEN_POSITIONS:
            logger.warning(f"Max open positions ({MAX_OPEN_POSITIONS}) reached")
            return False

        current_dd = self.get_current_drawdown(self.current_capital)
        if current_dd > MAX_PORTFOLIO_DRAWDOWN:
            logger.warning(f"Portfolio drawdown {current_dd:.2%} exceeds limit")
            return False

        return True

    def log_trade(self, pair: str, side: str, quantity: float, price: float,
                  order_id: str, stop_loss: float, target: float):
        """Log trade execution"""
        trade = {
            'timestamp': datetime.now().isoformat(),
            'pair': pair, 'side': side, 'quantity': quantity, 'price': price,
            'order_id': order_id, 'stop_loss': stop_loss, 'target': target,
            'commission': quantity * price * 0.001,
            'risk_reward_ratio': (target - price) / (price - stop_loss) if price != stop_loss else 0
        }
        self.trades_history.append(trade)
        logger.info(f"Trade logged: {side} {quantity:.4f} {pair} @ {price:.2f}")

    def update_portfolio_value(self, current_prices: dict, open_positions: dict):
        """Update portfolio value"""
        total_value = self.current_capital

        for pair, position_data in open_positions.items():
            if position_data.get('status') == TradeStatus.OPEN.value:
                position_size = position_data.get('position_size', 0)
                if position_size > 0 and pair in current_prices:
                    total_value += position_size * current_prices[pair]

        self.portfolio_value_history.append(total_value)
        self.current_capital = total_value


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


# ---------------------------------------------------------------------------
# Strategy Implementations
# ---------------------------------------------------------------------------

class PercocolStrategy(TradingStrategy):
    """Implements Craig Percoco's 3-pillar high-probability trading system"""

    def __init__(self):
        super().__init__()
        self.name = "Percoco High-Probability Strategy"
        self.ta = TechnicalAnalysis()
        self.risk_per_trade = 0.02
        self.min_rr_ratio = 2.0
        self.max_position_size = 0.05

    def analyze_setup(self, candles: list, ticker: dict) -> dict:
        """Analyze trading setup on single coin"""

        fvg_data = self.ta.detect_fair_value_gap(candles)
        choch_data = self.ta.detect_change_of_character(candles)
        trend_data = self.ta.detect_trend_structure(candles)

        current_price = ticker.get('Ticker', {}).get('LastPrice', 0)

        bullish_setup = {'valid': False, 'entry_price': None, 'stop_loss': None, 'target': None, 'rr_ratio': 0, 'confidence': 0, 'reason': []}

        if (fvg_data['bullish_fvgs'] and choch_data['bullish_choch'] and trend_data['trend'] in ['uptrend', 'range']):
            latest_fvg = fvg_data['bullish_fvgs'][-1]
            atr = self.ta.calculate_atr(candles)

            entry = latest_fvg['midpoint']
            stop_loss = latest_fvg['gap_low'] - (atr * 0.5)
            fib_levels = self.ta.calculate_fibonacci_levels(latest_fvg['gap_high'], latest_fvg['gap_low'], 'extension')
            target = fib_levels.get('161.8%', latest_fvg['gap_high'] * 1.05)

            risk = entry - stop_loss
            reward = target - entry
            rr = reward / risk if risk > 0 else 0

            confidence = 70
            if rr >= self.min_rr_ratio:
                confidence += 10
            if trend_data['trend'] == 'uptrend':
                confidence += 10
            confidence = min(confidence, 100)

            if rr >= self.min_rr_ratio:
                bullish_setup['valid'] = True
                bullish_setup['entry_price'] = entry
                bullish_setup['stop_loss'] = stop_loss
                bullish_setup['target'] = target
                bullish_setup['rr_ratio'] = rr
                bullish_setup['confidence'] = confidence
                bullish_setup['reason'] = [f'FVG {entry:.2f}', 'Bullish CHOCH', f'Trend: {trend_data["trend"]}', f'R:R {rr:.2f}:1']

        bearish_setup = {'valid': False, 'entry_price': None, 'stop_loss': None, 'target': None, 'rr_ratio': 0, 'confidence': 0, 'reason': []}

        if (fvg_data['bearish_fvgs'] and choch_data['bearish_choch'] and trend_data['trend'] in ['downtrend', 'range']):
            latest_fvg = fvg_data['bearish_fvgs'][-1]
            atr = self.ta.calculate_atr(candles)

            entry = latest_fvg['midpoint']
            stop_loss = latest_fvg['gap_high'] + (atr * 0.5)
            fib_levels = self.ta.calculate_fibonacci_levels(latest_fvg['gap_high'], latest_fvg['gap_low'], 'extension')
            target = fib_levels.get('161.8%', latest_fvg['gap_low'] * 0.95)

            risk = stop_loss - entry
            reward = entry - target
            rr = reward / risk if risk > 0 else 0

            confidence = 70
            if rr >= self.min_rr_ratio:
                confidence += 10
            if trend_data['trend'] == 'downtrend':
                confidence += 10
            confidence = min(confidence, 100)

            if rr >= self.min_rr_ratio:
                bearish_setup['valid'] = True
                bearish_setup['entry_price'] = entry
                bearish_setup['stop_loss'] = stop_loss
                bearish_setup['target'] = target
                bearish_setup['rr_ratio'] = rr
                bearish_setup['confidence'] = confidence
                bearish_setup['reason'] = [f'FVG {entry:.2f}', 'Bearish CHOCH', f'Trend: {trend_data["trend"]}', f'R:R {rr:.2f}:1']

        return {'bullish_setup': bullish_setup, 'bearish_setup': bearish_setup, 'current_price': current_price, 'trend': trend_data['trend']}

    def score_setup(self, setup: dict) -> float:
        """Score setup quality 0-100"""
        if not setup['valid']:
            return 0
        score = setup['confidence']
        if setup['rr_ratio'] > 3:
            score += 10
        elif setup['rr_ratio'] > 2:
            score += 5
        return min(score, 100)

    def calculate_position_size(self, entry_price: float, stop_loss: float, account_balance: float) -> float:
        """Calculate position size"""
        risk_amount = account_balance * self.risk_per_trade
        stop_distance = abs(entry_price - stop_loss)
        if stop_distance == 0:
            return 0
        position_size = risk_amount / stop_distance
        max_size = account_balance / entry_price * self.max_position_size
        return min(position_size, max_size)


class MultiAssetPercocolStrategy(PercocolStrategy):
    """Scans all coins and selects the best opportunity"""

    def __init__(self, portfolio_manager: PortfolioManager):
        super().__init__()
        self.portfolio_manager = portfolio_manager
        self.pair_analysis_cache = {}

    def scan_all_pairs(self) -> dict:
        """Scan all available pairs"""
        opportunities = {}
        logger.info(f"Starting scan of {len(AVAILABLE_PAIRS)} trading pairs...")
        scan_start_time = time.time()
        scanned_count = 0
        skipped_count = 0

        for pair in AVAILABLE_PAIRS:
            try:
                if PORTFOLIO_COINS.get(pair, {}).get('status') == TradeStatus.OPEN.value:
                    skipped_count += 1
                    continue

                candles = get_historical_ohlc(pair, PRIMARY_TIMEFRAME, limit=50)
                if not candles or len(candles) < 30:
                    skipped_count += 1
                    continue

                ticker = get_ticker(pair)
                if not ticker or not ticker.get('Success'):
                    skipped_count += 1
                    continue

                scanned_count += 1
                setup = self.analyze_setup(candles, ticker)
                bullish_score = self.score_setup(setup['bullish_setup'])
                bearish_score = self.score_setup(setup['bearish_setup'])
                best_score = max(bullish_score, bearish_score)

                if best_score > MIN_SETUP_CONFIDENCE:
                    opportunities[pair] = {
                        'bullish_score': bullish_score, 'bearish_score': bearish_score,
                        'best_score': best_score, 'setup': setup,
                        'direction': 'bullish' if bullish_score > bearish_score else 'bearish'
                    }
            except Exception as e:
                logger.error(f"Error scanning {pair}: {e}")
                skipped_count += 1
                continue

        ranked_opportunities = sorted(opportunities.items(), key=lambda x: x[1]['best_score'], reverse=True)
        scan_duration = time.time() - scan_start_time

        logger.info(f"Scan complete: {scanned_count} scanned, {skipped_count} skipped, {len(ranked_opportunities)} found ({scan_duration:.1f}s)")
        for i, (pair, opp) in enumerate(ranked_opportunities[:5]):
            logger.info(f"  #{i+1} {pair}: {opp['best_score']:.0f}% ({opp['direction']})")

        return dict(ranked_opportunities)

    def select_best_opportunity(self, opportunities: dict) -> tuple:
        """Select best opportunity to trade"""
        if not opportunities:
            logger.info("No opportunities found")
            return None, None

        best_pair = list(opportunities.keys())[0]
        best_opportunity = opportunities[best_pair]
        logger.info(f"Selected: {best_pair} (score: {best_opportunity['best_score']:.0f}%)")
        return best_pair, best_opportunity

    def execute_selected_trade(self, pair: str, opportunity: dict, balance: dict):
        """Execute selected trade"""
        direction = opportunity['direction']
        setup_data = opportunity['setup'][direction + '_setup']

        if not setup_data['valid']:
            logger.warning(f"Setup invalid for {pair}")
            return

        available_usd = balance.get('Balance', {}).get('USD', {}).get('Available', 0)
        position_size = self.calculate_position_size(setup_data['entry_price'], setup_data['stop_loss'], available_usd)

        if position_size < 0.001:
            logger.warning(f"Position size too small: {position_size}")
            return

        side = 'BUY' if direction == 'bullish' else 'SELL'

        order = place_order(pair, side, "LIMIT", str(position_size), str(setup_data['entry_price']))

        if order and order.get('Success'):
            order_id = order.get('OrderDetail', {}).get('OrderID')
            PORTFOLIO_COINS.setdefault(pair, {})
            PORTFOLIO_COINS[pair]['position_size'] = position_size
            PORTFOLIO_COINS[pair]['entry_price'] = setup_data['entry_price']
            PORTFOLIO_COINS[pair]['stop_loss'] = setup_data['stop_loss']
            PORTFOLIO_COINS[pair]['target'] = setup_data['target']
            PORTFOLIO_COINS[pair]['status'] = TradeStatus.PENDING_BUY.value
            PORTFOLIO_COINS[pair]['entry_time'] = time.time()
            PORTFOLIO_COINS[pair]['direction'] = direction

            self.portfolio_manager.log_trade(pair, side, position_size, setup_data['entry_price'], order_id, setup_data['stop_loss'], setup_data['target'])
            logger.info(f"Order placed: {order_id}")
        else:
            error = order.get('ErrMsg', 'Unknown error') if order else 'No response'
            logger.error(f"Failed to execute: {error}")


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


# ---------------------------------------------------------------------------
# Multi-asset trading bot (concrete implementation used by main)
# ---------------------------------------------------------------------------

class MultiAssetTradingBot(TradingBot):
    """Main trading bot for multi-asset portfolio"""

    def __init__(self, strategy: MultiAssetPercocolStrategy, portfolio_manager: PortfolioManager):
        super().__init__(strategy)
        self.portfolio_manager = portfolio_manager
        self.scan_interval = SCAN_INTERVAL
        self.last_scan_time = 0
        self.position_check_interval = POSITION_CHECK_INTERVAL
        self.last_position_check = 0

    def initialize(self) -> bool:
        logger.info("="*60)
        logger.info("INITIALIZING MULTI-ASSET TRADING BOT")
        logger.info("="*60)

        if not HORUS_API_KEY:
            logger.error("HORUS_API_KEY not configured")
            return False

        pairs = get_available_pairs()
        if not pairs:
            logger.error("Failed to fetch available pairs")
            return False

        global AVAILABLE_PAIRS
        AVAILABLE_PAIRS = pairs
        logger.info(f"Loaded {len(AVAILABLE_PAIRS)} available pairs")

        initialize_portfolio_tracking()
        return True

    def run_iteration(self):
        current_time = time.time()

        try:
            if current_time - self.last_scan_time > self.scan_interval:
                # cast strategy to concrete type for static analysis
                strategy_var = cast(MultiAssetPercocolStrategy, self.strategy)

                opportunities = strategy_var.scan_all_pairs()
                open_positions_count = sum(1 for d in PORTFOLIO_COINS.values() if d.get('status') == TradeStatus.OPEN.value)

                if self.portfolio_manager.can_open_new_position(open_positions_count):
                    pair, opportunity = strategy_var.select_best_opportunity(opportunities)
                    if pair and opportunity:
                        balance = get_balance()
                        if balance and balance.get('Success'):
                            strategy_var.execute_selected_trade(pair, opportunity, balance)

                self.last_scan_time = current_time

            if current_time - self.last_position_check > self.position_check_interval:
                self._manage_open_positions()
                self._update_portfolio_metrics()
                self.last_position_check = current_time

        except Exception as e:
            logger.error(f"Error in run_iteration: {e}", exc_info=True)

    def _manage_open_positions(self):
        current_prices = {}
        for pair, coin_data in PORTFOLIO_COINS.items():
            if coin_data.get('status') in [TradeStatus.OPEN.value, TradeStatus.PENDING_BUY.value]:
                ticker = get_ticker(pair)
                if ticker and ticker.get('Success'):
                    current_prices[pair] = ticker.get('Ticker', {}).get('LastPrice', 0)

        for pair, coin_data in PORTFOLIO_COINS.items():
            status = coin_data.get('status')
            if status not in [TradeStatus.OPEN.value, TradeStatus.PENDING_BUY.value] or pair not in current_prices:
                continue

            current_price = current_prices[pair]

            if status == TradeStatus.PENDING_BUY.value:
                pending = query_order(pair=pair, pending_only=True)
                if pending and pending.get('Success') and len(pending.get('OrderMatched', [])) > 0:
                    coin_data['status'] = TradeStatus.OPEN.value
                    logger.info(f"✓ {pair} filled at {current_price:.2f}")

            stop_loss = coin_data.get('stop_loss')
            direction = coin_data.get('direction', 'bullish')

            if stop_loss and ((direction == 'bullish' and current_price <= stop_loss) or (direction == 'bearish' and current_price >= stop_loss)):
                logger.warning(f"⚠ {pair} HIT STOP-LOSS")
                self._close_position(pair, "STOP_LOSS", current_price)
                continue

            target = coin_data.get('target')
            if target and ((direction == 'bullish' and current_price >= target) or (direction == 'bearish' and current_price <= target)):
                logger.info(f"✓ {pair} HIT TAKE-PROFIT")
                self._close_position(pair, "TAKE_PROFIT", current_price)

        self.portfolio_manager.update_portfolio_value(current_prices, PORTFOLIO_COINS)

    def _close_position(self, pair: str, reason: str, exit_price: float):
        coin_data = PORTFOLIO_COINS.get(pair, {})
        position_size = coin_data.get('position_size', 0)
        direction = coin_data.get('direction', 'bullish')

        if position_size == 0:
            return

        side = 'SELL' if direction == 'bullish' else 'BUY'
        order = place_order(pair, side, "MARKET", str(position_size), None)

        if order and order.get('Success'):
            pnl = (exit_price - coin_data.get('entry_price', 0)) * position_size * (1 if direction == 'bullish' else -1)
            coin_data['status'] = TradeStatus.CLOSED.value
            coin_data['pnl'] = pnl
            logger.info(f"✓ {pair} closed: PnL=${pnl:,.2f}")

    def _update_portfolio_metrics(self):
        metrics = self.portfolio_manager.get_portfolio_metrics()
        logger.info("\n" + "="*60 + "\nMETRICS\n" + "="*60)
        logger.info(f"Value: ${metrics['current_value']:,.2f} | Return: {metrics['total_return']:+.2%}")
        logger.info(f"Sharpe: {metrics['sharpe_ratio']:.2f} | Sortino: {metrics['sortino_ratio']:.2f} | Calmar: {metrics['calmar_ratio']:.2f}")
        logger.info("="*60)


# Helper to initialize portfolio tracking
def initialize_portfolio_tracking():
    """Initialize portfolio tracking for all coins"""
    global AVAILABLE_PAIRS, PORTFOLIO_COINS
    logger.info("Initializing portfolio tracking...")

    for pair in AVAILABLE_PAIRS:
        PORTFOLIO_COINS[pair] = {
            'position_size': 0,
            'entry_price': None,
            'stop_loss': None,
            'target': None,
            'pnl': 0,
            'status': TradeStatus.CLOSED.value,
            'entry_time': None,
            'last_update': None,
            'direction': None
        }

    logger.info(f"Initialized {len(PORTFOLIO_COINS)} coins")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point"""
    logger.info("\n" + "="*60)
    logger.info("ROOSTOO AI TRADING BOT - CRAIG PERCOCO STRATEGY")
    logger.info("="*60 + "\n")

    initial_capital = 10000.0
    portfolio_manager = PortfolioManager(initial_capital)
    strategy = MultiAssetPercocolStrategy(portfolio_manager)
    bot = MultiAssetTradingBot(strategy, portfolio_manager)

    if not bot.initialize():
        logger.error("Initialization failed")
        return

    logger.info(f"Starting bot loop...\n")
    bot.run()


if __name__ == "__main__":
    main()
