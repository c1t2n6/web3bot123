# Evaluation Criteria - HK Quant Trading Hackathon

## 📊 Tổng Quan

Competition được đánh giá dựa trên **3 awards** khác nhau:
1. **Portfolio Return** (Pure return)
2. **Risk-adjusted Return** (Composite score)
3. **Best Strategy/Technique** (Judges' choice)

Mỗi award có **3 giải** (1st, 2nd, 3rd), tạo tổng cộng **9 giải thưởng**.

---

## 🥇 1st Award - Portfolio Return

### Công Thức

```
Portfolio Return = (Final Portfolio Value - Initial Portfolio Value) / Initial Portfolio Value
```

### Ví Dụ

**Giả sử:**
- Initial Portfolio Value: **$100,000**
- Final Portfolio Value: **$150,000**

**Calculation:**
```
Portfolio Return = ($150,000 - $100,000) / $100,000
                = $50,000 / $100,000
                = 0.50
                = 50%
```

### Chiến Lược Tối Ưu

- ✅ **Tối đa hóa absolute return**
- ✅ **Aggressive strategies** có thể hoạt động tốt
- ⚠️ **Lưu ý:** Vẫn cần quản lý rủi ro để tránh drawdown lớn

### Metrics Tracking

- Track portfolio value mỗi ngày
- Monitor cumulative return
- Compare với leaderboard

---

## 🥈 2nd Award - Risk-adjusted Return

### Composite Score Calculation

```
Composite Score = 0.4 × Sortino Ratio + 0.3 × Sharpe Ratio + 0.3 × Calmar Ratio
```

**Weights:**
- **40%** Sortino Ratio
- **30%** Sharpe Ratio  
- **30%** Calmar Ratio

### Transparent Publication

- Tất cả underlying data và calculations sẽ được **transparently published** vào finale day
- Đảm bảo công bằng và reproducibility

---

## 📈 Sortino Ratio (Weight: 0.4)

### Định Nghĩa

**Measures return per unit of downside risk (bad volatility only)**

### Công Thức

```
Sortino Ratio = R_p / σ_d
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns (trung bình lợi nhuận)
- `σ_d` = Standard Deviation of Negative Portfolio Returns (độ lệch chuẩn của lợi nhuận âm)

### Ưu Điểm

- ✅ **Chỉ đo lường downside volatility** (giá giảm)
- ✅ **Bỏ qua upside volatility** (giá tăng - điều tốt!)
- ✅ Tốt cho strategies tập trung vào **risk management**

### Ví Dụ Tính Toán

**Giả sử daily returns trong 10 ngày:**
```
Day 1: +2%
Day 2: -1%
Day 3: +3%
Day 4: -2%
Day 5: +1%
Day 6: -1%
Day 7: +2%
Day 8: +1%
Day 9: -1%
Day 10: +2%
```

**Calculation:**
- Mean Return (R_p) = (2-1+3-2+1-1+2+1-1+2)/10 = 0.6%
- Negative Returns: [-1%, -2%, -1%, -1%]
- σ_d = Standard Deviation của [-1%, -2%, -1%, -1%]
  - Mean = -1.25%
  - Variance = [(-1-(-1.25))² + (-2-(-1.25))² + (-1-(-1.25))² + (-1-(-1.25))²] / 4
  - σ_d ≈ 0.43%
- **Sortino Ratio = 0.6% / 0.43% ≈ 1.40**

### Chiến Lược Tối Ưu

- Minimize downside volatility
- Limit drawdowns
- Focus trên consistent positive returns

---

## 📊 Sharpe Ratio (Weight: 0.3)

### Định Nghĩa

**Measures excess return per unit of total risk (volatility)**

### Công Thức

```
Sharpe Ratio = R_p / σ_p
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns
- `σ_p` = Standard Deviation of Portfolio Returns (tất cả returns)

### Đặc Điểm

- 📊 **Metric phổ biến nhất** trong quantitative finance
- 📊 Đo lường **tất cả volatility** (cả tăng và giảm)
- 📊 Cân bằng giữa return và risk tổng thể

### Ví Dụ Tính Toán

**Với cùng daily returns ở trên:**

**Calculation:**
- Mean Return (R_p) = 0.6%
- All Returns: [2%, -1%, 3%, -2%, 1%, -1%, 2%, 1%, -1%, 2%]
- σ_p = Standard Deviation của tất cả returns ≈ 1.56%
- **Sharpe Ratio = 0.6% / 1.56% ≈ 0.38**

### Chiến Lược Tối Ưu

- Balance return và volatility tổng thể
- Consistent returns tốt hơn volatile returns
- Focus vào stability

---

## 📉 Calmar Ratio (Weight: 0.3)

### Định Nghĩa

**Measures return relative to maximum drawdown (focuses on capital loss risk)**

### Công Thức

```
Calmar Ratio = R_p / Max Drawdown
```

**Trong đó:**
- `R_p` = Mean of Portfolio Returns
- `Max Drawdown` = Largest Portfolio peak-to-trough decline (largest percentage decline từ peak đến trough)

### Tính Maximum Drawdown

**Ví dụ portfolio value over time:**
```
Day 1: $100,000 (peak)
Day 2: $105,000 (new peak)
Day 3: $102,000
Day 4: $98,000 (trough from Day 2)
Day 5: $110,000 (new peak)
Day 6: $104,000 (trough from Day 5)
Day 7: $115,000 (new peak)
```

**Calculation:**
- Peak 1: $100,000, Trough: $100,000 → Drawdown: 0%
- Peak 2: $105,000, Trough: $98,000 → Drawdown: ($105,000 - $98,000) / $105,000 = 6.67%
- Peak 3: $110,000, Trough: $104,000 → Drawdown: ($110,000 - $104,000) / $110,000 = 5.45%
- Peak 4: $115,000, Trough: $115,000 → Drawdown: 0%

**Max Drawdown = 6.67%**

### Đặc Điểm

- 🎯 **Tập trung vào capital preservation**
- 🎯 Đo lường rủi ro mất vốn lớn nhất
- 🎯 Quan trọng cho **risk-averse strategies**

### Ví Dụ Tính Calmar Ratio

**Giả sử:**
- Mean Return (R_p) = 0.6% per day
- Max Drawdown = 6.67%

**Calmar Ratio = 0.6% / 6.67% ≈ 0.09**

### Chiến Lược Tối Ưu

- Minimize maximum drawdown
- Implement stop-loss mechanisms
- Capital preservation là ưu tiên
- Avoid large losses

---

## 🎯 Tối Ưu Composite Score

### Strategy Optimization

Để tối đa hóa Composite Score, cần balance cả 3 ratios:

```
Maximize: 0.4 × Sortino + 0.3 × Sharpe + 0.3 × Calmar
```

### Recommendations

1. **Minimize Downside Volatility** (Sortino - 40% weight)
   - Limit losses
   - Cut losses quickly
   - Avoid large negative returns

2. **Consistent Returns** (Sharpe - 30% weight)
   - Stable performance
   - Avoid extreme volatility
   - Regular positive returns

3. **Capital Preservation** (Calmar - 30% weight)
   - Prevent large drawdowns
   - Implement risk limits
   - Protect capital

### Trade-offs

- **High Return** vs **Low Risk**: Cần balance
- **Aggressive** vs **Conservative**: Hybrid approach tốt nhất
- **Consistency** vs **Volatility**: Consistency quan trọng hơn

---

## 🏆 3rd Award - Best Strategy/Technique

### Evaluation Method

- Được chọn bởi **finale judges** (industry professionals và professors)
- Dựa trên **presentation quality** và **technical innovation**

### Criteria

1. **Trading Idea & Strategy**
   - Innovation
   - Originality
   - Effectiveness

2. **Technical Execution**
   - Architecture quality
   - Algorithm sophistication
   - Code quality

3. **Risk Management & Controls**
   - Risk management implementation
   - Drawdown controls
   - Position sizing

4. **Results**
   - Live competition results
   - Backtest & validation results

5. **Presentation**
   - Clarity
   - Organization
   - Communication

---

## 📝 Implementation Tips

### 1. Track All Metrics

```python
# Example tracking structure
metrics = {
    'daily_returns': [],
    'portfolio_value': [],
    'drawdowns': [],
    'positive_returns': [],
    'negative_returns': []
}

# Calculate ratios
sortino_ratio = calculate_sortino(metrics)
sharpe_ratio = calculate_sharpe(metrics)
calmar_ratio = calculate_calmar(metrics)
composite_score = 0.4 * sortino_ratio + 0.3 * sharpe_ratio + 0.3 * calmar_ratio
```

### 2. Real-time Monitoring

- Track metrics trong quá trình competition
- Adjust strategy based on performance
- Monitor drawdowns và volatility

### 3. Backtesting

- Test strategy với historical data
- Validate ratios calculations
- Ensure strategy performs well across all metrics

### 4. Optimization

- Optimize cho cả return và risk-adjusted metrics
- Balance aggressive và conservative approaches
- Test different parameter combinations

---

## 📊 Comparison Table

| Metric | Weight | Focus | Best For |
|--------|--------|-------|----------|
| **Portfolio Return** | N/A (Separate award) | Absolute return | Aggressive strategies |
| **Sortino Ratio** | 40% | Downside risk | Risk management |
| **Sharpe Ratio** | 30% | Total volatility | Consistent returns |
| **Calmar Ratio** | 30% | Maximum drawdown | Capital preservation |

---

## 🎯 Key Takeaways

1. **Multiple Winning Opportunities**: Có thể thắng nhiều awards
2. **Balance is Key**: Cần balance return và risk
3. **Risk Management Matters**: 60% của composite score (Sortino + Calmar) focus vào risk
4. **Consistency Wins**: Stable returns tốt hơn volatile returns
5. **Track Everything**: Log all data để tính toán metrics chính xác

---

*Tài liệu này dựa trên Evaluation Criteria từ HK Quant Trading Hackathon*

