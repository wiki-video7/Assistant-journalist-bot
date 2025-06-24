# handlers/news_handlers.py - نسخه بهبود یافته با سیستم پرامپت‌ها

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.keyboards import MainKeyboard
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class NewsHandler:
    def __init__(self):
        pass
    
    async def handle_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت بخش اخبار"""
        query = update.callback_query
        await query.answer()
        
        try:
            if query.data == "show_content_menu":
                keyboard = MainKeyboard.get_content_menu()
                await query.edit_message_text(
                    "📰 **بخش تولید محتوا**\n\n"
                    "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                
            elif query.data == "news_write":
                context.user_data['state'] = 'waiting_for_news_topic'
                await query.edit_message_text(
                    "📝 **تولید تیتر و لید خبری**\n\n"
                    "لطفاً متن خبری خود را ارسال کنید تا برای شما:\n"
                    "• 3 تیتر جذاب (حداکثر 7 کلمه)\n"
                    "• 3 لید مناسب\n"
                    "تولید کنم.\n\n"
                    "⚠️ متن باید به فارسی باشد."
                )
                
            elif query.data == "news_summary":
                context.user_data['state'] = 'waiting_for_article_text'
                await query.edit_message_text(
                    "📋 **خلاصه‌سازی مقاله**\n\n"
                    "متن مقاله‌ای که می‌خواهید خلاصه شود را ارسال کنید.\n\n"
                    "✨ قابلیت‌ها:\n"
                    "• خلاصه‌سازی هوشمند\n"
                    "• حفظ نکات کلیدی\n"
                    "• زبان ساده و روان"
                )
                
            elif query.data == "news_factcheck":
                context.user_data['state'] = 'waiting_for_fact_check'
                await query.edit_message_text(
                    "✅ **راستی‌آزمایی**\n\n"
                    "ادعا یا اطلاعاتی که می‌خواهید راستی‌آزمایی شود را ارسال کنید.\n\n"
                    "🔍 پروتکل SWIFT-VERIFY:\n"
                    "• بررسی منابع معتبر\n"
                    "• تحلیل متقابل\n"
                    "• ارائه درجه اطمینان\n"
                    "• راهنمایی عملی"
                )
                
            elif query.data == "news_interview":
                context.user_data['state'] = 'waiting_for_interview_topic'
                await query.edit_message_text(
                    "💬 **تولید سوالات مصاحبه**\n\n"
                    "موضوع یا شخصیتی که می‌خواهید برای آن سوالات مصاحبه تهیه کنم را مشخص کنید.\n\n"
                    "📝 مثال:\n"
                    "• مصاحبه با مدیرعامل استارتاپ\n"
                    "• مصاحبه در مورد تحصیل در خارج\n"
                    "• مصاحبه ورزشی"
                )
                
            elif query.data == "news_press":
                context.user_data['state'] = 'waiting_for_press_release'
                await query.edit_message_text(
                    "📢 **بیانیه مطبوعاتی**\n\n"
                    "اطلاعات کلیدی رویداد، محصول یا خبری که می‌خواهید بیانیه‌اش را تهیه کنم:\n\n"
                    "📋 شامل کنید:\n"
                    "• موضوع اصلی\n"
                    "• جزئیات مهم\n"
                    "• تاریخ و مکان (در صورت وجود)\n"
                    "• اطلاعات تماس"
                )
                
        except Exception as e:
            logger.error(f"خطا در handle_news: {e}")
            await query.edit_message_text(
                "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_news_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """پردازش تولید تیتر و لید"""
        context.user_data['state'] = 'idle'
        
        # نمایش پیام در حال پردازش
        processing_msg = await update.message.reply_text("🔄 در حال تولید تیتر و لید...")
        
        try:
            # تولید تیتر و لید با سیستم پرامپت
            result = await ai_service.generate_headlines(text)
            
            # حذف پیام پردازش
            await processing_msg.delete()
            
            # ارسال نتیجه
            await update.message.reply_text(
                f"📰 **تیتر و لید تولید شده:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_news_topic: {e}")
            await processing_msg.edit_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_article_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """پردازش خلاصه‌سازی مقاله"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🔄 در حال خلاصه‌سازی...")
        
        try:
            # خلاصه‌سازی با AI
            summary_prompt = f"""
لطفاً این مقاله را به صورت خلاصه و مفید خلاصه کن:

{text}

خلاصه باید:
- نکات اصلی را شامل شود
- خواندنی و روان باشد
- حداکثر 200 کلمه
- به فارسی باشد
            """
            
            result = await ai_service.general_ai_chat(summary_prompt)
            
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📋 **خلاصه مقاله:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_article_summary: {e}")
            await processing_msg.edit_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_fact_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """پردازش راستی‌آزمایی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🔍 در حال راستی‌آزمایی...")
        
        try:
            # راستی‌آزمایی با سیستم پرامپت
            result = await ai_service.fact_check(text)
            
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"✅ **گزارش راستی‌آزمایی:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_fact_check: {e}")
            await processing_msg.edit_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_interview_questions(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید سوالات مصاحبه"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("💬 در حال تولید سوالات...")
        
        try:
            interview_prompt = f"""
برای موضوع زیر، 10 سوال مصاحبه حرفه‌ای تولید کن:

{text}

سوالات باید:
- متنوع و جذاب باشند
- از ساده به پیچیده پیش بروند
- باعث کشف اطلاعات جدید شوند
- به فارسی باشند
- شماره‌گذاری شوند

فرمت:
1. [سوال اول]
2. [سوال دوم]
...
            """
            
            result = await ai_service.general_ai_chat(interview_prompt)
            
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"💬 **سوالات مصاحبه:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_interview_questions: {e}")
            await processing_msg.edit_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_press_release(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید بیانیه مطبوعاتی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("📢 در حال تولید بیانیه...")
        
        try:
            press_prompt = f"""
بر اساس اطلاعات زیر، یک بیانیه مطبوعاتی حرفه‌ای تولید کن:

{text}

بیانیه باید شامل:
- تیتر جذاب
- پاراگراف اول (مهم‌ترین اطلاعات)
- جزئیات بیشتر
- نقل قول (در صورت امکان)
- اطلاعات تماس
- زبان رسمی و حرفه‌ای
- به فارسی
            """
            
            result = await ai_service.general_ai_chat(press_prompt)
            
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📢 **بیانیه مطبوعاتی:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_press_release: {e}")
            await processing_msg.edit_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
