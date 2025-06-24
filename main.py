#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assistant Journalist Bot
ربات هوشمند دستیار خبرنگار

نقطه ورود اصلی پروژه
"""

import sys
import os
import logging
from pathlib import Path

# اضافه کردن مسیر پروژه به Python path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

def setup_logging():
    """تنظیم سیستم لاگ"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "bot.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # کم کردن لاگ‌های اضافی
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)

def check_requirements():
    """بررسی پیش‌نیازها"""
    print("🔍 بررسی پیش‌نیازها...")
    
    # بررسی Python version
    if sys.version_info < (3, 8):
        print("❌ نسخه Python باید 3.8 یا بالاتر باشد")
        return False
    
    # بررسی کتابخانه‌های ضروری
    required_packages = ['telegram', 'openai', 'google.generativeai', 'dotenv']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('.', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ کتابخانه‌های گمشده: {', '.join(missing)}")
        print("برای نصب: pip install -r requirements.txt")
        return False
    
    print("✅ پیش‌نیازها برآورده شده")
    return True

def display_banner():
    """نمایش بنر"""
    banner = """
╔══════════════════════════════════════════════════╗
║            🤖 Assistant Journalist Bot            ║
║                                                  ║
║        ربات هوشمند دستیار خبرنگار                ║
║                                                  ║
║  📰 تولید محتوا  🔍 راستی‌آزمایی  🎬 تولید رسانه   ║
║                                                  ║
║              Powered by Advanced AI              ║
╚══════════════════════════════════════════════════╝
    """
    print(banner)

def create_directories():
    """ایجاد پوشه‌های ضروری"""
    dirs = ['logs', 'uploads', 'cache', 'data/prompts', 'data/templates']
    for directory in dirs:
        (PROJECT_ROOT / directory).mkdir(parents=True, exist_ok=True)

def main():
    """تابع اصلی"""
    display_banner()
    
    if not check_requirements():
        print("\n❌ لطفاً ابتدا پیش‌نیازها را نصب کنید")
        sys.exit(1)
    
    setup_logging()
    create_directories()
    
    try:
        # Import بعد از تنظیمات
        from core.bot import JournalistBot
        from core.config import config
        
        # بررسی تنظیمات
        if not config.BOT_TOKEN:
            print("❌ BOT_TOKEN در فایل .env موجود نیست")
            sys.exit(1)
        
        print(f"🤖 Bot Username: @{config.BOT_USERNAME}")
        
        # نمایش سرویس‌های فعال
        services = []
        if config.OPENAI_API_KEY:
            services.append("OpenAI")
        if config.GEMINI_API_KEY:
            services.append("Gemini")
        
        if services:
            print(f"⚙️  سرویس‌های فعال: {', '.join(services)}")
        else:
            print("⚠️  هیچ سرویس AI فعال نیست")
        
        print("\n🚀 شروع ربات...")
        
        # ایجاد و اجرای ربات
        bot = JournalistBot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n⏹️  ربات متوقف شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        sys.exit(1)
    finally:
        print("👋 خداحافظ!")

if __name__ == "__main__":
    # بررسی آرگومان‌های خط فرمان
    if len(sys.argv) > 1:
        if sys.argv[1] == "--version":
            print("Assistant Journalist Bot v1.0.0")
            sys.exit(0)
        elif sys.argv[1] == "--help":
            print("""
Assistant Journalist Bot - دستیار هوشمند خبرنگار

استفاده:
    python main.py              # اجرای ربات
    python main.py --version    # نمایش نسخه
    python main.py --help       # نمایش راهنما

ویژگی‌ها:
    📰 تولید تیتر و لید خبری
    ✅ راستی‌آزمایی اطلاعات
    🎬 تولید اسکریپت ویدیو
    🤖 مهندسی پرامپت
            """)
            sys.exit(0)
    
    main()
