# core/config.py - ساده‌شده

import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

class Config:
    """تنظیمات ربات - ساده‌شده"""
    
    # تنظیمات اصلی (اجباری)
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "assistant_journalist_bot")
    
    # کلیدهای AI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    
    # تنظیمات فایل
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR = "uploads"
    CACHE_DIR = "cache"
    LOGS_DIR = "logs"
    
    # محدودیت‌ها
    FREE_DAILY_LIMIT = 10
    PRO_DAILY_LIMIT = 100
    MAX_TEXT_LENGTH = 4000
    
    # ادمین‌ها (اختیاری)
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    @classmethod
    def validate(cls):
        """بررسی تنظیمات ضروری"""
        if not cls.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN در فایل .env موجود نیست!")
        
        if not cls.OPENAI_API_KEY and not cls.GEMINI_API_KEY:
            print("⚠️  هیچ کلید AI تنظیم نشده - برخی ویژگی‌ها کار نخواهند کرد")
        
        # ایجاد پوشه‌ها
        for directory in [cls.UPLOAD_DIR, cls.CACHE_DIR, cls.LOGS_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """بررسی ادمین بودن"""
        return user_id in cls.ADMIN_IDS

# بررسی تنظیمات در هنگام import
config = Config()
config.validate()
