# 🤖 Assistant Journalist Bot

ربات هوشمند دستیار خبرنگار با قابلیت‌های پیشرفته AI

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## ✨ ویژگی‌های کلیدی

### 📰 تولید محتوای خبری
- تیتر و لید هوشمند (سیستم پرامپت حرفه‌ای)
- خلاصه‌سازی مقالات
- تولید سوالات مصاحبه
- بیانیه مطبوعاتی

### 🔍 راستی‌آزمایی
- پروتکل SWIFT-VERIFY
- تحلیل منابع معتبر
- گزارش جامع با درجه اطمینان

### 🎬 تولید رسانه
- اسکریپت ویدیو بهینه‌شده
- اسکریپت پادکست
- محتوای شبکه‌های اجتماعی

### 🤖 ابزارهای AI
- مهندس پرامپت (PromptCraft Master)
- بهینه‌سازی prompt تصویر
- طراحی چت‌بات

## 📁 ساختار پروژه

```
assistant_journalist_bot/
├── main.py                    # 🚀 فایل اجرا
├── .env.example              # 🔐 نمونه تنظیمات
├── requirements.txt           # 📦 کتابخانه‌ها
├── Dockerfile                # 🐳 Docker
├── docker-compose.yml        # 🐳 Docker Compose
├── README.md                  # 📚 مستندات
├── LICENSE                   # ⚖️ مجوز
├── .gitignore                # 🚫 فایل‌های نادیده گرفتنی
├── core/
│   ├── __init__.py
│   ├── bot.py                # ⚙️ هسته ربات
│   └── config.py             # 🔧 تنظیمات
├── handlers/
│   ├── __init__.py
│   ├── news_handlers.py      # 📰 هندلرهای خبری
│   ├── media_handlers.py     # 🎬 هندلرهای رسانه
│   └── ai_handlers.py        # 🤖 هندلرهای AI
├── services/
│   ├── __init__.py
│   └── ai_service.py         # 🧠 سرویس‌های AI
├── utils/
│   ├── __init__.py
│   └── keyboards.py          # ⌨️ کیبوردهای تلگرام
├── data/
│   ├── __init__.py
│   ├── prompts/              # 📝 پرامپت‌های سیستم
│   └── templates/            # 📄 الگوهای محتوا
├── uploads/                  # 📁 فایل‌های آپلود
├── cache/                    # 💾 کش
└── logs/                     # 📊 لاگ‌ها
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.9+
- FFmpeg (برای پردازش رسانه)

### نصب سریع

```bash
# 1. کلون پروژه
git clone https://github.com/your-username/assistant-journalist-bot.git
cd assistant-journalist-bot

# 2. ایجاد virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. نصب dependencies
pip install -r requirements.txt

# 4. تنظیم environment variables
cp .env.example .env
# ویرایش .env با کلیدهای واقعی

# 5. اجرا
python main.py
```

### با Docker

```bash
# اجرای ساده
docker-compose up -d

# یا build دستی
docker build -t journalist-bot .
docker run -d --env-file .env journalist-bot
```

## 🔑 تنظیمات API

### Telegram Bot Token
1. به [@BotFather](https://t.me/BotFather) مراجعه کنید
2. `/newbot` را ارسال کنید
3. Token را در `.env` قرار دهید

### OpenAI API
- دریافت از [platform.openai.com](https://platform.openai.com)

### Google Gemini API  
- دریافت از [ai.google.dev](https://ai.google.dev)

## 📖 استفاده

### دستورات اصلی
- `/start` - شروع ربات
- `/menu` - نمایش منو
- `/help` - راهنما

### بخش‌های اصلی
- **📰 تولید محتوا**: تیتر، لید، مصاحبه
- **🔍 راستی‌آزمایی**: بررسی اطلاعات
- **🎬 رسانه**: اسکریپت ویدیو، پادکست
- **⚙️ AI**: مهندسی پرامپت، چت‌بات

## 🧪 تست

```bash
# بررسی سلامت سیستم
python main.py --health

# اجرای تست‌ها
pytest tests/

# بررسی کد
black . && flake8 .
```

## 📊 مانیتورینگ

```bash
# مشاهده لاگ‌ها
tail -f logs/bot.log

# وضعیت Docker
docker-compose logs -f
```

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

## 📝 تاریخچه تغییرات

### v1.0.0 (2025-01-XX)
- انتشار اولیه
- تولید تیتر و لید خبری
- راستی‌آزمایی با پروتکل SWIFT-VERIFY
- تولید اسکریپت ویدیو
- مهندسی پرامپت

## ⚖️ مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

## 📞 پشتیبانی

- 🐛 گزارش باگ: [Issues](https://github.com/your-username/assistant-journalist-bot/issues)
- 💬 پشتیبانی: [@your_support_username](https://t.me/your_support_username)
- 📧 ایمیل: your-email@example.com

---

**🎉 ربات شما آماده تبدیل شدن به قدرتمندترین دستیار خبرنگاری است!**