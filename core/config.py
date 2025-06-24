# config.py - تنظیمات ربات
from dotenv import load_dotenv
load_dotenv()  

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
   """کلاس تنظیمات ربات"""
   
   # تنظیمات ربات تلگرام
   BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
   BOT_USERNAME: str = os.getenv("BOT_USERNAME", "assistant_journalist_bot")
   
   # تنظیمات AI
   OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
   GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
   
   # تنظیمات دیتابیس
   DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///bot.db")
   
   # تنظیمات فایل
   MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
   UPLOAD_DIR: str = "uploads/"
   CACHE_DIR: str = "cache/"
   
   # محدودیت‌های کاربری
   FREE_DAILY_LIMIT: int = 10
   PRO_DAILY_LIMIT: int = 100
   MAX_TEXT_LENGTH: int = 4000
   
   # تنظیمات Whisper
   WHISPER_MODEL: str = "base"
   
   # Admin users
   ADMIN_IDS: list = [123456789]  # لیست آیدی ادمین‌ها
   
   # URLs
   NEWS_API_URL: str = "https://newsapi.org/v2/"
   NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
   
   def __post_init__(self):
       """بررسی تنظیمات ضروری"""
       if not self.BOT_TOKEN:
           raise ValueError("BOT_TOKEN الزامی است!")
           
       # ایجاد پوشه‌های ضروری
       os.makedirs(self.UPLOAD_DIR, exist_ok=True)
       os.makedirs(self.CACHE_DIR, exist_ok=True)
       
   def is_admin(self, user_id: int) -> bool:
       """بررسی ادمین بودن کاربر"""
       return user_id in self.ADMIN_IDS
       
   def get_ai_model(self, service: str = "openai") -> Optional[str]:
       """انتخاب مدل AI"""
       models = {
           "openai": "gpt-3.5-turbo",
           "gemini": "gemini-pro"
       }
       return models.get(service)

# نمونه instance برای استفاده
config = Config()
