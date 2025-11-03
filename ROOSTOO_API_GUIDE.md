# Roostoo API Documentation Guide

## 📚 Tài Liệu Tham Khảo

- **GitHub Repository:** https://github.com/roostoo/Roostoo-API-Documents
- **Python Demo Code:** Available in the repository
- **Base API URL:** `https://mock-api.roostoo.com`

---

## 🔐 Authentication & Security

### API Keys

- **API_KEY** và **SECRET_KEY** sẽ được generate và gửi khi Roostoo cấp permission
- **Apply API permission:** Gửi email đến developer group `jolly@roostoo.com`

### Access Security Levels

#### 1. RCL_TSCheck
- Chỉ cần **timestamp** parameter
- Endpoints cơ bản

#### 2. RCL_TopLevelCheck (SIGNED)
- **Yêu cầu:**
  - `RST-API-KEY` trong header
  - `MSG-SIGNATURE` trong header
  - `timestamp` parameter (13-digit millisecond timestamp)
- Sử dụng cho endpoints quan trọng (trading, account info)

### RCL_TopLevelCheck Security Implementation

#### Signature Generation

1. **Algorithm:** HMAC SHA256
2. **Key:** Your `SECRET_KEY`
3. **Value:** `totalParams`
   - **GET request:** `totalParams` = query string
   - **POST request:** `totalParams` = request body

#### Headers Required

```
RST-API-KEY: <your-api-key>
MSG-SIGNATURE: <hmac-sha256-signature>
Content-Type: application/x-www-form-urlencoded (for POST)
```

#### Timing Security

- `timestamp` phải là 13-digit millisecond timestamp
- Server sẽ kiểm tra:
  ```python
  if abs(serverTime - timestamp) <= 60*1000:  # 60 seconds
      # process request
  else:
      # reject request
  ```
- **Request sẽ bị reject nếu timestamp chênh lệch > 60 giây**

---

## 📝 SIGNED Endpoint Examples

### Example 1: POST Request (Place Order)

**Request:**
```http
POST /v3/place_order
Content-Type: application/x-www-form-urlencoded
RST-API-KEY: your-api-key
MSG-SIGNATURE: <generated-signature>

pair=BTC/USD&side=BUY&type=MARKET&quantity=0.1&timestamp=1570198992695
```

**Signature Generation:**
```bash
# Using OpenSSL
totalParams="pair=BTC/USD&side=BUY&type=MARKET&quantity=0.1&timestamp=1570198992695"
signature=$(echo -n "$totalParams" | openssl dgst -sha256 -hmac "your-secret-key")
```

### Example 2: GET Request (Query Order)

**Request:**
```http
GET /v3/query_order?order_id=123&timestamp=1570198992695
RST-API-KEY: your-api-key
MSG-SIGNATURE: <generated-signature>
```

**Signature Generation:**
```bash
# Query string for signature
totalParams="order_id=123&timestamp=1570198992695"
signature=$(echo -n "$totalParams" | openssl dgst -sha256 -hmac "your-secret-key")
```

---

## 🔌 API Endpoints

### 1. Check Server Time

```
GET /v3/server_time
Auth: RCL_TSCheck
```

**Purpose:** Lấy server time để sync timestamp

**Response:**
```json
{
  "ServerTime": 1570198992695
}
```

**Usage:** Sử dụng giá trị này để tạo timestamp cho các requests khác

---

### 2. Exchange Information

```
GET /v3/exchange_info
Auth: RCL_TSCheck
```

**Purpose:** Lấy thông tin về exchange, trading pairs, etc.

**Response:** (Chi tiết trong API docs)

---

### 3. Get Market Ticker

```
GET /v3/ticker
Auth: RCL_TSCheck
```

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| pair | STRING | NO | Trading pair (e.g., "BTC/USD") |
| timestamp | STRING | YES | 13-digit millisecond timestamp |

**Purpose:** Lấy giá ticker cho trading pair

**Response:**
```json
{
  "Success": true,
  "Ticker": {
    "Pair": "BTC/USD",
    "LastPrice": 8149.07,
    "BidPrice": 8148.50,
    "AskPrice": 8149.60,
    "Volume24h": 1234.56,
    "Change24h": 2.5
  }
}
```

---

### 4. Balance Information

```
POST /v3/balance
Auth: RCL_TopLevelCheck (SIGNED)
```

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| timestamp | STRING | YES | 13-digit millisecond timestamp |

**Purpose:** Lấy balance của tất cả coins trong account

**Response:**
```json
{
  "Success": true,
  "Balance": {
    "BTC": {
      "Available": 10.5,
      "Locked": 2.3,
      "Total": 12.8
    },
    "USD": {
      "Available": 50000,
      "Locked": 10000,
      "Total": 60000
    }
  }
}
```

**Key Fields:**
- `Available`: Số tiền có thể trade ngay
- `Locked`: Số tiền đang trong pending orders
- `Total`: Tổng số tiền (Available + Locked)

---

### 5. Pending Order Count

```
POST /v3/pending_order_count
Auth: RCL_TopLevelCheck (SIGNED)
```

**Parameters:**
| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| timestamp | STRING | YES | 13-digit millisecond timestamp |

**Purpose:** Đếm số pending orders hiện tại

**Response:**
```json
{
  "Success": true,
  "PendingOrderCount": 5
}
```

---

### 6. New Order (Trade)

```
POST /v3/place_order
Auth: RCL_TopLevelCheck (SIGNED)
```

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| pair | STRING | YES | Trading pair (e.g., "BTC/USD") |
| side | STRING | YES | "BUY" or "SELL" |
| type | STRING | YES | "MARKET" or "LIMIT" |
| quantity | STRING | YES | Amount to trade |
| price | STRING | NO | Required if type="LIMIT" |
| stop_type | STRING | NO | "GTC" (Good Till Cancel) default |
| timestamp | STRING | YES | 13-digit millisecond timestamp |

**Order Types:**

1. **MARKET Order**
   - Execute ngay tại giá market
   - Không cần `price` parameter
   - Example: `type=MARKET`

2. **LIMIT Order**
   - Chỉ execute khi đạt giá chỉ định
   - **PHẢI** có `price` parameter
   - Example: `type=LIMIT&price=8000`

**Response - Success:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "OrderDetail": {
    "Pair": "BTC/USD",
    "OrderID": 81,
    "Status": "FILLED",
    "Side": "BUY",
    "Type": "MARKET",
    "Price": 8149.07,
    "Quantity": 0.1,
    "FilledQuantity": 0.1,
    "FilledAverPrice": 8149.07,
    "CommissionChargeValue": 0.08149,
    "CommissionPercent": 0.001
  }
}
```

**Response - Error:**
```json
{
  "Success": false,
  "ErrMsg": "insufficient balance"
}
```

**Commission Fee:**
- Mỗi order sẽ incur **0.1% commission fee** (như đã nêu trong hackathon rules)
- Commission được trừ từ balance

---

### 7. Query Order

```
POST /v3/query_order
Auth: RCL_TopLevelCheck (SIGNED)
```

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| timestamp | STRING | YES | 13-digit millisecond timestamp |
| order_id | STRING | NO | Query by order ID |
| pair | STRING | NO | Query by trading pair |
| offset | STRING_INT | NO | Pagination offset |
| limit | STRING_INT | NO | Max results (default: 100) |
| pending_only | STRING_BOOL | NO | "TRUE" or "FALSE" |

**Important Rules:**
- Khi `order_id` được gửi, **KHÔNG** được gửi các parameters khác
- Nếu không có `order_id` và `pair`, system sẽ match tất cả orders
- `pending_only=TRUE` chỉ lấy pending orders
- Default `limit` = 100 nếu không chỉ định

**Response - Matched Orders:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "OrderMatched": [
    {
      "Pair": "BTC/USD",
      "OrderID": 81,
      "Status": "FILLED",
      "Role": "TAKER",
      "ServerTimeUsage": 0.039723,
      "CreateTimestamp": 1570199071550,
      "FinishTimestamp": 1570199071590,
      "Side": "BUY",
      "Type": "MARKET",
      "StopType": "GTC",
      "Price": 8149.07,
      "Quantity": 11.112,
      "FilledQuantity": 11.112,
      "FilledAverPrice": 8149.07,
      "CoinChange": 11.112,
      "UnitChange": 90552.46584,
      "CommissionCoin": "USD",
      "CommissionChargeValue": 10.866295,
      "CommissionPercent": 0.00012
    },
    {
      "Pair": "BTC/USD",
      "OrderID": 80,
      "Status": "PENDING",
      "Role": "MAKER",
      "CreateTimestamp": 1570198992695,
      "FinishTimestamp": 0,
      "Side": "BUY",
      "Type": "LIMIT",
      "Price": 7893,
      "Quantity": 11.112,
      "FilledQuantity": 0
    }
  ]
}
```

**Order Status:**
- `FILLED`: Order đã được execute hoàn toàn
- `PENDING`: Order đang chờ execute
- `CANCELED`: Order đã bị cancel

**Response - No Match:**
```json
{
  "Success": false,
  "ErrMsg": "no order matched"
}
```

---

### 8. Cancel Order

```
POST /v3/cancel_order
Auth: RCL_TopLevelCheck (SIGNED)
```

**Parameters:**

| Name | Type | Mandatory | Description |
|------|------|-----------|-------------|
| timestamp | STRING | YES | 13-digit millisecond timestamp |
| order_id | STRING | NO | Cancel by order ID |
| pair | STRING | NO | Cancel by trading pair |

**Important Rules:**
- **Chỉ pending orders** mới có thể cancel
- `order_id` và `pair` **chỉ được gửi 0 hoặc 1 parameter**
- Nếu không có cả 2, system sẽ **cancel tất cả pending orders**

**Response:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "CanceledList": [20, 35]
}
```

---

## 💻 Python Implementation Example

### Setup và Helper Functions

```python
import requests
import hmac
import hashlib
import time

BASE_URL = "https://mock-api.roostoo.com"

# Your API credentials (from email)
API_KEY = "your-api-key"
SECRET_KEY = "your-secret-key"

def _get_timestamp():
    """Get current timestamp in milliseconds (13 digits)"""
    return int(time.time() * 1000)

def _get_signed_headers(payload):
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
```

### Check Server Time

```python
def get_server_time():
    """Get server time (Auth: RCL_TSCheck)"""
    url = f"{BASE_URL}/v3/server_time"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Usage
server_time = get_server_time()
print(f"Server Time: {server_time['ServerTime']}")
```

### Get Market Ticker

```python
def get_ticker(pair=None):
    """Get market ticker (Auth: RCL_TSCheck)"""
    url = f"{BASE_URL}/v3/ticker"
    params = {'timestamp': _get_timestamp()}
    if pair:
        params['pair'] = pair
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Usage
ticker = get_ticker("BTC/USD")
print(ticker)
```

### Get Balance

```python
def get_balance():
    """Get account balance (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/balance"
    
    payload = {}
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    response = requests.post(url, headers=headers, data=total_params_string)
    response.raise_for_status()
    return response.json()

# Usage
balance = get_balance()
if balance.get('Success'):
    print("Balance:", balance.get('Balance'))
```

### Place Order

```python
def place_order(pair, side, order_type, quantity, price=None):
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
            raise ValueError("LIMIT order requires price parameter")
        payload['price'] = str(price)
    elif price is not None:
        print("Warning: price parameter ignored for MARKET order")
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error placing order: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

# Usage Examples
# MARKET order
market_order = place_order(
    pair="BTC/USD",
    side="BUY",
    order_type="MARKET",
    quantity="0.1"
)

# LIMIT order
limit_order = place_order(
    pair="ETH/USD",
    side="SELL",
    order_type="LIMIT",
    quantity="1.0",
    price="3000"
)
```

### Query Order

```python
def query_order(order_id=None, pair=None, pending_only=None, limit=None, offset=None):
    """
    Query orders (Auth: RCL_TopLevelCheck)
    
    Args:
        order_id: Query by order ID (mutually exclusive with pair)
        pair: Query by trading pair
        pending_only: True/False to filter pending orders
        limit: Max results (default: 100)
        offset: Pagination offset
    """
    url = f"{BASE_URL}/v3/query_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair
        if pending_only is not None:
            payload['pending_only'] = 'TRUE' if pending_only else 'FALSE'
        if limit:
            payload['limit'] = str(limit)
        if offset:
            payload['offset'] = str(offset)
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying order: {e}")
        return None

# Usage Examples
# Query by order ID
order = query_order(order_id=81)

# Query pending orders for a pair
pending = query_order(pair="BTC/USD", pending_only=True)

# Query all orders for a pair
all_orders = query_order(pair="ETH/USD", limit=50)
```

### Cancel Order

```python
def cancel_order(order_id=None, pair=None):
    """
    Cancel orders (Auth: RCL_TopLevelCheck)
    
    Args:
        order_id: Cancel by order ID (mutually exclusive with pair)
        pair: Cancel by trading pair
        If both None: cancels all pending orders
    """
    url = f"{BASE_URL}/v3/cancel_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair
    # If neither, cancels all pending orders
    
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error canceling order: {e}")
        return None

# Usage Examples
# Cancel specific order
result = cancel_order(order_id=81)

# Cancel all pending orders for a pair
result = cancel_order(pair="BTC/USD")

# Cancel all pending orders
result = cancel_order()
```

---

## ⚠️ Error Handling Best Practices

### 1. Check Response Success

```python
response = place_order(...)
if response and response.get('Success'):
    order_id = response.get('OrderDetail', {}).get('OrderID')
    print(f"Order placed: {order_id}")
else:
    error_msg = response.get('ErrMsg', 'Unknown error')
    print(f"Order failed: {error_msg}")
```

### 2. Handle Network Errors

```python
try:
    response = requests.post(url, ...)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("Request timeout - retry later")
except requests.exceptions.ConnectionError:
    print("Connection error - check network")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
```

### 3. Validate Balance Before Trading

```python
def can_afford_order(pair, side, quantity, price=None):
    """Check if account has sufficient balance"""
    balance = get_balance()
    if not balance.get('Success'):
        return False
    
    # Get quote currency (e.g., USD in BTC/USD)
    quote_currency = pair.split('/')[1]
    
    if side == "BUY":
        # Need quote currency (USD)
        available = balance['Balance'].get(quote_currency, {}).get('Available', 0)
        if price:
            required = float(quantity) * float(price) * 1.001  # +0.1% commission
        else:
            # For MARKET orders, check ticker for current price
            ticker = get_ticker(pair)
            current_price = ticker.get('Ticker', {}).get('LastPrice', 0)
            required = float(quantity) * current_price * 1.001
        return available >= required
    else:  # SELL
        # Need base currency (BTC)
        base_currency = pair.split('/')[0]
        available = balance['Balance'].get(base_currency, {}).get('Available', 0)
        return available >= float(quantity)

# Usage
if can_afford_order("BTC/USD", "BUY", "0.1", "50000"):
    place_order("BTC/USD", "BUY", "LIMIT", "0.1", "50000")
else:
    print("Insufficient balance")
```

---

## 📊 Bot Workflow Example

### Typical Trading Bot Loop

```python
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def trading_bot_loop():
    """Main trading bot loop"""
    
    while True:
        try:
            # 1. Get current balance
            balance = get_balance()
            if not balance.get('Success'):
                logger.error("Failed to get balance")
                time.sleep(5)
                continue
            
            # 2. Get market data
            ticker = get_ticker("BTC/USD")
            if not ticker.get('Success'):
                logger.error("Failed to get ticker")
                time.sleep(5)
                continue
            
            current_price = ticker['Ticker']['LastPrice']
            logger.info(f"Current BTC/USD price: {current_price}")
            
            # 3. Your trading strategy logic here
            # Example: Simple buy/sell based on price
            btc_balance = balance['Balance'].get('BTC', {}).get('Available', 0)
            usd_balance = balance['Balance'].get('USD', {}).get('Available', 0)
            
            # Example strategy: Buy if price < threshold, Sell if price > threshold
            # (Replace with your actual strategy)
            if current_price < 50000 and usd_balance > 1000:
                # Buy signal
                quantity = str(usd_balance / current_price * 0.99)  # Use 99% to account for fees
                order = place_order("BTC/USD", "BUY", "MARKET", quantity)
                if order and order.get('Success'):
                    logger.info(f"Buy order placed: {order['OrderDetail']['OrderID']}")
                else:
                    logger.error(f"Buy order failed: {order.get('ErrMsg')}")
            
            elif current_price > 60000 and btc_balance > 0.01:
                # Sell signal
                quantity = str(btc_balance * 0.99)  # Use 99% to account for fees
                order = place_order("BTC/USD", "SELL", "MARKET", quantity)
                if order and order.get('Success'):
                    logger.info(f"Sell order placed: {order['OrderDetail']['OrderID']}")
                else:
                    logger.error(f"Sell order failed: {order.get('ErrMsg')}")
            
            # 4. Check pending orders
            pending = query_order(pair="BTC/USD", pending_only=True)
            if pending and pending.get('Success'):
                pending_count = len(pending.get('OrderMatched', []))
                if pending_count > 0:
                    logger.info(f"Pending orders: {pending_count}")
            
            # 5. Wait before next iteration
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
            time.sleep(10)

# Run bot
if __name__ == "__main__":
    trading_bot_loop()
```

---

## 🔍 Testing Checklist

### Before Competition

- [ ] Test API connection với test keys
- [ ] Verify signature generation đúng
- [ ] Test tất cả endpoints
- [ ] Handle errors properly
- [ ] Log tất cả trades và API calls
- [ ] Test với different trading pairs
- [ ] Verify commission calculation
- [ ] Test order cancellation
- [ ] Test balance checking

### Common Issues

1. **Signature Mismatch**
   - Check: Parameters sorting
   - Check: Encoding (UTF-8)
   - Check: Secret key đúng

2. **Timestamp Error**
   - Sync với server time
   - Check: 13-digit millisecond timestamp

3. **Insufficient Balance**
   - Always check balance trước khi place order
   - Account for commission (0.1%)

4. **Order Status**
   - Monitor pending orders
   - Handle filled/canceled orders

---

## 📚 Additional Resources

- **Official GitHub:** https://github.com/roostoo/Roostoo-API-Documents
- **Python Demo Code:** Check repository for `python_demo.py`
- **Partner Demo:** Check `partner_python_demo.py` for partner-specific examples
- **Email Support:** jolly@roostoo.com

---

*Tài liệu này dựa trên Roostoo API Documentation từ GitHub repository*

