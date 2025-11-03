# Hướng Dẫn Triển Khai Bot Lên AWS EC2

## 📋 Mục Lục
1. [Đăng nhập với SSO](#1-đăng-nhập-với-sso)
2. [Chuyển đến EC2 trong us-east-1](#2-chuyển-đến-ec2-trong-us-east-1)
3. [Launch Instance (Các bước thủ công)](#3-launch-instance-các-bước-thủ-công)
4. [Kết nối với Instance (Session Manager)](#4-kết-nối-với-instance-session-manager)
5. [Setup Bot](#5-setup-bot)
6. [Chạy Bot 24/7 với tmux](#6-chạy-bot-247-với-tmux)
7. [Quản lý tmux Session](#7-quản-lý-tmux-session)
8. [Quy Tắc và Giới Hạn](#8-quy-tắc-và-giới-hạn)

---

## 1. Đăng nhập với SSO

### Bước 1: Mở link đăng nhập
- Mở link nhận được trong email
- Format: `https://<org-id>.awsapps.com/start`

### Bước 2: Nhập thông tin đăng nhập
- Nhập username/email
- Nhập password đã được cung cấp

### Bước 3: Truy cập AWS Account
- Sau khi đăng nhập, bạn sẽ thấy **AWS Access Portal**
- Click vào tile **"AWS Account"**

### Bước 4: Mở Management Console
- Click vào link **"Management Console"**
- Ví dụ: `Hackathon-TeamX` với `HackathonPermissionSet`
- AWS Console sẽ mở ra

---

## 2. Chuyển đến EC2 trong us-east-1

### ⚠️ QUAN TRỌNG: Toàn bộ hackathon chạy trong region N. Virginia (us-east-1)

### Bước 1: Kiểm tra Region
- Ở góc trên bên phải của AWS Console
- **PHẢI** đảm bảo region là **`us-east-1` (N. Virginia)**
- Nếu hiển thị region khác (ví dụ: "Ohio"), click vào và đổi sang **`us-east-1`**

### Bước 2: Mở EC2 Dashboard
- Trong search bar chính, gõ **"EC2"**
- Chọn EC2 từ kết quả tìm kiếm
- EC2 Dashboard sẽ mở ra

---

## 3. Launch Instance (Các bước thủ công)

### Bước 1: Bắt đầu Launch Instance
- Từ EC2 Dashboard, click vào nút **"Launch instance"** (màu cam lớn)

### Bước 2: Đặt tên
- **Name:** Đặt tên cho instance
- Ví dụ: `my-trading-bot`

### Bước 3: Chọn Application and OS Images (AMI)
- **PHẢI chọn:** **Amazon Linux**
- **PHẢI chọn cụ thể:** **Amazon Linux 2023 AMI**
  - AMI này đã bao gồm phần mềm kết nối cần thiết

### Bước 4: Chọn Instance type
- Click vào dropdown **"Instance type"**
- Gõ **"t3.medium"** vào ô search
- **CHỌN:** `t3.medium`
- ⚠️ **LƯU Ý:** `t3.medium` là instance type **DUY NHẤT** được phép sử dụng

### Bước 5: Key pair (login)
- Click vào dropdown **"Key pair"**
- Có thể tạo key pair mới hoặc không cần
- ⚠️ **Key pair KHÔNG CẦN THIẾT** vì sử dụng kết nối qua browser (Session Manager)

### Bước 6: Network settings
- Click nút **"Edit"** để xem chi tiết
- **Subnet:** Để nguyên "No preference (default subnet...)"
- **Firewall (security groups):**
  - Chọn **"Select existing security group"**
  - Từ danh sách, check vào security group tên **"default"**
  - ⚠️ **KHÔNG** tạo security group mới - group "default" đã đủ an toàn cho phương thức kết nối này

### Bước 7: Advanced details (BƯỚC QUAN TRỌNG!)
- Scroll xuống và mở rộng phần **"Advanced details"**
- Tìm field **"IAM instance profile"**
- Click dropdown và chọn **"HackathonInstanceRole"**
- ⚠️ **CẢNH BÁO:** Nếu bỏ qua bước này, bạn sẽ **KHÔNG THỂ** kết nối với instance!

### Bước 8: Launch
- Review **"Summary"** ở bên phải
- Kiểm tra:
  - ✅ `t3.medium` instance type
  - ✅ `Amazon Linux 2023` AMI
- Click nút **"Launch instance"**

---

## 4. Kết nối với Instance (Session Manager)

### ⚠️ QUAN TRỌNG: Session Manager là phương thức KẾT NỐI DUY NHẤT

- **SSH bị chặn** cho mục đích bảo mật
- **EC2 Instance Connect bị chặn**

### Các bước kết nối:

1. **Sau khi launch, click "View all instances"**
   - Đợi 1-2 phút để instance khởi động
   - Đợi **Status check** hiển thị **"2/2 checks passed"** hoặc **"3/3 checks passed"**

2. **Chọn instance**
   - Click checkbox bên cạnh tên instance

3. **Click nút "Connect"** ở đầu trang

4. **Chọn tab "Session Manager"**

5. **Click nút "Connect"** (màu cam)

6. **Kết quả:**
   - Tab trình duyệt mới sẽ mở ra
   - Màn hình terminal màu đen
   - Bạn đã kết nối an toàn với instance!

---

## 5. Setup Bot

### Bước 1: Kiểm tra quyền
- Bạn có quyền **`sudo`** (root) access
- Bạn đã ở trong instance terminal

### Bước 2: Di chuyển về home directory
```bash
cd ~
```
- Lệnh này đưa bạn về **home directory**
- Kiểm tra thư mục hiện tại: `pwd`

### Bước 3: Update packages và cài đặt dependencies

```bash
# Update và cài git, python, etc.
sudo dnf update -y

# Cài đặt git và python3-pip
sudo dnf install -y git python3-pip
```

**Lưu ý:**
- Cài đặt thêm bất kỳ dependencies nào bot cần
- Ví dụ: `nodejs`, `npm`, `docker`, etc.

### Bước 4: Clone code từ GitHub

```bash
# Clone repository của bạn
git clone <your-bot-repo>

# Di chuyển vào thư mục repository
cd <repo>

# Cài đặt Python dependencies
pip install -r requirements.txt
```

**Lưu ý:**
- Clone từ GitHub hoặc repository khác
- Cài đặt tất cả dependencies cần thiết
- Cấu hình bot (API keys, trading parameters, etc.) bằng:
  - Environment variables, hoặc
  - Config file

---

## 6. Chạy Bot 24/7 với tmux

### ⚠️ QUAN TRỌNG: Bot PHẢI chạy trong tmux session

- Nếu chạy bot và đóng browser, bot sẽ **DỪNG LẠI**
- **PHẢI** chạy bot trong `tmux` session để giữ nó chạy nền

### Step 1: Cài đặt tmux

```bash
sudo dnf install -y tmux
```

### Step 2: Khởi động tmux session mới

```bash
tmux
```

**Lưu ý:**
- Terminal session mới sẽ xuất hiện
- Trông gần giống terminal cũ, nhưng có **thanh màu xanh lá ở phía dưới**

### Step 3: Chạy bot trong tmux session

```bash
# Ví dụ với Python
python3 my_bot.py

# Hoặc với Node.js
node bot.js

# Hoặc với bất kỳ command nào khác
```

**Lưu ý:**
- Bot sẽ chạy trong tmux session này
- Bạn có thể thấy output của bot trong terminal này

---

## 7. Quản lý tmux Session

### Detach từ session (Rời khỏi nhưng giữ bot chạy)

**Thao tác:**
1. Nhấn `Ctrl + B`
2. **Thả ra** các phím
3. Nhấn `D` (cho detach)

**Kết quả:**
- Bạn quay về terminal chính
- Bot tiếp tục chạy an toàn trong background
- Có thể đóng browser tab

### Re-attach vào session (Kết nối lại sau)

**Khi cần kiểm tra bot:**
1. Kết nối lại qua Session Manager
2. Chạy lệnh:

```bash
# Kết nối lại session đang chạy
tmux attach

# Hoặc liệt kê các session hiện có
tmux ls
```

**Lưu ý:**
- `tmux ls` sẽ hiển thị tất cả sessions đang chạy
- `tmux attach` sẽ kết nối lại với session mặc định
- Sau khi attach, bạn sẽ thấy lại terminal của bot đang chạy

### Các lệnh tmux hữu ích khác

```bash
# Tạo session mới với tên
tmux new -s mybot

# Attach vào session có tên cụ thể
tmux attach -t mybot

# Liệt kê tất cả sessions
tmux ls

# Kill session
tmux kill-session -t mybot

# Kill tất cả sessions
tmux kill-server
```

---

## 8. Quy Tắc và Giới Hạn

### ⚠️ QUAN TRỌNG: Đọc kỹ các quy tắc!

**KHÔNG** cố gắng bypass các giới hạn này để đảm bảo công bằng và bảo mật.

### Region
- **CHỈ** sử dụng region **`us-east-1` (N. Virginia)**

### Instance Type
- **CHỈ** launch instance type **`t3.medium`**

### Connection Method
- **CHỈ** kết nối qua **Session Manager**
- SSH bị chặn
- EC2 Instance Connect bị chặn

### Storage
- Instance disk (EBS Volume) giới hạn **50 GB**

### Other AWS Services
- **KHÔNG THỂ** sử dụng các AWS services khác
- Ví dụ: IAM, S3, Lambda, etc.
- Permissions chỉ giới hạn cho:
  - Launch và quản lý EC2 instance
  - Deploy bots

### Instances
- **CHỈ LAUNCH 1 INSTANCE** trong EC2
- ⚠️ **CẢNH BÁO:** Tạo nhiều hơn 1 instance có thể tự động trigger termination
- Access chỉ được cấp để launch **một instance duy nhất**

---

## 📝 Checklist Triển Khai

### Trước khi Launch
- [ ] Đã đăng nhập qua SSO
- [ ] Đã chuyển sang region `us-east-1`
- [ ] Đã mở EC2 Dashboard

### Trong quá trình Launch
- [ ] Đã đặt tên instance
- [ ] Đã chọn **Amazon Linux 2023 AMI**
- [ ] Đã chọn **t3.medium** instance type
- [ ] Đã chọn security group **"default"**
- [ ] ✅ **ĐÃ CHỌN IAM instance profile: "HackathonInstanceRole"** (QUAN TRỌNG!)

### Sau khi Launch
- [ ] Đã đợi Status check: 2/2 hoặc 3/3 passed
- [ ] Đã kết nối qua Session Manager
- [ ] Đã update packages và cài dependencies
- [ ] Đã clone code repository
- [ ] Đã cài đặt bot dependencies (requirements.txt, etc.)
- [ ] Đã cấu hình API keys và parameters
- [ ] Đã cài đặt tmux
- [ ] Đã tạo tmux session
- [ ] Đã chạy bot trong tmux
- [ ] Đã detach từ tmux session
- [ ] Bot đang chạy trong background

---

## 🔧 Troubleshooting

### Không thể kết nối với instance
- ✅ Kiểm tra đã chọn **"HackathonInstanceRole"** trong Advanced details chưa?
- ✅ Kiểm tra Status check đã pass chưa (đợi 1-2 phút)?
- ✅ Đảm bảo đang dùng **Session Manager**, không phải SSH

### Bot dừng khi đóng browser
- ✅ Đảm bảo bot đang chạy trong **tmux session**
- ✅ Đảm bảo đã **detach** từ tmux (Ctrl+B, D) trước khi đóng browser

### Không tìm thấy region us-east-1
- ✅ Kiểm tra góc trên bên phải AWS Console
- ✅ Click vào region hiện tại và chọn **N. Virginia (us-east-1)**

### Instance bị terminate
- ✅ Kiểm tra có launch nhiều hơn 1 instance không
- ✅ Chỉ được phép 1 instance duy nhất

---

## 📚 Tài Nguyên Tham Khảo

- **Roostoo API Docs:** https://github.com/roostoo/Roostoo-API-Documents
- **AWS Session Manager Docs:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html
- **tmux Cheat Sheet:** https://tmuxcheatsheet.com/
- **Amazon Linux 2023 Docs:** https://docs.aws.amazon.com/linux/al2023/

---

*Hướng dẫn này dựa trên AWS Deployment Guide từ HK Quant Trading Hackathon*

