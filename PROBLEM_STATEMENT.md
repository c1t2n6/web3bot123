# Problem Statement – HK University Web3 Quant Hackathon

## 🎯 Competition: AI Web3 Trading Bot Competition

### Nhiệm vụ chính

Phát triển một trong các loại thuật toán sau để cạnh tranh trên **Roostoo's real-time mock exchange backend**:

1. **AI-driven trading algorithm** (Thuật toán giao dịch dựa trên AI)
2. **Traditional quantitative rule-based algorithm** (Thuật toán định lượng dựa trên quy tắc truyền thống)
3. **Hybrid strategy** (Chiến lược kết hợp)

### Yêu cầu kỹ thuật

#### Tự động hóa hoàn toàn
- Thiết kế trading bot có khả năng đưa ra quyết định **mua, giữ, và bán tự động** mà không cần can thiệp thủ công
- Tất cả quyết định phải được thực hiện bởi bot

#### Tương tác với Roostoo Exchange
- Sử dụng **POST và GET API requests** để tương tác với **Roostoo backend exchange engine**
- Tham khảo: **Roostoo API Documents**

### Mục tiêu

**Tối đa hóa portfolio returns đồng thời tối thiểu hóa rủi ro**

#### Metrics được sử dụng:
1. **Portfolio Return** - Tổng lợi nhuận
2. **Sortino Ratio** - Đo lường return trên downside risk
3. **Sharpe Ratio** - Đo lường excess return trên total risk
4. **Calmar Ratio** - Đo lường return so với maximum drawdown

---

## 🚀 Cơ Hội Đặc Biệt

Đây là cơ hội duy nhất để thể hiện kỹ năng **algorithmic trading và AI** trong môi trường:
- **Cạnh tranh khốc liệt**
- **Real-time**
- **Web3 crypto markets**

---

## 📋 Requirements Chi Tiết

### 1. Strategies và Bot Usage

**Open-ended** - Không giới hạn cách tiếp cận!

Bạn có thể sử dụng:
- ✅ **LLM (Large Language Model) models**
- ✅ **Reinforcement Learning algorithms** (ví dụ: PPO agents)
- ✅ **Traditional trading strategies**
- ✅ **Custom solutions** built from scratch

### 2. Data Sources và Costs

#### Nguồn dữ liệu:
- ✅ **Bất kỳ nguồn dữ liệu nào** - Tự do sử dụng
- ✅ **Khuyến khích:** Sử dụng **Horus** (data partner đã sponsor data cho competition)
- ✅ **Roostoo platform data** - Miễn phí qua API GET requests (chi tiết trong documentation)

#### Chi phí:
- ✅ **Roostoo sẽ cover:** Cloud server costs (AWS EC2)
- ⚠️ **KHÔNG cover:** Additional data source costs
  - Ví dụ: LLM API calls
  - Ví dụ: Premium data subscriptions
  - → Bạn tự trả các chi phí này

### 3. Competition Leaderboard

- **Roostoo sẽ hiển thị bot names** trên Roostoo app
- Tạo **live competition leaderboard** giữa các teams
- Theo dõi performance real-time

### 4. Performance Tracking

Bạn có thể theo dõi bot performance qua các platform:

- **iOS App:** `https://apps.apple.com/us/app/roostoo-mock-crypto-trading/id1483561353`
- **Android App:** `https://play.google.com/store/apps/details?id=com.roostoo.roostoo&hl=en`
- **Webapp:** `app.roostoo.com`

### 5. Access Restriction

- ⚠️ **Bạn KHÔNG có access** đến competition account qua frontend
- **Lý do:** Ngăn chặn manual trades để đảm bảo tính công bằng
- **Tất cả trades PHẢI** được thực hiện qua API từ bot

### 6. Logging Recommendation

**Khuyến nghị mạnh mẽ:**

1. **Record tất cả trades** của bot internally
2. **Track performance logs** của bot
3. **Track success/failure status** của mỗi API request

**Lý do:**
- Debug issues
- Analyze performance
- Prepare cho final presentation
- Validate results

### 7. Deployment Requirement

- ✅ **PHẢI deploy** bot trên **AWS VM** (Virtual Machine)
- ✅ Bot **PHẢI** được config để execute trades tự động trên Roostoo platform
- ✅ Bot phải chạy 24/7 trong competition period

---

## 📅 Timeline

### Competition Duration
- **2 tuần** chạy trên AWS cloud infrastructure
- Infrastructure được provision bởi Roostoo

### Preparation Period
- **10 ngày** để chuẩn bị
- Bao gồm thời gian trong hackathon để finalize, build, và deploy bots

#### Chi tiết:
- **Oct 29:** Online Info Session & Workshop
- **Nov 1 – Nov 10:** Preparation Period
  - Build your bot
  - Test deployment trên Roostoo

### Trading Competition
- **Nov 10 – Nov 24:** Live trading bắt đầu
  - **2 tuần** competition chính thức
  - **Cho phép:** Optional one-time update và redeployment của codebase
  - Cho strategy iteration và cải thiện

### Final Submission Deadline
- **Dec 1:** Final Submission Deadline
  - Presentation decks
  - Code repositories

### Grand Finale
- **Dec 1 – Dec 5:** Grand Finale @ HKU/HKUST
  - Demo presentations với industry judges
  - Awards ceremony

---

## 🏆 Evaluation Criteria

### 1st Award - Portfolio Return

**Công thức:**
```
Portfolio Return = (Final Portfolio Value - Initial Portfolio Value) / Initial Portfolio Value
```

**Mục tiêu:** Tối đa hóa portfolio return

---

### 2nd Award - Risk-adjusted Return

**Composite Score** được tính từ 3 financial ratios với weight:

#### 0.4x Sortino Ratio

**Định nghĩa:** Measures return per unit of **downside risk** (bad volatility only)

**Công thức:**
```
Sortino Ratio = R_p / σ_d
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns
- `σ_d` = Standard Deviation of Negative Portfolio Returns

**Ý nghĩa:** 
- Chỉ đo lường downside volatility (giá giảm)
- Bỏ qua upside volatility (giá tăng)
- Tốt cho strategies tập trung vào risk management

#### 0.3x Sharpe Ratio

**Định nghĩa:** Measures excess return per unit of **total risk** (volatility)

**Công thức:**
```
Sharpe Ratio = R_p / σ_p
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns
- `σ_p` = Standard Deviation of Portfolio Returns

**Ý nghĩa:**
- Đo lường tất cả volatility (cả tăng và giảm)
- Metric phổ biến nhất trong quantitative finance
- Cân bằng giữa return và risk

#### 0.3x Calmar Ratio

**Định nghĩa:** Measures return relative to **maximum drawdown** (focuses on capital loss risk)

**Công thức:**
```
Calmar Ratio = R_p / Max Drawdown
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns
- `Max Drawdown` = Largest Portfolio peak-to-trough decline

**Ý nghĩa:**
- Tập trung vào capital preservation
- Đo lường rủi ro mất vốn lớn nhất
- Quan trọng cho risk-averse strategies

#### Transparent Calculation

- Tất cả underlying data và calculations sẽ được **transparently published** vào finale day
- Đảm bảo công bằng và minh bạch

---

### 3rd Award - Best Strategy/Technique

- Được chọn bởi **finale judges**
- Dựa trên **best presentations**
- Đánh giá:
  - Innovation
  - Technical execution
  - Strategy effectiveness
  - Presentation quality

---

## 📜 Rules and Constraints

### 1. Prohibited Strategies

**KHÔNG được phép:**
- ❌ **High-frequency trading (HFT)**
- ❌ **Market-making**
- ❌ **Arbitrage strategies**

**Lý do:** 
- Sẽ dẫn đến excessive server requests
- API responses sẽ failed
- Không phù hợp với mục tiêu competition

### 2. Permitted Trading

- ✅ **CHỈ spot trading**
- ✅ Trên **tất cả available cryptocurrencies** trên Roostoo
- ❌ **KHÔNG được phép:**
  - Leverage (Đòn bẩy)
  - Short selling (Bán khống)

### 3. Commission Fee

- Mỗi executed order sẽ incur **0.1% commission fee**
- Cần tính toán vào strategy để đảm bảo profitability

### 4. Code Submission

- ✅ **PHẢI submit** repositories dưới dạng **open-source**
- Để code validation và đảm bảo công bằng

### 5. AWS Provision

- Mỗi team sẽ được cung cấp **AWS sub-account**
- Để launch **EC2 instance** cho hosting bot trên cloud

---

## 📚 Resources

### Luma Page
- **HK University Web3 Quant Trading Hackathon Competition**
- Link: [Luma Page](https://lu.ma/) (URL đầy đủ sẽ được cung cấp)

### WhatsApp Group
- **Technical và general inquiries**
- Link: `https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr?mode=ems_copy_c`

### Roostoo API
- **Roostoo-API-Documents**
- GitHub: `https://github.com/roostoo/Roostoo-API-Documents`

### AWS Guide
- **How-to-Sign-In-and-Launch-Your-Bot**
- Notion: `https://www.notion.so/Hackathon-Guide-How-to-Sign-In-and-Launch-Your-Bot-updated-29482203adbe80539adfdd37bcd68efb?source=copy_link`

### Horus API
- **Horus Data Source**
- Website: `horusdata.xyz`
- Được sponsor cho competition

---

## 💡 Gợi Ý Chiến Lược

### 1. Data-Driven Approach
- Sử dụng Horus API cho market data
- Combine với Roostoo platform data
- Technical indicators
- Sentiment analysis (nếu có)

### 2. Risk Management
- Implement position sizing
- Stop-loss mechanisms
- Portfolio diversification
- Drawdown controls
- Optimize cho Sortino, Sharpe, và Calmar ratios

### 3. Strategy Types

#### AI-Driven:
- LLM-based decision making
- Reinforcement Learning (PPO, DQN, etc.)
- Deep Learning models

#### Traditional:
- Mean reversion
- Momentum strategies
- Pairs trading
- Breakout strategies

#### Hybrid:
- Combine AI signals với traditional filters
- Ensemble methods

### 4. Technical Considerations

- **API Rate Limiting:** Không spam requests
- **Error Handling:** Robust error handling
- **Connection Stability:** Handle disconnections
- **Logging:** Comprehensive logging
- **Backtesting:** Validate strategy trước khi deploy

---

*Tài liệu này dựa trên Problem Statement từ HK University Web3 Quant Trading Hackathon*

