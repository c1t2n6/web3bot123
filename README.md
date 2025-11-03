# HK Quant Trading Hackathon - Project Documentation

## 📚 Tài Liệu

### 1. [Hackathon Analysis](./HACKATHON_ANALYSIS.md)
Tổng quan về hackathon, timeline, prizes, và requirements.

### 2. [Problem Statement](./PROBLEM_STATEMENT.md)
Chi tiết về nhiệm vụ, requirements, và evaluation criteria.

### 3. [Evaluation Criteria](./EVALUATION_CRITERIA.md)
Công thức tính toán và strategy optimization cho:
- Portfolio Return
- Sortino Ratio (0.4x weight)
- Sharpe Ratio (0.3x weight)
- Calmar Ratio (0.3x weight)

### 4. [Roostoo API Guide](./ROOSTOO_API_GUIDE.md)
Hướng dẫn chi tiết về Roostoo API:
- Authentication & Security
- All API endpoints
- Python implementation examples
- Error handling best practices

### 5. [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)
Hướng dẫn deploy bot lên AWS EC2:
- SSO login
- Launch instance
- Session Manager connection
- tmux setup for 24/7 operation

## 🚀 Quick Start

### 1. Đọc tài liệu
- Bắt đầu với [Problem Statement](./PROBLEM_STATEMENT.md)
- Review [Roostoo API Guide](./ROOSTOO_API_GUIDE.md)
- Chuẩn bị [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)

### 2. Setup Development
```bash
# Clone repository (nếu có)
git clone <your-repo>

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install requests
```

### 3. Test API Connection
```python
# Use examples from ROOSTOO_API_GUIDE.md
# Test with provided test API keys
```

### 4. Develop Strategy
- Implement trading logic
- Test locally
- Backtest strategy

### 5. Deploy to AWS
- Follow [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)
- Deploy bot using competition API keys

## 📅 Important Dates

- **Oct 29:** Online Info Session & Workshop
- **Nov 1-10:** Preparation Period
- **Nov 10-24:** Trading Competition
- **Dec 1:** Final Submission Deadline
- **Dec 1-5:** Grand Finale

## 🔗 Resources

- **Roostoo API Docs:** https://github.com/roostoo/Roostoo-API-Documents
- **WhatsApp Support:** https://chat.whatsapp.com/D1YyBcfgzzd6duLsnuHEGr
- **Horus API:** horusdata.xyz
- **AWS Guide:** https://www.notion.so/Hackathon-Guide-How-to-Sign-In-and-Launch-Your-Bot-updated-29482203adbe80539adfdd37bcd68efb

## 🏆 Awards

- **Highest Return:** $3,000 / $2,000 / $1,000 HKD
- **Best Composite Score:** $3,000 / $2,000 / $1,000 HKD
- **Best Strategy/Technique:** $3,000 / $2,000 / $1,000 HKD

**Total Prize Pool:** $18,000 HKD

## 📞 Contact

- **Email:** hackathon@roostoo.com
- **API Support:** jolly@roostoo.com

---

*Good luck with the hackathon! 🚀*

