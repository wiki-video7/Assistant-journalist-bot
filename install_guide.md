# 🚀 راهنمای نصب ربات Assistant Journalist Bot

## 📋 پیش‌نیازهای سیستم

### 🐍 Python
```bash
# نصب Python 3.9+
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv

# macOS (با Homebrew):
brew install python@3.9

# Windows: 
# دانلود از https://python.org
```

### 🔧 ابزارهای سیستم

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y \
    ffmpeg \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    libsndfile1-dev \
    libavcodec-extra \
    libavformat-dev \
    libavdevice-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libopencv-dev \
    build-essential \
    python3-dev \
    pkg-config \
    cmake \
    git
```

#### macOS:
```bash
# نصب Homebrew اگر نصب نیست
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب پیش‌نیازها
brew install \
    ffmpeg \
    portaudio \
    libsndfile \
    jpeg \
    libpng \
    libtiff \
    opencv \
    cmake \
    pkg-config \
    git
```

#### Windows:
```powershell
# نصب Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# نصب پیش‌نیازها
choco install ffmpeg git python3
```

## 📦 نصب پروژه

### 1. دانلود پروژه
```bash
# کلون کردن از GitHub
git clone https://github.com/your-username/assistant-journalist-bot.git
cd assistant-journalist-bot

# یا دانلود و استخراج ZIP
```

### 2. ایجاد محیط مجازی
```bash
# ایجاد virtual environment
python3 -m venv venv

# فعال‌سازی
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. نصب کتابخانه‌های Python
```bash
# نصب requirements اصلی
pip install -r requirements.txt

# نصب PyTorch (اختیاری - برای GPU)
# CPU only:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# CUDA (GPU):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 4. نصب مدل‌های زبانی
```bash
# نصب مدل spaCy برای انگلیسی
python -m spacy download en_core_web_sm

# دانلود مدل Whisper (اختیاری)
# این مدل‌ها در اولین استفاده دانلود می‌شوند
```

## 🔑 تنظیم API Keys

### 1. ایجاد فایل .env
```bash
# کپی کردن فایل نمونه
cp .env.example .env

# ویرایش فایل
nano .env
```

### 2. تکمیل اطلاعات API
```env
# Bot Configuration - اجباری
BOT_TOKEN=your_telegram_bot_token_here
BOT_USERNAME=your_bot_username

# AI APIs - حداقل یکی اجباری
OPENAI_API_KEY=sk-proj-your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here

# News API - اختیاری
NEWS_API_KEY=your_news_api_key_here

# Database - اختیاری
DATABASE_URL=sqlite:///bot.db
```

### 3. دریافت API Keys

#### 🤖 Telegram Bot Token:
1. به [@BotFather](https://t.me/BotFather) در تلگرام مراجعه کنید
2. `/newbot` را ارسال کنید
3. نام و username ربات را انتخاب کنید
4. Token دریافتی را در `.env` قرار دهید

#### 🧠 OpenAI API:
1. به [platform.openai.com](https://platform.openai.com) بروید
2. حساب کاربری ایجاد کنید
3. به بخش API Keys بروید
4. کلید جدید ایجاد کنید

#### 🔮 Google Gemini API:
1. به [ai.google.dev](https://ai.google.dev) بروید
2. Get API Key را کلیک کنید
3. کلید دریافتی را کپی کنید

## 🧪 تست نصب

### 1. بررسی سلامت سیستم
```bash
python main.py --health
```

خروجی موفق:
```
🔍 بررسی سلامت سیستم...
   ✅ Python Version
   ✅ Config File
   ✅ Project Structure
```

### 2. اجرای آزمایشی
```bash
python main.py
```

اگر همه چیز درست باشد، باید این پیام را ببینید:
```
╔══════════════════════════════════════════════════╗
║            🤖 Assistant Journalist Bot            ║
║        ربات هوشمند دستیار خبرنگار                ║
╚══════════════════════════════════════════════════╝

✅ تمام پیش‌نیازها برآورده شده‌اند
🚀 شروع ربات...
ربات آماده است!
```

## 🛠️ رفع مشکلات رایج

### ❌ خطای "ModuleNotFoundError"
```bash
# مطمئن شوید virtual environment فعال است
source venv/bin/activate

# نصب مجدد requirements
pip install -r requirements.txt
```

### ❌ خطای "FFmpeg not found"
```bash
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
choco install ffmpeg

# تست:
ffmpeg -version
```

### ❌ خطای "PortAudio"
```bash
# Ubuntu/Debian:
sudo apt install portaudio19-dev python3-pyaudio

# macOS:
brew install portaudio
pip install pyaudio

# Windows:
pip install pipwin
pipwin install pyaudio
```

### ❌ خطای "OpenCV"
```bash
# حذف نسخه قدیمی
pip uninstall opencv-python opencv-python-headless

# نصب مجدد
pip install opencv-python-headless
```

### ❌ خطای "API Key"
- مطمئن شوید `.env` در مسیر اصلی پروژه است
- کلیدهای API را بدون فاصله کپی کنید
- از نقل قول استفاده نکنید

### ❌ خطای "Permission Denied"
```bash
# Linux/macOS:
chmod +x main.py

# اجرا با python
python main.py
```

## 🚀 راه‌اندازی Production

### 1. استفاده از PM2
```bash
# نصب PM2
npm install -g pm2

# ایجاد فایل ecosystem
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'journalist-bot',
    script: 'main.py',
    interpreter: 'python3',
    cwd: '/path/to/your/bot',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
}
EOF

# اجرا
pm2 start ecosystem.config.js
```

### 2. استفاده از Docker
```dockerfile
# Dockerfile موجود در پروژه
docker build -t journalist-bot .
docker run -d --name bot --env-file .env journalist-bot
```

### 3. استفاده از systemd
```bash
# ایجاد service file
sudo nano /etc/systemd/system/journalist-bot.service

# محتوا:
[Unit]
Description=Assistant Journalist Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/bot
Environment=PATH=/path/to/bot/venv/bin
ExecStart=/path/to/bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target

# فعال‌سازی
sudo systemctl daemon-reload
sudo systemctl enable journalist-bot
sudo systemctl start journalist-bot
```

## 📊 مانیتورینگ

### لاگ‌ها
```bash
# مشاهده لاگ‌های زنده
tail -f logs/bot.log

# جستجو در لاگ‌ها
grep "ERROR" logs/bot.log
```

### وضعیت سیستم
```bash
# بررسی وضعیت
python main.py --health

# نمایش نسخه
python main.py --version
```

## 🔄 به‌روزرسانی

```bash
# دریافت آخرین تغییرات
git pull origin main

# نصب dependencies جدید
pip install -r requirements.txt

# راه‌اندازی مجدد
pm2 restart journalist-bot
```

## 🆘 پشتیبانی

اگر با مشکلی مواجه شدید:

1. **مستندات:** README.md را مطالعه کنید
2. **لاگ‌ها:** فایل `logs/bot.log` را بررسی کنید
3. **تست:** `python main.py --health` را اجرا کنید
4. **Issues:** در GitHub issue جدید ایجاد کنید

---

## ✅ چک‌لیست نصب کامل

- [ ] Python 3.9+ نصب شده
- [ ] FFmpeg نصب شده
- [ ] Virtual environment ایجاد شده
- [ ] Requirements نصب شده
- [ ] فایل .env تنظیم شده
- [ ] API Keys معتبر
- [ ] Health check موفق
- [ ] ربات اجرا می‌شود
- [ ] پیام تست ارسال شده

🎉 **تبریک! ربات شما آماده استفاده است.**