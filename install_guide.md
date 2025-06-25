# 🚀 راهنمای کامل نصب Assistant Journalist Bot

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/نصب-آسان-success.svg?style=for-the-badge)

**راهنمای گام به گام برای کاربران مبتدی و حرفه‌ای** 

⏱️ زمان تقریبی نصب: **15-30 دقیقه**

</div>

---

## 📋 فهرست مطالب

- [🎯 نکات مهم قبل از شروع](#-نکات-مهم-قبل-از-شروع)
- [💻 پیش‌نیازهای سیستم](#-پیش‌نیازهای-سیستم)
- [🔧 نصب پیش‌نیازها](#-نصب-پیش‌نیازها)
- [📦 دانلود و نصب ربات](#-دانلود-و-نصب-ربات)
- [🔑 تنظیم API Keys](#-تنظیم-api-keys)
- [⚙️ پیکربندی ربات](#️-پیکربندی-ربات)
- [🧪 تست و راه‌اندازی](#-تست-و-راه‌اندازی)
- [🐳 نصب با Docker](#-نصب-با-docker)
- [🚀 تولید (Production)](#-تولید-production)
- [❌ عیب‌یابی](#-عیب‌یابی)
- [🆘 کمک و پشتیبانی](#-کمک-و-پشتیبانی)

---

## 🎯 نکات مهم قبل از شروع

### ✅ چک‌لیست آمادگی
- [ ] دسترسی به اینترنت پایدار
- [ ] حداقل 30 دقیقه وقت آزاد
- [ ] دسترسی مدیریت سیستم (Admin/Sudo)
- [ ] آماده بودن API Keys (تلگرام، OpenAI یا Gemini)

### ⚠️ هشدارهای مهم
- **هرگز API Keys خود را با دیگران به اشتراک نگذارید**
- لطفاً دستورات را دقیقاً کپی کنید
- در صورت بروز خطا، عجله نکنید و لاگ‌ها را بخوانید
- برای محیط تولید حتماً از HTTPS استفاده کنید

---

## 💻 پیش‌نیازهای سیستم

### 🔧 حداقل سیستم مورد نیاز

| جزء | حداقل | توصیه شده |
|-----|--------|-----------|
| **RAM** | 2GB | 4GB+ |
| **فضای دیسک** | 3GB | 10GB+ |
| **CPU** | 1 Core | 2+ Cores |
| **اتصال اینترنت** | 1 Mbps | 10+ Mbps |

### 🖥️ سیستم‌عامل‌های پشتیبانی شده

✅ **کاملاً پشتیبانی:**
- Ubuntu 20.04+ / Debian 11+
- CentOS 8+ / RHEL 8+
- macOS 11+ (Big Sur)
- Windows 10+ / Windows Server 2019+

⚠️ **پشتیبانی محدود:**
- سایر توزیع‌های Linux
- macOS 10.15 (Catalina)

---

## 🔧 نصب پیش‌نیازها

### 🐍 Python 3.9+

#### 🪟 Windows
```powershell
# روش 1: دانلود از سایت رسمی (توصیه شده)
# برو به https://python.org/downloads
# دانلود Python 3.11.x
# حین نصب، گزینه "Add Python to PATH" را فعال کن

# روش 2: با Chocolatey
# ابتدا Chocolatey را نصب کن از https://chocolatey.org/install
choco install python --version=3.11.7

# تأیید نصب
python --version
# باید نمایش دهد: Python 3.11.x
```

#### 🍎 macOS
```bash
# روش 1: با Homebrew (توصیه شده)
# ابتدا Homebrew را نصب کن
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب Python
brew install python@3.11

# تأیید نصب
python3 --version

# روش 2: دانلود از python.org
# برو به https://python.org/downloads و نسخه macOS را دانلود کن
```

#### 🐧 Ubuntu/Debian
```bash
# به‌روزرسانی سیستم
sudo apt update && sudo apt upgrade -y

# نصب Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-pip python3.11-dev

# تنظیم Python پیش‌فرض (اختیاری)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# تأیید نصب
python3.11 --version
```

#### 🔴 CentOS/RHEL/Fedora
```bash
# CentOS 8+/RHEL 8+
sudo dnf update -y
sudo dnf install -y python3.11 python3.11-pip python3.11-devel

# Fedora
sudo dnf install -y python3 python3-pip python3-devel

# تأیید نصب
python3 --version
```

### 🎬 FFmpeg (ضروری برای پردازش رسانه)

#### 🪟 Windows
```powershell
# روش 1: با Chocolatey (آسان‌ترین)
choco install ffmpeg

# روش 2: دانلود دستی
# 1. برو به https://ffmpeg.org/download.html#build-windows
# 2. دانلود نسخه "release builds"
# 3. فایل ZIP را استخراج کن
# 4. پوشه bin را به PATH اضافه کن

# تست نصب
ffmpeg -version
```

#### 🍎 macOS
```bash
# با Homebrew
brew install ffmpeg

# تست نصب
ffmpeg -version
```

#### 🐧 Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y ffmpeg

# تست نصب
ffmpeg -version
```

#### 🔴 CentOS/RHEL/Fedora
```bash
# فعال‌سازی مخزن EPEL (برای CentOS/RHEL)
sudo dnf install -y epel-release

# نصب FFmpeg
sudo dnf install -y ffmpeg

# تست نصب
ffmpeg -version
```

### 🔊 کتابخانه‌های صوتی (اختیاری - برای پردازش صدا)

#### 🐧 Ubuntu/Debian
```bash
sudo apt install -y \
    portaudio19-dev \
    python3-pyaudio \
    libasound2-dev \
    libsndfile1-dev \
    libavcodec-extra \
    libavformat-dev \
    libavdevice-dev
```

#### 🍎 macOS
```bash
brew install portaudio libsndfile
```

#### 🪟 Windows
```powershell
# معمولاً نیازی به نصب جداگانه نیست
# در صورت بروز مشکل:
pip install pipwin
pipwin install pyaudio
```

### 🖼️ کتابخانه‌های پردازش تصویر (اختیاری)

#### 🐧 Ubuntu/Debian
```bash
sudo apt install -y \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libopencv-dev \
    python3-opencv
```

#### 🍎 macOS
```bash
brew install jpeg libpng libtiff opencv
```

---

## 📦 دانلود و نصب ربات

### 📥 روش 1: دانلود با Git (توصیه شده)

```bash
# 1. نصب Git (اگر نصب نیست)
# Ubuntu/Debian:
sudo apt install -y git

# CentOS/RHEL/Fedora:
sudo dnf install -y git

# macOS:
brew install git

# Windows: دانلود از https://git-scm.com

# 2. کلون کردن پروژه
git clone https://github.com/your-username/assistant-journalist-bot.git
cd assistant-journalist-bot

# 3. بررسی محتویات
ls -la
# باید فایل‌هایی مانند main.py، requirements.txt و ... ببینید
```

### 📥 روش 2: دانلود ZIP

```bash
# 1. دانلود فایل ZIP از GitHub
# برو به: https://github.com/your-username/assistant-journalist-bot
# کلیک روی "Code" > "Download ZIP"

# 2. استخراج فایل
# Windows: راست کلیک > "Extract All"
# macOS: دابل کلیک روی ZIP
# Linux:
unzip assistant-journalist-bot-main.zip
cd assistant-journalist-bot-main
```

### 🔧 ایجاد محیط مجازی Python

```bash
# 1. ایجاد محیط مجازی
python3 -m venv venv

# یا در Windows:
python -m venv venv

# 2. فعال‌سازی محیط مجازی
# Linux/macOS:
source venv/bin/activate

# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# ✅ اگر موفق باشد، پرامپت شما باید شروع شود با (venv)
```

### 📚 نصب کتابخانه‌های Python

```bash
# مطمئن شوید محیط مجازی فعال است (باید (venv) در ابتدای خط باشد)

# 1. به‌روزرسانی pip
python -m pip install --upgrade pip

# 2. نصب کتابخانه‌های اصلی
pip install -r requirements.txt

# 3. در صورت بروز خطا، نصب تک به تک:
pip install python-telegram-bot==21.0.1
pip install python-dotenv==1.0.1
pip install openai==1.51.2
pip install google-generativeai==0.8.3
pip install requests==2.32.3
pip install aiofiles==24.1.0

# 4. تأیید نصب
pip list
```

### 🔍 تست نصب اولیه

```bash
# بررسی سلامت پروژه
python main.py --version

# خروجی موردانتظار:
# Assistant Journalist Bot v1.0.0

# بررسی ساختار فایل‌ها
python main.py --health

# اگر خطایی نداشت، آماده تنظیم API Keys هستید
```

---

## 🔑 تنظیم API Keys

### 📋 لیست API Keys مورد نیاز

| API | وضعیت | هزینه | لینک دریافت |
|-----|--------|-------|-------------|
| **Telegram Bot** | ⚠️ ضروری | رایگان | [@BotFather](https://t.me/BotFather) |
| **OpenAI** | ⚠️ یکی ضروری | پولی ($5 کردیت) | [platform.openai.com](https://platform.openai.com) |
| **Google Gemini** | ⚠️ یکی ضروری | رایگان/پولی | [ai.google.dev](https://ai.google.dev) |
| **News API** | ✅ اختیاری | رایگان/پولی | [newsapi.org](https://newsapi.org) |

### 🤖 دریافت Telegram Bot Token

#### گام 1: ایجاد ربات
```bash
# 1. در تلگرام، به @BotFather برو
# 2. دستور /start را ارسال کن
# 3. دستور /newbot را ارسال کن
# 4. نام ربات را وارد کن (مثل: دستیار خبرنگار من)
# 5. Username ربات را وارد کن (باید به bot ختم شود، مثل: my_journalist_bot)
```

#### گام 2: کپی کردن Token
```bash
# BotFather توکنی شبیه این میده:
# 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

# ⚠️ این توکن را کپی کن و جایی امن نگهدار
```

#### گام 3: تنظیمات اختیاری ربات
```bash
# در BotFather:
/setdescription - توضیح ربات
/setabouttext - درباره ربات  
/setuserpic - عکس پروفایل ربات
/setcommands - دستورات ربات
```

### 🧠 دریافت OpenAI API Key

#### گام 1: ثبت نام
```bash
# 1. برو به https://platform.openai.com
# 2. روی "Sign up" کلیک کن
# 3. اطلاعات خود را وارد کن
# 4. ایمیل خود را تأیید کن
```

#### گام 2: ایجاد API Key
```bash
# 1. وارد حساب کاربری شو
# 2. برو به بخش "API Keys" در منوی چپ
# 3. "Create new secret key" را کلیک کن
# 4. نام مناسبی برای کلید انتخاب کن (مثل: Journalist Bot)
# 5. کلید ایجاد شده را کپی کن

# ⚠️ کلید فقط یک بار نمایش داده میشه، حتماً کپی کن
```

#### گام 3: اضافه کردن اعتبار مالی
```bash
# 1. برو به بخش "Billing" 
# 2. "Add payment method" کلیک کن
# 3. کارت اعتباری یا PayPal اضافه کن
# 4. حداقل $5 اعتبار اضافه کن

# 💡 نکته: OpenAI برای کاربران جدید $5 اعتبار رایگان میده
```

### 🔮 دریافت Google Gemini API Key

#### گام 1: دسترسی به Google AI Studio
```bash
# 1. برو به https://ai.google.dev
# 2. "Get started" یا "Get API Key" کلیک کن  
# 3. با حساب گوگل خود وارد شو
```

#### گام 2: ایجاد پروژه
```bash
# 1. "Create API Key" کلیک کن
# 2. پروژه جدید ایجاد کن یا موجود انتخاب کن
# 3. کلید API را کپی کن

# 💡 نکته: Gemini محدودیت رایگان خوبی داره
```

### 📰 دریافت News API Key (اختیاری)

```bash
# 1. برو به https://newsapi.org
# 2. "Get API Key" کلیک کن
# 3. ثبت نام کن
# 4. کلید رایگان خود را کپی کن

# 💡 پلن رایگان: 1000 درخواست در ماه
```

### 🔧 تنظیم فایل .env

#### ایجاد فایل تنظیمات
```bash
# 1. کپی کردن فایل نمونه
cp .env.example .env

# 2. ویرایش فایل
# Linux/macOS:
nano .env
# یا
gedit .env

# Windows:
notepad .env
```

#### محتوای فایل .env
```env
# 🤖 تنظیمات ربات تلگرام (ضروری)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
BOT_USERNAME=my_journalist_bot

# 🧠 سرویس‌های AI (حداقل یکی ضروری)
OPENAI_API_KEY=sk-proj-your_long_openai_key_here...
GEMINI_API_KEY=your_gemini_api_key_here

# 📰 API اخبار (اختیاری)
NEWS_API_KEY=your_news_api_key_here

# 👥 مدیران ربات (User ID های تلگرام - کاما جدا)
ADMIN_IDS=123456789,987654321

# 💾 پایگاه داده (اختیاری)
DATABASE_URL=sqlite:///bot.db

# ⚙️ تنظیمات پیشرفته (اختیاری)
MAX_REQUESTS_PER_MINUTE=30
FREE_DAILY_LIMIT=50
CACHE_TTL_HOURS=12
LOG_LEVEL=INFO
```

### 🔍 پیدا کردن User ID تلگرام خود

```bash
# روش 1: استفاده از @userinfobot
# 1. در تلگرام به @userinfobot برو
# 2. /start بزن
# 3. User ID ات رو میگه

# روش 2: استفاده از @myidbot  
# 1. در تلگرام به @myidbot برو
# 2. /getid بزن

# User ID شما عددی شبیه 123456789 است
```

---

## ⚙️ پیکربندی ربات

### 📁 ایجاد پوشه‌های ضروری

```bash
# اطمینان از وجود پوشه‌ها
mkdir -p logs uploads cache data

# تنظیم مجوزها (Linux/macOS)
chmod 755 logs uploads cache
chmod 644 .env

# بررسی ساختار
ls -la
# باید این پوشه‌ها را ببینید:
# drwxr-xr-x logs/
# drwxr-xr-x uploads/  
# drwxr-xr-x cache/
# -rw-r--r-- .env
```

### 🔒 امنیت فایل تنظیمات

```bash
# محافظت از فایل .env (Linux/macOS)
chmod 600 .env
ls -la .env
# باید نتیجه شبیه این باشد:
# -rw------- 1 user user 1234 date .env

# Windows: روی فایل .env راست کلیک > Properties > Security
# فقط به کاربر فعلی دسترسی خواندن دهید
```

### 🧪 تست تنظیمات

```bash
# بررسی کامل تنظیمات
python main.py --health

# خروجی موردانتظار:
# 🔍 بررسی پیش‌نیازها...
# ✅ Python Version: 3.11.x  
# ✅ Config File: .env loaded
# ✅ Bot Token: Valid
# ✅ OpenAI API: Connected / ⚠️ Not configured
# ✅ Gemini API: Connected / ⚠️ Not configured
# ✅ Project Structure: Complete
# ✅ File Permissions: Secure
# 
# 🎉 سیستم آماده اجراست!
```

---

## 🧪 تست و راه‌اندازی

### 🚀 اجرای اولیه

```bash
# اطمینان از فعال بودن محیط مجازی
source venv/bin/activate  # Linux/macOS
# یا
venv\Scripts\activate     # Windows

# اجرای ربات
python main.py

# خروجی موردانتظار:
# ╔══════════════════════════════════════════════════╗
# ║            🤖 Assistant Journalist Bot            ║
# ║        ربات هوشمند دستیار خبرنگار                ║
# ╚══════════════════════════════════════════════════╝
# 
# ✅ تمام پیش‌نیازها برآورده شده‌اند
# 🤖 Bot Username: @my_journalist_bot
# ⚙️ سرویس‌های فعال: OpenAI, Gemini
# 🚀 شروع ربات...
# ربات آماده است!
```

### 📱 تست در تلگرام

#### گام 1: پیدا کردن ربات
```bash
# 1. تلگرام را باز کن
# 2. در جستجو username ربات را بنویس (مثل @my_journalist_bot)
# 3. روی ربات کلیک کن
# 4. "START" یا "شروع" را بزن
```

#### گام 2: تست دستورات اصلی
```bash
# تست این دستورات:
/start    # باید پیام خوشامدگویی بیاید
/menu     # باید منوی اصلی نمایش داده شود  
/help     # باید راهنما نمایش داده شود
/mystats  # باید آمار شخصی شما نمایش داده شود
```

#### گام 3: تست ویژگی‌ها
```bash
# 1. روی "📰 تولید محتوا" کلیک کن
# 2. "📝 نگارش خبر" را انتخاب کن
# 3. یک متن خبری کوتاه ارسال کن
# 4. باید 3 جفت تیتر و لید دریافت کنی

# مثال متن تست:
# شرکت گوگل امروز اعلام کرد که قصد دارد تا پایان سال جاری یک هوش مصنوعی جدید عرضه کند.
```

### 📊 مانیتورینگ اولیه

```bash
# مشاهده لاگ‌های زنده
tail -f logs/bot.log

# بررسی آمار ربات (با حساب ادمین)
# در تلگرام: /stats

# خروجی نمونه:
# 📊 آمار کلی ربات
# ⏱️ زمان فعالیت: 0.5 ساعت
# 👥 کل کاربران: 1
# 🟢 کاربران فعال امروز: 1
# 💬 کل پیام‌ها: 5
# 🤖 درخواست‌های AI: 2
# ❌ کل خطاها: 0
# ⚡ میانگین زمان پاسخ: 1.234s
```

---

## 🐳 نصب با Docker

### 📋 پیش‌نیازهای Docker

#### 🐧 Ubuntu/Debian
```bash
# حذف نسخه‌های قدیمی
sudo apt remove docker docker-engine docker.io containerd runc

# نصب وابستگی‌ها
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# اضافه کردن کلید GPG رسمی Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# اضافه کردن مخزن
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# نصب Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# اضافه کردن کاربر به گروه docker
sudo usermod -aG docker $USER

# راه‌اندازی سرویس
sudo systemctl start docker
sudo systemctl enable docker

# تست نصب
docker --version
docker compose version
```

#### 🍎 macOS
```bash
# دانلود Docker Desktop از:
# https://docs.docker.com/desktop/mac/install/

# یا با Homebrew:
brew install --cask docker

# راه‌اندازی Docker Desktop از Applications
# تست نصب:
docker --version
```

#### 🪟 Windows
```powershell
# دانلود Docker Desktop از:
# https://docs.docker.com/desktop/windows/install/

# نصب و راه‌اندازی Docker Desktop
# تست نصب:
docker --version
```

### 🚀 اجرای ربات با Docker

#### روش 1: Docker Compose (توصیه شده)
```bash
# 1. اطمینان از وجود فایل .env
cp .env.example .env
# ویرایش .env با API Keys واقعی

# 2. اجرای ربات
docker compose up -d

# 3. مشاهده لاگ‌ها
docker compose logs -f journalist-bot

# 4. بررسی وضعیت
docker compose ps

# 5. متوقف کردن
docker compose down
```

#### روش 2: Docker Build دستی
```bash
# 1. ساخت image
docker build -t journalist-bot .

# 2. اجرا
docker run -d \
  --name assistant-journalist-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/cache:/app/cache \
  --restart unless-stopped \
  journalist-bot

# 3. مشاهده لاگ‌ها
docker logs -f assistant-journalist-bot
```

### 🔧 مدیریت Docker

```bash
# مشاهده container های در حال اجرا
docker ps

# مشاهده تمام container ها
docker ps -a

# ورود به container
docker exec -it assistant-journalist-bot /bin/bash

# راه‌اندازی مجدد
docker restart assistant-journalist-bot

# حذف container
docker rm -f assistant-journalist-bot

# حذف image
docker rmi journalist-bot

# پاک کردن تمام داده‌های Docker (احتیاط!)
docker system prune -a
```

---

## 🚀 تولید (Production)

### ☁️ انتخاب پلتفرم

| پلتفرم | مناسب برای | هزینه تقریبی/ماه | دشواری |
|---------|-------------|------------------|---------|
| **VPS (DigitalOcean/Linode)** | کنترل کامل | $10-50 | متوسط |
| **Heroku** | سادگی | $7-25 | آسان |
| **AWS EC2** | مقیاس‌پذیری | $10-100+ | دشوار |
| **Google Cloud Run** | کارایی | Pay-per-use | متوسط |
| **Railway** | توسعه‌دهندگان | $5-20 | آسان |

### 🔧 تنظیمات Production

#### فایل .env.production
```env
# تنظیمات Production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# امنیت
BOT_TOKEN=your_production_bot_token
OPENAI_API_KEY=your_production_openai_key
GEMINI_API_KEY=your_production_gemini_key

# پایگاه داده Production
DATABASE_URL=postgresql://user:pass@localhost:5432/botdb

# محدودیت‌های Production
MAX_REQUESTS_PER_MINUTE=100
FREE_DAILY_LIMIT=1000
PRO_DAILY_LIMIT=10000

# کش Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_HOURS=24

# مانیتورینگ
SENTRY_DSN=https://your-sentry-dsn
ENABLE_METRICS=true
```

### 🔒 تنظیمات امنیتی Production

#### SSL/TLS Certificate
```bash
# نصب Certbot
sudo apt install certbot python3-certbot-nginx

# دریافت گواهی SSL رایگان
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# تست تجدید خودکار
sudo certbot renew --dry-run

# تنظیم cron job برای تجدید خودکار
sudo crontab -e
# اضافه کردن:
0 12 * * * /usr/bin/certbot renew --quiet
```

#### Firewall تنظیمات
```bash
# Ubuntu/Debian با UFW
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 22/tcp from any to any
sudo ufw --force enable

# CentOS/RHEL با firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### امنیت فایل‌ها
```bash
# تنظیم مالکیت
sudo chown -R bot:bot /path/to/bot
sudo chmod -R 750 /path/to/bot

# محافظت از فایل‌های حساس
sudo chmod 600 /path/to/bot/.env.production
sudo chmod 600 /path/to/bot/logs/*.log

# SELinux (اگر فعال است)
sudo setsebool -P httpd_can_network_connect 1
```

### 🎯 استقرار VPS

#### Digital Ocean Droplet
```bash
# 1. ایجاد Droplet
# Size: 2GB RAM, 1 vCPU, 50GB SSD
# OS: Ubuntu 22.04 LTS
# Region: نزدیک‌ترین به کاربران

# 2. اتصال SSH
ssh root@your-droplet-ip

# 3. به‌روزرسانی سیستم
apt update && apt upgrade -y

# 4. ایجاد کاربر غیر root
adduser botuser
usermod -aG sudo botuser
su - botuser

# 5. کپی کردن کلیدهای SSH
mkdir ~/.ssh
chmod 700 ~/.ssh
# کپی محتوای /root/.ssh/authorized_keys به ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 6. نصب Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker botuser

# 7. کلون پروژه
git clone https://github.com/your-username/assistant-journalist-bot.git
cd assistant-journalist-bot

# 8. تنظیم محیط production
cp .env.example .env.production
nano .env.production
# ویرایش با مقادیر واقعی

# 9. اجرا
docker compose -f docker-compose.prod.yml up -d

# 10. تنظیم auto-start
sudo systemctl enable docker
```

#### Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/journalist-bot
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        proxy_pass http://localhost:8000/health;
        access_log off;
    }
}

# فعال‌سازی سایت
sudo ln -s /etc/nginx/sites-available/journalist-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 📊 مانیتورینگ Production

#### Systemd Service
```ini
# /etc/systemd/system/journalist-bot.service
[Unit]
Description=Assistant Journalist Bot
After=network.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/botuser/assistant-journalist-bot
ExecStart=/usr/bin/docker compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker compose -f docker-compose.prod.yml down
User=botuser
Group=botuser

[Install]
WantedBy=multi-user.target
```

#### راه‌اندازی Service
```bash
# فعال‌سازی service
sudo systemctl daemon-reload
sudo systemctl enable journalist-bot.service
sudo systemctl start journalist-bot.service

# بررسی وضعیت
sudo systemctl status journalist-bot.service

# مشاهده لاگ‌ها
sudo journalctl -u journalist-bot.service -f
```

#### Health Check Script
```bash
# ~/health-check.sh
#!/bin/bash
HEALTH_URL="http://localhost:8000/health"
TELEGRAM_BOT_TOKEN="your_monitoring_bot_token"
CHAT_ID="your_admin_chat_id"

if ! curl -sf "$HEALTH_URL" > /dev/null; then
    MESSAGE="🚨 Assistant Journalist Bot is DOWN!"
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE"
    
    # تلاش برای راه‌اندازی مجدد
    sudo systemctl restart journalist-bot.service
fi

# تنظیم cron job
# crontab -e
# */5 * * * * /home/botuser/health-check.sh
```

---

## ❌ عیب‌یابی

### 🔍 مشکلات رایج و راه‌حل‌ها

#### 1. خطای "ModuleNotFoundError"
```bash
# علت: محیط مجازی فعال نیست یا کتابخانه‌ها نصب نشده

# راه‌حل:
# 1. فعال‌سازی محیط مجازی
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 2. بررسی نصب کتابخانه‌ها
pip list | grep telegram
pip list | grep openai

# 3. نصب مجدد
pip install -r requirements.txt --force-reinstall
```

#### 2. خطای "FFmpeg not found"
```bash
# راه‌حل Ubuntu/Debian:
sudo apt update
sudo apt install ffmpeg
ffmpeg -version

# راه‌حل macOS:
brew install ffmpeg

# راه‌حل Windows:
# دانلود از https://ffmpeg.org
# اضافه کردن به PATH
```

#### 3. خطای "Invalid Bot Token"
```bash
# بررسی‌های ضروری:
# 1. Token در .env صحیح است؟
cat .env | grep BOT_TOKEN

# 2. فاصله یا کاراکتر اضافی؟
# Token باید دقیقاً این فرمت باشد:
# 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# 3. تست مستقیم Token
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

#### 4. خطای "OpenAI API Rate Limit"
```bash
# علت: بیش از حد مجاز درخواست ارسال شده

# راه‌حل فوری:
# 1. کاهش تعداد درخواست‌ها
echo "MAX_REQUESTS_PER_MINUTE=5" >> .env

# 2. استفاده از Gemini به عنوان جایگزین
# در .env:
GEMINI_API_KEY=your_gemini_key

# 3. بررسی کوتا OpenAI
# در https://platform.openai.com/usage
```

#### 5. خطای "Permission Denied"
```bash
# Linux/macOS:
sudo chown -R $USER:$USER /path/to/bot
chmod +x main.py

# بررسی مجوزها:
ls -la main.py
# باید -rwxr-xr-x باشد
```

#### 6. خطای Docker
```bash
# خطای "Cannot connect to Docker daemon"
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker

# خطای "Port already in use"
docker ps
docker stop <container_name>

# خطای "No space left on device"
docker system prune -a
```

### 🔧 ابزارهای عیب‌یابی

#### Debug Mode
```bash
# فعال‌سازی حالت debug
export LOG_LEVEL=DEBUG
python main.py

# یا در .env:
LOG_LEVEL=DEBUG
```

#### Verbose Logging
```bash
# لاگ‌های تفصیلی
tail -f logs/bot.log | grep ERROR
tail -f logs/bot.log | grep WARNING

# فیلتر لاگ‌های خاص
grep -n "OpenAI\|Gemini" logs/bot.log
```

#### Network Debugging
```bash
# تست اتصال به API ها
curl -I https://api.openai.com/v1/models
curl -I https://generativelanguage.googleapis.com

# بررسی DNS
nslookup api.telegram.org
nslookup api.openai.com
```

#### Memory و CPU Monitoring
```bash
# مانیتورینگ منابع
htop
# یا
top -p $(pgrep -f main.py)

# مانیتورینگ Docker
docker stats assistant-journalist-bot
```

### 📞 جمع‌آوری اطلاعات Debug

#### اسکریپت جمع‌آوری اطلاعات
```bash
#!/bin/bash
# debug-info.sh

echo "=== System Information ===" > debug-report.txt
echo "Date: $(date)" >> debug-report.txt
echo "OS: $(uname -a)" >> debug-report.txt
echo "Python: $(python3 --version)" >> debug-report.txt
echo "pip: $(pip --version)" >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Bot Information ===" >> debug-report.txt
echo "Bot Version: $(python main.py --version)" >> debug-report.txt
echo "Working Directory: $(pwd)" >> debug-report.txt
echo "Virtual Environment: $VIRTUAL_ENV" >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Configuration ===" >> debug-report.txt
echo "Config file exists: $(test -f .env && echo 'Yes' || echo 'No')" >> debug-report.txt
echo "Log directory: $(ls -la logs/)" >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Recent Errors ===" >> debug-report.txt
tail -50 logs/bot.log | grep -E "(ERROR|CRITICAL)" >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Installed Packages ===" >> debug-report.txt
pip list >> debug-report.txt

echo "Debug report saved to debug-report.txt"
```

---

## 🆘 کمک و پشتیبانی

### 🔗 منابع کمک

#### 📚 مستندات
- **مستندات کامل**: [docs.assistant-journalist-bot.com](https://docs.assistant-journalist-bot.com)
- **راهنمای API**: [api-docs.assistant-journalist-bot.com](https://api-docs.assistant-journalist-bot.com)
- **نمونه کدها**: [examples.assistant-journalist-bot.com](https://examples.assistant-journalist-bot.com)

#### 💬 کانال‌های پشتیبانی
- **تلگرام پشتیبانی**: [@assistant_journalist_support](https://t.me/assistant_journalist_support)
- **کانال اطلاعیه‌ها**: [@assistant_journalist_news](https://t.me/assistant_journalist_news)
- **گروه کاربران**: [@assistant_journalist_community](https://t.me/assistant_journalist_community)

#### 🐛 گزارش مشکلات
- **GitHub Issues**: [github.com/your-repo/issues](https://github.com/your-repo/assistant-journalist-bot/issues)
- **فرم گزارش باگ**: [bug-report.assistant-journalist-bot.com](https://bug-report.assistant-journalist-bot.com)

### 📝 قبل از درخواست کمک

#### ✅ چک‌لیست آماده‌سازی
- [ ] مستندات و FAQ را مطالعه کرده‌ام
- [ ] آخرین نسخه را نصب کرده‌ام
- [ ] `python main.py --health` را اجرا کرده‌ام
- [ ] فایل لاگ را بررسی کرده‌ام
- [ ] خطای دقیق را یادداشت کرده‌ام

#### 📋 اطلاعات مورد نیاز برای پشتیبانی
```bash
# جمع‌آوری اطلاعات سیستم
python main.py --debug-info

# اطلاعات شامل:
- نسخه سیستم عامل
- نسخه Python
- نسخه ربات
- پیکربندی اصلی
- متن کامل خطا
- مراحل بازتولید مشکل
```

### 🕐 زمان پاسخ‌گویی

| نوع مشکل | اولویت | زمان پاسخ |
|----------|---------|-----------|
| **Critical** (ربات کار نمی‌کند) | 🔴 فوری | 2-6 ساعت |
| **High** (ویژگی مهم مشکل دارد) | 🟠 بالا | 12-24 ساعت |
| **Medium** (مشکل عملکرد) | 🟡 متوسط | 1-3 روز |
| **Low** (سوال یا بهبود) | 🟢 پایین | 3-7 روز |

### 🤝 مشارکت در پروژه

#### نحوه کمک به پروژه
```bash
# 1. Fork کردن repository
# 2. کلون کردن fork
git clone https://github.com/YOUR_USERNAME/assistant-journalist-bot.git

# 3. ایجاد branch جدید
git checkout -b feature/my-improvement

# 4. انجام تغییرات
# 5. تست تغییرات
python -m pytest tests/

# 6. Commit و Push
git add .
git commit -m "feat: add amazing feature"
git push origin feature/my-improvement

# 7. ایجاد Pull Request
```

#### راه‌های مشارکت
- 🐛 **گزارش باگ** - پیدا کردن و گزارش مشکلات
- 💡 **پیشنهاد ویژگی** - ایده‌های جدید
- 📝 **بهبود مستندات** - تکمیل راهنماها
- 🌍 **ترجمه** - ترجمه به زبان‌های مختلف
- 💻 **توسعه کد** - اضافه کردن ویژگی‌های جدید

### 🎓 منابع آموزشی

#### ویدیوهای آموزشی
- **نصب و راه‌اندازی**: [youtube.com/watch?v=xxx](https://youtube.com/watch?v=xxx)
- **تنظیمات پیشرفته**: [youtube.com/watch?v=yyy](https://youtube.com/watch?v=yyy)
- **عیب‌یابی**: [youtube.com/watch?v=zzz](https://youtube.com/watch?v=zzz)

#### مقالات مفید
- **بهترین شیوه‌های استفاده**: [blog.assistant-journalist-bot.com/best-practices](https://blog.assistant-journalist-bot.com/best-practices)
- **تنظیمات امنیتی**: [blog.assistant-journalist-bot.com/security](https://blog.assistant-journalist-bot.com/security)
- **بهینه‌سازی عملکرد**: [blog.assistant-journalist-bot.com/optimization](https://blog.assistant-journalist-bot.com/optimization)

---

## 🎉 تبریک! نصب کامل شد

### ✅ چک‌لیست نهایی

#### مراحل انجام شده
- [ ] Python 3.9+ نصب شده
- [ ] FFmpeg نصب شده
- [ ] پروژه دانلود شده
- [ ] محیط مجازی ایجاد شده
- [ ] کتابخانه‌ها نصب شده
- [ ] فایل .env تنظیم شده
- [ ] API Keys پیکربندی شده
- [ ] تست اولیه انجام شده
- [ ] ربات در تلگرام کار می‌کند

#### بررسی نهایی
```bash
# تست کامل سیستم
python main.py --health

# اجرای ربات
python main.py

# تست در تلگرام
# /start در ربات تلگرام
```

### 🚀 قدم‌های بعدی

#### 1. بهینه‌سازی برای استفاده
```bash
# تنظیم کردن دستورات ربات
# در @BotFather:
/setcommands
# سپس این دستورات را ارسال کنید:
start - شروع ربات
menu - نمایش منو
help - راهنمای استفاده
mystats - آمار شخصی
```

#### 2. سفارشی‌سازی
- ویرایش پیام‌های خوشامدگویی در `handlers/`
- اضافه کردن Admin IDs در `.env`
- تنظیم محدودیت‌های استفاده
- سفارشی‌سازی prompt ها در `data/prompts.py`

#### 3. مانیتورینگ
```bash
# تنظیم مانیتورینگ منظم
crontab -e
# اضافه کردن:
0 */6 * * * cd /path/to/bot && python main.py --health
```

#### 4. پشتیبان‌گیری
```bash
# اسکریپت پشتیبان‌گیری روزانه
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/path/to/backups"
BOT_DIR="/path/to/bot"

# پشتیبان فایل‌های مهم
tar -czf "$BACKUP_DIR/bot-backup-$DATE.tar.gz" \
    "$BOT_DIR/.env" \
    "$BOT_DIR/logs/" \
    "$BOT_DIR/cache/" \
    "$BOT_DIR/uploads/"

# نگهداری فقط 7 روز اخیر
find "$BACKUP_DIR" -name "bot-backup-*.tar.gz" -mtime +7 -delete
```

### 🌟 نکات مهم برای استفاده بهینه

#### 💡 بهترین شیوه‌ها
1. **امنیت اول**: هرگز API Keys را commit نکنید
2. **پایداری**: از محیط virtual environment استفاده کنید
3. **مانیتورینگ**: لاگ‌ها را منظم بررسی کنید
4. **به‌روزرسانی**: منظم ربات را update کنید
5. **پشتیبان**: از تنظیمات و داده‌ها backup بگیرید

#### ⚡ افزایش کارایی
```bash
# کش Redis برای عملکرد بهتر
# در .env:
REDIS_URL=redis://localhost:6379/0

# محدودیت‌های هوشمند
MAX_REQUESTS_PER_MINUTE=30
CACHE_TTL_HOURS=24

# Load balancing
# ربات خودکار بین OpenAI و Gemini تعادل برقرار می‌کند
```

### 🎊 پیام نهایی

```
╔════════════════════════════════════════════════╗
║  🎉 تبریک! نصب با موفقیت انجام شد            ║
║                                                ║
║  ربات Assistant Journalist Bot شما            ║
║  آماده ارائه خدمات هوشمند خبرنگاری است     ║
║                                                ║
║  💡 نکته: برای حمایت از پروژه، در GitHub     ║
║     ستاره ⭐ فراموش نکنید!                   ║
║                                                ║
║  🤝 سوال یا مشکل؟ در تلگرام @assistant_      ║
║     journalist_support با ما در تماس باشید   ║
╚════════════════════════════════════════════════╝

🚀 موفق باشید!
```

---

<div align="center">

**🔗 لینک‌های مفید**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-repo/assistant-journalist-bot)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/assistant_journalist_support)
[![Documentation](https://img.shields.io/badge/Docs-4285F4?style=for-the-badge&logo=googledocs&logoColor=white)](https://docs.assistant-journalist-bot.com)

**❤️ با عشق برای جامعه خبرنگاری ایران ساخته شده**

</div>
