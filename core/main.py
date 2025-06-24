#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assistant Journalist Bot - Main Entry Point
ربات دستیار خبرنگار - نقطه ورود اصلی

هوشمندترین ربات خبرنگاری با قابلیت‌های AI پیشرفته
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# اضافه کردن مسیر پروژه به Python path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Import های اصلی
try:
    from core.bot import JournalistBot
    from core.config import config
except ImportError as e:
    print(f"❌ خطا در import: {e}")
    print("لطفاً مطمئن شوید که تمام فایل‌های مورد نیاز موجود هستند.")
    sys.exit(1)

# تنظیم logging
def setup_logging():
    """تنظیم سیستم لاگ‌گیری"""
    
    # ایجاد پوشه logs
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # تنظیمات لاگ
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # تنظیم فایل لاگ
    log_file = logs_dir / "bot.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # کم کردن سطح لاگ کتابخانه‌های خارجی
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)

def check_requirements():
    """بررسی پیش‌نیازها"""
    print("🔍 بررسی پیش‌نیازها...")
    
    # بررسی Python version
    if sys.version_info < (3, 9):
        print("❌ نسخه Python باید 3.9 یا بالاتر باشد")
        print(f"نسخه فعلی: {sys.version}")
        return False
    
    # بررسی کتابخانه‌های ضروری
    required_packages = [
        'telegram',
        'openai',
        'google.generativeai',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ کتابخانه‌های زیر نصب نشده‌اند:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nبرای نصب:")
        print("pip install -r requirements.txt")
        return False
    
    # بررسی متغیرهای محیطی
    if not config.BOT_TOKEN:
        print("❌ BOT_TOKEN در فایل .env موجود نیست")
        return False
    
    if not config.OPENAI_API_KEY and not config.GEMINI_API_KEY:
        print("⚠️  هیچ کلید API برای سرویس‌های AI تنظیم نشده")
        print("   حداقل یکی از OPENAI_API_KEY یا GEMINI_API_KEY را در .env قرار دهید")
    
    print("✅ تمام پیش‌نیازها برآورده شده‌اند")
    return True

def display_banner():
    """نمایش بنر شروع"""
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

def display_info():
    """نمایش اطلاعات سیستم"""
    print("\n📊 اطلاعات سیستم:")
    print(f"   🐍 Python: {sys.version.split()[0]}")
    print(f"   📁 مسیر پروژه: {PROJECT_ROOT}")
    print(f"   🤖 Bot Username: @{config.BOT_USERNAME}")
    
    # نمایش سرویس‌های فعال
    services = []
    if config.OPENAI_API_KEY:
        services.append("OpenAI")
    if config.GEMINI_API_KEY:
        services.append("Gemini")
    if config.NEWS_API_KEY:
        services.append("News API")
    
    if services:
        print(f"   ⚙️  سرویس‌های فعال: {', '.join(services)}")
    else:
        print("   ⚠️  هیچ سرویس AI فعال نیست")

async def startup_checks():
    """بررسی‌های شروع"""
    print("\n🔧 بررسی‌های شروع...")
    
    try:
        # تست اتصال به API
        if config.OPENAI_API_KEY:
            print("   ✅ OpenAI API Key موجود")
        
        if config.GEMINI_API_KEY:
            print("   ✅ Gemini API Key موجود")
            
        # ایجاد پوشه‌های ضروری
        directories = ['uploads', 'cache', 'logs', 'data/prompts', 'data/templates']
        for directory in directories:
            dir_path = PROJECT_ROOT / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("   ✅ پوشه‌های ضروری ایجاد شدند")
        print("   ✅ سیستم آماده اجرا است")
        
    except Exception as e:
        print(f"   ❌ خطا در بررسی‌های شروع: {e}")
        return False
    
    return True

def main():
    """تابع اصلی"""
    # نمایش بنر
    display_banner()
    
    # بررسی پیش‌نیازها
    if not check_requirements():
        print("\n❌ لطفاً ابتدا پیش‌نیازها را برآورده کنید")
        sys.
