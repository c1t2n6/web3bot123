# 📋 Checklist - Những Gì Bạn Cần Làm

## ⏰ Timeline Quan Trọng

| Ngày | Sự Kiện | Hành Động |
|------|---------|-----------|
| **Oct 29** | Online Info Session & Workshop | ✅ Tham dự session |
| **Oct 31** | Nhận Email từ Organizers | ✅ Kiểm tra email, nhận API keys và docs |
| **Nov 1-10** | Preparation Period (10 ngày) | ✅ Build bot, test deployment |
| **Nov 10** | Competition Bắt Đầu | ✅ Deploy bot với competition API keys |
| **Nov 10-24** | Trading Competition (2 tuần) | ✅ Monitor bot, 1 lần update được phép |
| **Nov 30** | Submission Deadline | ✅ Submit repo link và deck |
| **Dec 1-5** | Grand Finale | ✅ Tham dự (nếu top 10) |

---

## 📚 GIAI ĐOẠN 1: Chuẩn Bị (Trước Nov 1)

### ✅ Đọc và Hiểu Tài Liệu

- [ ] Đọc [Problem Statement](./PROBLEM_STATEMENT.md)
  - Hiểu rõ nhiệm vụ: Build autonomous trading bot
  - Hiểu rules và constraints
  - Nắm evaluation criteria

- [ ] Đọc [Evaluation Criteria](./EVALUATION_CRITERIA.md)
  - Hiểu công thức: Portfolio Return, Sortino (40%), Sharpe (30%), Calmar (30%)
  - Strategy optimization cho multiple metrics

- [ ] Đọc [Roostoo API Guide](./ROOSTOO_API_GUIDE.md)
  - Hiểu authentication (HMAC SHA256)
  - Nắm tất cả endpoints
  - Review Python examples

- [ ] Đọc [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)
  - Hiểu SSO login process
  - Nắm EC2 launch steps
  - Hiểu Session Manager và tmux

- [ ] Đọc [Horus API Guide](./HORUS_API_GUIDE.md) (Optional nhưng khuyến khích)
  - Hiểu cách integrate Horus data
  - Xem integration examples

### ✅ Setup Development Environment

- [ ] Cài đặt Python 3.7+
- [ ] Setup virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```
- [ ] Cài dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Clone/download [bot_template.py](./bot_template.py)
- [ ] Test Python environment hoạt động

### ✅ Tham Gia Cộng Đồng

- [ ] Join WhatsApp group: https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr
- [ ] Tham dự Online Info Session (Oct 29)
- [ ] Ghi chú các điểm quan trọng từ session

---

## 📦 GIAI ĐOẠN 2: Nhận Tài Nguyên (Oct 31)

### ✅ Kiểm Tra Email

- [ ] **Slide deck** và problem statement
- [ ] **Roostoo API guide** (chi tiết)
- [ ] **AWS Cloud guide** + email invitation cho team captain
- [ ] **Horus API documentation**
- [ ] **Test API keys** (Roostoo API key và secret - cho testing)

### ✅ Setup AWS Account

- [ ] Team captain nhận email invitation
- [ ] Sign in với SSO link (format: `https://<org-id>.awsapps.com/start`)
- [ ] Truy cập AWS Account → Management Console
- [ ] **QUAN TRỌNG:** Chọn region `us-east-1` (N. Virginia)
- [ ] Test kết nối thành công

### ✅ Test API Connections

- [ ] Test Roostoo API với test keys
  - [ ] Get server time
  - [ ] Get ticker
  - [ ] Get balance
  - [ ] Test signature generation
- [ ] (Optional) Test Horus API nếu có credentials
- [ ] Verify tất cả API calls thành công

---

## 🛠️ GIAI ĐOẠN 3: Development (Nov 1-10)

### ✅ Design Bot Architecture

- [ ] Quyết định strategy approach:
  - [ ] AI-driven (LLM, RL)
  - [ ] Traditional quantitative
  - [ ] Hybrid
- [ ] Design code structure
- [ ] Plan data sources (Roostoo + Horus?)
- [ ] Plan risk management

### ✅ Implement Core Functionality

- [ ] Customize [bot_template.py](./bot_template.py)
- [ ] Implement trading strategy logic
  - [ ] `should_buy()` method
  - [ ] `should_sell()` method
  - [ ] Position sizing logic
  - [ ] Risk management
- [ ] Integrate Roostoo API
  - [ ] All endpoints working
  - [ ] Error handling
  - [ ] Logging
- [ ] (Optional) Integrate Horus API
  - [ ] Get market data
  - [ ] Get signals/analytics
  - [ ] Combine với strategy

### ✅ Testing

- [ ] Test locally với test API keys
- [ ] Backtest strategy (nếu có historical data)
- [ ] Test error handling
- [ ] Test reconnection logic
- [ ] Verify logging hoạt động
- [ ] Test với different market conditions

### ✅ Deploy to AWS (Preparation)

- [ ] Follow [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)
- [ ] Launch EC2 instance:
  - [ ] Name: e.g., "my-trading-bot"
  - [ ] AMI: **Amazon Linux 2023**
  - [ ] Instance type: **t3.medium** (ONLY allowed)
  - [ ] Security group: **default**
  - [ ] **QUAN TRỌNG:** IAM instance profile: **HackathonInstanceRole**
- [ ] Connect via Session Manager
- [ ] Setup environment:
  - [ ] Update packages: `sudo dnf update -y`
  - [ ] Install dependencies: `sudo dnf install -y git python3-pip`
  - [ ] Clone code từ GitHub
  - [ ] Install Python dependencies: `pip install -r requirements.txt`
  - [ ] Configure API keys (environment variables hoặc config file)
- [ ] Install tmux: `sudo dnf install -y tmux`
- [ ] Test bot chạy trong tmux
- [ ] Verify bot chạy 24/7 (detach và reconnect)

---

## 🚀 GIAI ĐOẠN 4: Competition (Nov 10-24)

### ✅ Nhận Competition Keys (Nov 9)

- [ ] Nhận competition API key và secret
- [ ] Update bot với competition credentials
- [ ] Verify credentials hoạt động

### ✅ Deploy và Start (Nov 10)

- [ ] Update bot code với competition API keys
- [ ] Redeploy lên AWS EC2
- [ ] Start bot trong tmux session:
  ```bash
  tmux
  python3 bot.py
  # Detach: Ctrl+B, then D
  ```
- [ ] Verify bot đang chạy:
  - [ ] Check tmux: `tmux ls`
  - [ ] Reattach: `tmux attach`
  - [ ] Verify logs
- [ ] Monitor bot performance

### ✅ Monitor và Optimize (Nov 10-24)

- [ ] Monitor bot daily
  - [ ] Check bot vẫn chạy
  - [ ] Check logs cho errors
  - [ ] Monitor performance trên Roostoo leaderboard
- [ ] Track metrics:
  - [ ] Portfolio return
  - [ ] Sortino, Sharpe, Calmar ratios
  - [ ] Drawdown
- [ ] (Optional) One-time update allowed:
  - [ ] Improve strategy nếu cần
  - [ ] Fix bugs
  - [ ] Redeploy

### ✅ Monitor Performance

- [ ] Check Roostoo leaderboard:
  - [ ] iOS App: https://apps.apple.com/us/app/roostoo-mock-crypto-trading/id1483561353
  - [ ] Android App: https://play.google.com/store/apps/details?id=com.roostoo.roostoo
  - [ ] Webapp: app.roostoo.com
- [ ] Log tất cả trades internally
- [ ] Track API request success/failure

---

## 📝 GIAI ĐOẠN 5: Submission (Trước Nov 30)

### ✅ Prepare Repository

- [ ] Ensure code là **open-source**
- [ ] Clean code và comments
- [ ] Add README với instructions
- [ ] Document strategy và architecture
- [ ] Push to GitHub hoặc public repository
- [ ] Get repository link

### ✅ Prepare Presentation Deck (Nếu Top 10)

- [ ] Deck **≤12 slides**
- [ ] Include các phần:
  - [ ] Trading idea & strategy
  - [ ] Technical execution (architecture, algorithms)
  - [ ] Risk management & controls
  - [ ] Live Roostoo competition results
  - [ ] Backtest & validation results

### ✅ Submit (Nov 30)

- [ ] Submit repository link → hackathon@roostoo.com
- [ ] (Nếu top 10) Submit presentation deck → hackathon@roostoo.com
- [ ] Verify email sent successfully

---

## 🎤 GIAI ĐOẠN 6: Finale (Dec 1-5)

### ✅ Prepare for Presentation (Nếu Top 10)

- [ ] Practice 8-minute presentation
- [ ] Prepare for 4-minute Q&A
- [ ] Review deck
- [ ] Prepare answers cho potential questions
- [ ] Test presentation setup

### ✅ Attend Finale

- [ ] Check venue (HKU/HKUST)
- [ ] Attend demo presentations
- [ ] Network với fellow quants và sponsors
- [ ] Awards ceremony

---

## 🎯 Yêu Cầu và Rules - QUAN TRỌNG!

### ❌ Không Được:

- [ ] High-frequency trading (HFT)
- [ ] Market-making strategies
- [ ] Arbitrage strategies
- [ ] Leverage
- [ ] Short selling
- [ ] Manual trades (chỉ qua API)

### ✅ Phải:

- [ ] **Spot trading only**
- [ ] **Autonomous decisions** (không manual intervention)
- [ ] **Open-source code**
- [ ] **Deploy on AWS EC2**
- [ ] **Run 24/7** trong competition period
- [ ] **Log all trades** và API requests

### ⚠️ Constraints:

- [ ] Region: **us-east-1 only**
- [ ] Instance type: **t3.medium only**
- [ ] Connection: **Session Manager only** (SSH blocked)
- [ ] Storage: **50 GB limit**
- [ ] Instances: **1 instance only**
- [ ] Commission: **0.1% per order**

---

## 🏆 Mục Tiêu Chiến Thắng

### Optimize cho:

1. **Highest Return Award**
   - [ ] Focus vào absolute return
   - [ ] Balance risk vs return

2. **Best Composite Score Award**
   - [ ] Optimize Sortino Ratio (40% weight)
   - [ ] Optimize Sharpe Ratio (30% weight)
   - [ ] Optimize Calmar Ratio (30% weight)
   - [ ] Balance tất cả metrics

3. **Best Strategy/Technique Award**
   - [ ] Innovation trong approach
   - [ ] Technical execution quality
   - [ ] Clear presentation

**Lưu ý:** Có thể thắng nhiều awards!

---

## 📞 Hỗ Trợ

### Khi Cần Giúp:

- [ ] **WhatsApp Group:** https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr
- [ ] **Email:** hackathon@roostoo.com
- [ ] **API Support:** jolly@roostoo.com

### Tài Nguyên:

- [ ] **Roostoo API Docs:** https://github.com/roostoo/Roostoo-API-Documents
- [ ] **AWS Guide:** https://www.notion.so/Hackathon-Guide-How-to-Sign-In-and-Launch-Your-Bot-updated-29482203adbe80539adfdd37bcd68efb
- [ ] **Horus API:** horusdata.xyz

---

## 📊 Quick Reference

### Important Dates Summary

```
Oct 29  → Info Session
Oct 31  → Nhận email với API keys và docs
Nov 1-10 → Preparation: Build và test bot
Nov 10  → Competition bắt đầu (deploy bot!)
Nov 10-24 → Trading competition (monitor và optimize)
Nov 30  → Submit deadline
Dec 1-5 → Grand Finale (nếu top 10)
```

### Key Metrics

- **Portfolio Return** = (Final - Initial) / Initial
- **Composite Score** = 0.4×Sortino + 0.3×Sharpe + 0.3×Calmar
- **Commission Fee** = 0.1% per order

### Bot Requirements

- ✅ Autonomous (tự động hoàn toàn)
- ✅ 24/7 operation
- ✅ Spot trading only
- ✅ Open-source code
- ✅ AWS EC2 deployment
- ✅ Comprehensive logging

---

**Chúc bạn thành công! 🚀**

*In lại checklist này và check off từng item khi hoàn thành!*

