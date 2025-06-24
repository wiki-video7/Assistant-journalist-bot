# utils/keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class MainKeyboard:
    @staticmethod
    def get_main_menu():
        """کیبورد منوی اصلی"""
        keyboard = [
            [
                InlineKeyboardButton("📰 تولید محتوا", callback_data="show_content_menu"),
                InlineKeyboardButton("🔍 تحقیق و تحلیل", callback_data="show_research_menu")
            ],
            [
                InlineKeyboardButton("🎬 تولید رسانه", callback_data="show_media_menu"),
                InlineKeyboardButton("⚙️ ابزارهای AI", callback_data="show_ai_menu")
            ],
            [
                InlineKeyboardButton("📚 راهنما", callback_data="show_help"),
                InlineKeyboardButton("ℹ️ درباره ما", callback_data="show_about")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_content_menu():
        """منوی تولید محتوا"""
        keyboard = [
            [InlineKeyboardButton("📝 نگارش خبر", callback_data="news_write")],
            [InlineKeyboardButton("📋 خلاصه‌سازی", callback_data="news_summary")],
            [InlineKeyboardButton("💬 سوالات مصاحبه", callback_data="news_interview")],
            [InlineKeyboardButton("📢 بیانیه مطبوعاتی", callback_data="news_press")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_research_menu():
        """منوی تحقیق"""
        keyboard = [
            [InlineKeyboardButton("🔎 جستجوی خبر", callback_data="research_search")],
            [InlineKeyboardButton("✅ راستی‌آزمایی", callback_data="news_factcheck")],
            [InlineKeyboardButton("📊 تحلیل روند", callback_data="research_trend")],
            [InlineKeyboardButton("🌐 بررسی منابع", callback_data="research_sources")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_media_menu():
        """منوی رسانه"""
        keyboard = [
            [InlineKeyboardButton("🎥 اسکریپت ویدیو", callback_data="media_video_script")],
            [InlineKeyboardButton("📻 اسکریپت پادکست", callback_data="media_podcast")],
            [InlineKeyboardButton("📱 محتوای اجتماعی", callback_data="media_social")],
            [InlineKeyboardButton("🗜️ فشرده‌سازی", callback_data="media_compress")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_ai_menu():
        """منوی ابزارهای AI"""
        keyboard = [
            [InlineKeyboardButton("🤖 مهندس Prompt", callback_data="ai_prompt_engineer")],
            [InlineKeyboardButton("🖼️ متن به تصویر", callback_data="ai_text_to_image")],
            [InlineKeyboardButton("💬 مهندس چت‌بات", callback_data="ai_chatbot")],
            [InlineKeyboardButton("📚 کتابخانه الگو", callback_data="ai_templates")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
