# Phân Tích Chi Tiết: HK Quant Trading Hackathon

## 📋 Tổng Quan

**Tên sự kiện:** Hong-Kong Universities Web3 Quant Trading Hackathon

### Đối tượng tham gia
- Sinh viên từ 3 trường đại học hàng đầu Hong Kong:
  - HKU (The University of Hong Kong)
  - HKUST (The Hong Kong University of Science and Technology)
  - CUHK (The Chinese University of Hong Kong)

### Thời gian
- **Giai đoạn hình thành đội:** 10 tháng 10 - 31 tháng 10
- **Giai đoạn thi đấu:** 1 tháng 11 - 30 tháng 11
- **Sự kiện cuối và trình bày:** Tuần đầu tháng 12

---

## 🎯 Mục Tiêu Hackathon

### 1. Tạo cộng đồng học tập năng động
- Kết nối tài năng kỹ thuật và sinh viên định lượng tại Hong Kong

### 2. Kết nối với ngành công nghiệp
- Liên kết sinh viên hàng đầu với các nhà lãnh đạo ngành
- Phát triển giải pháp giao dịch thuật toán và AI cấp công nghiệp trong Web3

### 3. Trải nghiệm ý nghĩa và thú vị
- Môi trường học hỏi và cạnh tranh lành mạnh

---

## 🚀 Vấn Đề Cần Giải Quyết (Problem Statement)

### Nhiệm vụ chính
**Xây dựng một trading bot hoặc AI trading agent hoạt động live, dựa trên dữ liệu, cạnh tranh trên trình giả lập giao dịch real-time của Roostoo.**

### Yêu cầu kỹ thuật
1. **Tự động đưa ra quyết định mua, giữ và bán** mà không cần can thiệp thủ công từ con người
2. **Tương tác với Roostoo mock exchange APIs:**
   - Sử dụng **GET requests** để lấy dữ liệu portfolio
   - Sử dụng **POST requests** để thực hiện giao dịch

### Chiến lược
- Chiến lược mở (open-ended), không giới hạn cách tiếp cận
- Quan trọng nhất: bot phải tự động hoàn toàn

---

## 📜 Quy Tắc và Ràng Buộc

### 1. ❌ Các chiến lược bị cấm
- **Không được sử dụng:**
  - High-frequency trading (Giao dịch tần suất cao)
  - Market-making (Tạo thanh khoản)
  - Arbitraging strategy (Chiến lược arbitrage)

### 2. ⚠️ Giới hạn giao dịch
- **Chỉ được phép:** Spot trading (Giao dịch giao ngay)
- **Không được phép:**
  - Leverage (Đòn bẩy)
  - Shorting (Bán khống)

### 3. 📂 Yêu cầu mã nguồn
- Phải submit repository dưới dạng **open-source** để xác thực code
- Điều này đảm bảo tính minh bạch và công bằng

### 4. ☁️ Hạ tầng cloud
- Mỗi đội sẽ nhận được một AWS sub-account
- Phải launch EC2 instance để host bot trên cloud
- Bot phải chạy tự động trên remote servers, không phải local machine

### 5. 📊 Nguồn dữ liệu
- **Khuyến khích sử dụng:** Horus data source
- **Cho phép:** Sử dụng bất kỳ nguồn dữ liệu nào có sẵn

---

## 📅 Timeline Chi Tiết

### Giai đoạn chuẩn bị
- **29 tháng 10:** Online Info Session + Workshop

### Giai đoạn thi đấu
- **1 - 10 tháng 11:** Bắt đầu! Xây dựng bot và test deployment trên Roostoo
- **10 - 24 tháng 11:** Trading Competition bắt đầu
  - Trong 2 tuần này, được phép **một lần cập nhật và redeploy** để cải thiện strategy và code (optional)

### Giai đoạn cuối
- **1 tháng 12:** Final Submission Deadline
  - Submit: Decks & Code Repos
- **1 - 5 tháng 12:** Grand Finale @ HKU / HKUST
  - Demo Presentation với Judges từ ngành công nghiệp
  - Trao giải thưởng

---

## 📦 Logistics - Những gì bạn nhận được

### 31 tháng 10 (Thứ 6)
Mỗi đội sẽ nhận email chứa:
1. Slide deck hiện tại và problem statement
2. **Roostoo API guide**
3. **AWS Cloud guide** + Email invitation cho team captain để set up
4. **Horus API documentation**
5. **Một set Roostoo API key và API secret** (dùng cho testing portfolio chung)

### 9 tháng 11 (Chủ nhật)
- **Competition API key và API secret** riêng cho mỗi đội

### Kênh thông tin
- Email announcements
- WhatsApp group cho technical support
- Link WhatsApp: `https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr`

---

## ✅ Logistics - Những gì ban tổ chức kỳ vọng từ bạn

### 10 tháng 11 (Thứ 2)
- **Deploy bot vào competition và để nó tự động cạnh tranh!**

### 30 tháng 11 (Chủ nhật)
- Submit:
  - **Repo link** (để nhận certificate)
  - **Deck** (nếu bạn là top 10)
- Gửi đến: `hackathon@roostoo.com`

### 1-5 tháng 12 (TBA)
- Tham dự finale và networking
- Gặp gỡ fellow quants và sponsors

---

## 🏆 Giải Thưởng

### Phân loại giải thưởng (3 hạng mục)

#### (A) Highest Return
- Giải nhất: **HKD $3,000**
- Giải nhì: **HKD $2,000**
- Giải ba: **HKD $1,000**

#### (B) Best Composite Score
- Tính theo weighted average:
  - 0.4x Sortino Ratio
  - 0.3x Sharpe Ratio
  - 0.3x Calmar Ratio
- Giải nhất: **HKD $3,000**
- Giải nhì: **HKD $2,000**
- Giải ba: **HKD $1,000**

#### (C) Best Strategy/Technique
- Giải nhất: **HKD $3,000**
- Giải nhì: **HKD $2,000**
- Giải ba: **HKD $1,000**

### Tổng giải thưởng
- **Tổng giải thưởng:** $18,000 HKD
- **Cơ hội:** Một đội có thể thắng nhiều hạng mục!

### Cơ hội nghề nghiệp

#### Flow Traders
- Winning team members được offer:
  - Free assessment shot
  - Cơ hội tham gia in-house poker tournament với Flow Traders' Traders (tháng 12)

#### Resume sharing
- Resumes của participants sẽ được chia sẻ với:
  - Flow Traders
  - Jane Street
  - Kwan

### Lợi ích khác

#### Bot của riêng bạn
- Tạo bot có giá trị thực tế
- Khả năng tạo thêm bots trong tương lai
- Roostoo cung cấp platform để tiếp tục live-testing
- Có thể kết nối với industry resources

#### Cộng đồng và networking
- Gặp gỡ potential cofounders và business partners
- Networking platform cho top talents từ 3 trường đại học hàng đầu HK

---

## 🎤 Finalist Presentation

### Điều kiện
- **Top 10 teams** từ Roostoo leaderboard (dựa trên pure portfolio return)

### Format
- **8 phút** trình bày
- **4 phút** Q&A

### Yêu cầu presentation deck
- **≤12 slides**
- Phải bao gồm:
  1. Trading idea & strategy
  2. Technical execution (architecture, algorithms)
  3. Risk management & controls
  4. Live Roostoo competition results
  5. Backtest & validation results

### Ban giám khảo
- Industry professionals
- Professors

---

## 🛠️ Tài Nguyên Kỹ Thuật

### 1. Roostoo API Documentation
- **Link:** `https://github.com/roostoo/Roostoo-API-Documents`
- **Mục đích:** Tương tác với Roostoo backend exchange trading engine qua POST và GET API requests

### 2. Deploy on AWS Guide
- **Link:** `https://www.notion.so/Hackathon-Guide-How-to-Sign-In-and-Launch-Your-Bot-updated-29482203adbe80539adfdd37bcd68efb`
- **Mục đích:** Deploy bot trên cloud infrastructure để đảm bảo chạy tự động trên remote servers

### 3. Horus API Documentation
- Nguồn dữ liệu được khuyến khích sử dụng

---

## 🏢 Nhà Tài Trợ và Đối Tác

### Gold Sponsor
- **Flow Traders**
  - Global proprietary trading firm
  - Leading market maker
  - Publicly listed on Euronext Amsterdam

### Silver Sponsor
- **Jane Street**
  - Global leading quantitative trading firm
  - Known for deep mathematical expertise
  - Cutting-edge algorithmic trading

### Platform Partner
- **Roostoo**
  - Cloud-hosted exchange backend platform
  - Enables algorithmic bots to trade and compete
  - Real-time, simulated environment

### Academic Partners
- TRADERS @ HKUQRS
- DAFTES
- CUHK Quant Trading Society

---

## 📊 Phân Tích và Chiến Lược

### Điểm quan trọng cho việc phát triển bot

1. **Tự động hóa hoàn toàn**
   - Bot phải chạy 24/7 không cần giám sát
   - Tất cả quyết định phải được thực hiện tự động

2. **Tuân thủ quy tắc**
   - Tránh HFT, market-making, arbitrage
   - Chỉ spot trading, không leverage/shorting

3. **Quản lý rủi ro**
   - Implement risk management & controls
   - Đây là tiêu chí đánh giá trong final presentation

4. **Validation**
   - Cần có backtest & validation results
   - So sánh với live competition results

5. **Technical architecture**
   - Clean code (sẽ được review vì open-source)
   - Scalable và maintainable
   - Documented rõ ràng

### Gợi ý chiến lược

#### Focus areas:
1. **Data-driven decisions**
   - Sử dụng Horus API hoặc data sources khác
   - Technical analysis indicators
   - Sentiment analysis (nếu có)

2. **Risk management**
   - Position sizing
   - Stop-loss mechanisms
   - Portfolio diversification
   - Drawdown controls

3. **Performance metrics**
   - Ngoài return, cần optimize:
     - Sortino Ratio
     - Sharpe Ratio
     - Calmar Ratio

4. **Technical execution**
   - Robust error handling
   - API rate limiting
   - Connection stability
   - Logging và monitoring

---

## 📝 Checklist Trước Khi Bắt Đầu

### Chuẩn bị (Trước 31/10)
- [ ] Đọc kỹ problem statement
- [ ] Review Roostoo API docs
- [ ] Review AWS deployment guide
- [ ] Review Horus API docs
- [ ] Setup development environment
- [ ] Tham gia WhatsApp group cho support

### Development Phase (1-10/11)
- [ ] Design bot architecture
- [ ] Implement trading strategy
- [ ] Integrate với Roostoo API
- [ ] Test trên test API keys
- [ ] Deploy trên AWS EC2
- [ ] Monitor và debug

### Competition Phase (10-24/11)
- [ ] Deploy với competition API keys
- [ ] Monitor bot performance
- [ ] Cải thiện strategy (1 lần update được phép)
- [ ] Optimize cho các metrics khác nhau

### Submission Phase (Trước 1/12)
- [ ] Finalize code và documentation
- [ ] Prepare presentation deck (≤12 slides)
- [ ] Submit repo link và deck (nếu top 10)
- [ ] Prepare cho final presentation

---

## 🎯 Mục Tiêu Chiến Thắng

Để tối đa hóa cơ hội thắng:

1. **Highest Return:** Focus vào return cao nhưng phải kiểm soát rủi ro
2. **Best Composite Score:** Balance giữa return và risk-adjusted metrics (Sortino, Sharpe, Calmar)
3. **Best Strategy/Technique:** Innovation trong approach và execution

**Lưu ý:** Có thể thắng nhiều hạng mục, vì vậy hãy thiết kế strategy để optimize cho nhiều metrics cùng lúc!

---

## 📞 Liên Hệ

- **Email:** hackathon@roostoo.com
- **WhatsApp Support Group:** https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr

---

*Tài liệu này được tạo dựa trên thông tin từ HK Quant Trading Hackathon Info Session Presentation*

