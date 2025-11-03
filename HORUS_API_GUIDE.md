# Horus API Documentation Guide

## 📚 Tài Liệu Tham Khảo

- **Website:** https://horusdata.xyz/home
- **API Docs:** Available on website (link: API Docs ↗)
- **Platform:** Alternative Investment Data Platform

---

## 🎯 Giới Thiệu về Horus

### Về Horus

**Horus** là một platform cung cấp dữ liệu cho **alternative assets** (tài sản thay thế), bao gồm:

- **Digital assets** (tài sản số)
- **Real estate** (bất động sản)
- **Commodities** (hàng hóa)
- Và nhiều loại tài sản khác

### Tại sao sử dụng Horus trong Hackathon?

- ✅ **Data Partner** được sponsor cho competition
- ✅ **Real-time data** cho crypto markets
- ✅ **Predictive analytics** và machine learning models
- ✅ **Developer-first API** với comprehensive documentation
- ✅ **Flexible rate limits** cho hackathon participants

---

## 🔑 Tính Năng Chính

### 1. Real-Time Data

- **Continuously updated** prices, volume, và market trends
- **Timestamped** data delivery
- **Streamlined data pipeline** cho dashboards và alerts
- Giữ cho dữ liệu luôn current và up-to-date

### 2. Predictive Analytics

- **Proprietary metrics** độc quyền
- **Machine learning models** để surface signals
- **Forecast trends** và screen opportunities
- Phân tích across alternative markets

### 3. Market Vision

- **Dashboards** và visualizations
- **Reveal patterns** across markets
- **Clear, intuitive** interface
- Ready to act on insights

### 4. Developer-First API

- **RESTful APIs** design
- **Seamless integration** vào applications
- **Comprehensive documentation**
- **Flexible rate limits**

---

## 🔌 API Overview

### API Structure

Horus cung cấp RESTful API với:

```
Base URL: (Check API Documentation)
```

### Authentication

(Từ API Documentation - cần check chi tiết trên website)

Thường sẽ bao gồm:
- **API Key** authentication
- **Rate limiting** (flexible cho hackathon)
- **Endpoint-specific** requirements

### Common Endpoints (Expected)

Dựa trên tính năng platform, API có thể cung cấp:

1. **Market Data Endpoints**
   - Real-time prices
   - Volume data
   - Market trends

2. **Analytics Endpoints**
   - Predictive signals
   - Forecasting models
   - Risk metrics

3. **Historical Data Endpoints**
   - Historical prices
   - Historical volume
   - Historical trends

---

## 💻 Integration với Trading Bot

### Use Case trong Hackathon

Horus data có thể được sử dụng để:

1. **Market Analysis**
   - Real-time price feeds
   - Volume analysis
   - Trend identification

2. **Signal Generation**
   - Predictive analytics signals
   - ML model predictions
   - Risk assessment

3. **Strategy Enhancement**
   - Combine với Roostoo platform data
   - Multi-source data validation
   - Enhanced decision making

### Example Integration Pattern

```python
import requests
import time

# Horus API Configuration
HORUS_API_KEY = "your-horus-api-key"  # From hackathon email
HORUS_BASE_URL = "https://api.horusdata.xyz"  # Check actual URL in docs

def get_horus_market_data(symbol: str):
    """
    Get market data from Horus API
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC/USD")
    
    Returns:
        dict: Market data
    """
    url = f"{HORUS_BASE_URL}/market/data"
    headers = {
        "Authorization": f"Bearer {HORUS_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "symbol": symbol
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting Horus data: {e}")
        return None

def get_horus_signals(symbol: str):
    """
    Get predictive signals from Horus
    
    Args:
        symbol: Trading pair symbol
    
    Returns:
        dict: Predictive signals and analytics
    """
    url = f"{HORUS_BASE_URL}/analytics/signals"
    headers = {
        "Authorization": f"Bearer {HORUS_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "symbol": symbol
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting Horus signals: {e}")
        return None

# Integration với trading bot
def enhanced_strategy_with_horus(ticker, balance):
    """
    Enhanced strategy using Horus data
    """
    # Get Horus market data
    horus_data = get_horus_market_data("BTC/USD")
    
    # Get Horus signals
    horus_signals = get_horus_signals("BTC/USD")
    
    # Combine với Roostoo ticker data
    # Make trading decision based on multiple data sources
    
    if horus_signals and horus_signals.get('buy_signal'):
        # Use Horus predictive analytics
        return "BUY"
    elif horus_signals and horus_signals.get('sell_signal'):
        return "SELL"
    
    return "HOLD"
```

---

## 📋 Hackathon Context

### Nhận API Access

Từ hackathon email (Oct 31):
- Horus API documentation sẽ được gửi
- API keys có thể được cung cấp (hoặc instructions để apply)

### Khuyến Khích Sử Dụng

Từ Problem Statement:
> "You're encouraged to use Horus data source, but you're welcome to use any available data source out there."

### Cost Consideration

**Quan trọng:**
- Horus data được **sponsor** cho competition
- **KHÔNG có cost** cho participants trong hackathon period
- Check với organizers về rate limits và access details

---

## 🔗 Accessing API Documentation

### Steps để Access API Docs

1. **Visit:** https://horusdata.xyz/home
2. **Click:** "API Docs ↗" link (top navigation)
3. **Review:** API endpoints và authentication methods
4. **Get Credentials:** Từ hackathon email hoặc contact organizers

### Alternative Access

- **Contact:** Organizers qua email hoặc WhatsApp group
- **Email:** hackathon@roostoo.com
- **WhatsApp:** https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr

---

## 💡 Best Practices

### 1. Rate Limiting

- Respect API rate limits
- Implement request throttling
- Cache data khi có thể
- Use efficient polling intervals

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Rate limiter decorator"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

# Usage
@rate_limit(calls_per_minute=30)
def get_horus_data():
    # Your API call
    pass
```

### 2. Error Handling

```python
def safe_horus_call(func):
    """Decorator for safe Horus API calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            logger.warning("Horus API timeout - using fallback")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Horus API error: {e}")
            return None
    return wrapper
```

### 3. Data Caching

```python
from functools import lru_cache
import time

# Cache Horus data for 30 seconds
@lru_cache(maxsize=128)
def get_cached_horus_data(symbol: str, timestamp: int):
    """
    Get Horus data with caching
    
    Args:
        symbol: Trading symbol
        timestamp: Current timestamp (for cache invalidation)
    """
    # Round timestamp to 30-second intervals for caching
    cache_key = (symbol, timestamp // 30)
    return get_horus_market_data(symbol)
```

### 4. Multi-Source Validation

```python
def validate_with_multiple_sources(symbol: str):
    """
    Validate trading signals using multiple data sources
    """
    # Get data from multiple sources
    roostoo_ticker = get_ticker(symbol)  # From Roostoo API
    horus_data = get_horus_market_data(symbol)  # From Horus
    
    # Compare và validate
    if roostoo_ticker and horus_data:
        roostoo_price = roostoo_ticker.get('Ticker', {}).get('LastPrice', 0)
        horus_price = horus_data.get('price', 0)
        
        # Price validation
        price_diff = abs(roostoo_price - horus_price) / roostoo_price
        if price_diff > 0.01:  # More than 1% difference
            logger.warning(f"Price mismatch: Roostoo={roostoo_price}, Horus={horus_price}")
        
        return {
            'roostoo': roostoo_ticker,
            'horus': horus_data,
            'validated': price_diff < 0.01
        }
    
    return None
```

---

## 📊 Integration với Bot Template

### Enhanced Bot với Horus Data

```python
# In bot_template.py, enhance TradingStrategy class

class EnhancedStrategyWithHorus(TradingStrategy):
    """Trading strategy enhanced with Horus data"""
    
    def __init__(self):
        super().__init__()
        self.horus_enabled = True
        self.horus_data_cache = {}
        self.horus_signal_cache = {}
    
    def get_horus_indicators(self, symbol: str):
        """Get Horus indicators and signals"""
        # Get from Horus API
        signals = get_horus_signals(symbol)
        
        if signals:
            # Cache signals
            self.horus_signal_cache[symbol] = {
                'data': signals,
                'timestamp': time.time()
            }
        
        return signals
    
    def should_buy(self, ticker: Dict, balance: Dict) -> bool:
        """Enhanced buy logic with Horus data"""
        # Base strategy logic
        base_signal = super().should_buy(ticker, balance)
        
        # Get Horus signals
        horus_signals = self.get_horus_indicators(TRADING_PAIR)
        
        if horus_signals:
            # Use Horus predictive analytics
            buy_signal = horus_signals.get('buy_signal', False)
            confidence = horus_signals.get('confidence', 0)
            
            # Combine signals
            if buy_signal and confidence > 0.7:
                return True
        
        return base_signal
    
    def should_sell(self, ticker: Dict, balance: Dict) -> bool:
        """Enhanced sell logic with Horus data"""
        # Similar to should_buy
        base_signal = super().should_sell(ticker, balance)
        
        horus_signals = self.get_horus_indicators(TRADING_PAIR)
        
        if horus_signals:
            sell_signal = horus_signals.get('sell_signal', False)
            confidence = horus_signals.get('confidence', 0)
            
            if sell_signal and confidence > 0.7:
                return True
        
        return base_signal
```

---

## 🔍 Data Sources Comparison

### Roostoo vs Horus

| Feature | Roostoo | Horus |
|---------|---------|-------|
| **Purpose** | Trading execution | Market data & analytics |
| **Real-time Prices** | ✅ | ✅ |
| **Trading** | ✅ Execute orders | ❌ Data only |
| **Predictive Analytics** | ❌ | ✅ |
| **ML Signals** | ❌ | ✅ |
| **Historical Data** | Limited | ✅ Extensive |
| **Cost** | Free (sponsored) | Free (sponsored) |

### Best Practice: Combine Both

```
┌─────────────┐
│   Horus     │ → Market Data, Signals, Analytics
│     API     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Trading   │ → Decision Making Logic
│   Strategy  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Roostoo   │ → Execute Trades
│     API     │
└─────────────┘
```

---

## 📝 Checklist

### Setup Horus Integration

- [ ] Visit https://horusdata.xyz/home
- [ ] Access API Documentation
- [ ] Get API credentials từ hackathon email
- [ ] Test API connection
- [ ] Understand rate limits
- [ ] Implement error handling
- [ ] Add caching layer
- [ ] Integrate với bot strategy
- [ ] Test với mock data
- [ ] Monitor API usage

---

## 🆘 Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify key từ hackathon email
   - Check authentication format
   - Contact organizers nếu vẫn lỗi

2. **Rate Limit Exceeded**
   - Implement request throttling
   - Cache data appropriately
   - Reduce polling frequency

3. **Data Not Updating**
   - Check API endpoint
   - Verify timestamp handling
   - Clear cache nếu cần

4. **Integration Issues**
   - Verify data format matches
   - Check error responses
   - Log API calls để debug

---

## 📚 Resources

- **Website:** https://horusdata.xyz/home
- **API Docs:** Available trên website (click "API Docs ↗")
- **Hackathon Support:** hackathon@roostoo.com
- **WhatsApp Group:** https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr

---

## 💡 Strategy Ideas với Horus

### 1. Signal-Based Trading
- Sử dụng Horus predictive signals
- Combine với technical indicators
- High confidence signals only

### 2. Multi-Timeframe Analysis
- Horus data cho different timeframes
- Cross-validate với Roostoo prices
- Trend confirmation

### 3. Risk Assessment
- Horus risk metrics
- Portfolio-level risk analysis
- Dynamic position sizing

### 4. Market Regime Detection
- Horus market vision dashboards
- Identify market regimes
- Adapt strategy accordingly

---

*Tài liệu này dựa trên thông tin từ Horus website và hackathon context. Chi tiết API sẽ được cung cấp trong hackathon email hoặc API documentation.*

**Lưu ý:** API endpoints, authentication methods, và exact response formats cần được verify từ official API documentation sau khi nhận được credentials từ hackathon organizers.

