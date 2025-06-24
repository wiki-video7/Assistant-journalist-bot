# handlers/news_handlers.py - بهبود یافته

from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import MainKeyboard
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class NewsHandler:
    async def handle_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت بخش اخبار"""
        query = update.callback_query
        await query.answer()
        
        try:
            if query.data == "show_content_menu":
                keyboard = MainKeyboard.get_content_menu()
                await query.edit_message_text(
                    "📰 **بخش تولید محتوا**\n\nگزینه مورد نظر را انتخاب کنید:",
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                
            elif query.data == "news_write":
                context.user_data['state'] = 'waiting_for_news_topic'
                await query.edit_message_text(
                    "📝 **تولید تیتر و لید خبری**\n\n"
                    "متن خبری خود را ارسال کنید تا:\n"
                    "• 3 تیتر جذاب (حداکثر 7 کلمه)\n"
                    "• 3 لید مناسب\n"
                    "تولید کنم.\n\n"
                    "⚠️ متن باید به فارسی باشد."
                )
                
            elif query.data == "news_summary":
                context.user_data['state'] = 'waiting_for_article_text'
                await query.edit_message_text(
                    "📋 **خلاصه‌سازی مقاله**\n\n"
                    "متن مقاله را ارسال کنید.\n\n"
                    "✨ قابلیت‌ها:\n"
                    "• خلاصه هوشمند\n"
                    "• حفظ نکات کلیدی\n"
                    "• زبان ساده"
                )
                
            elif query.data == "news_factcheck":
                context.user_data['state'] = 'waiting_for_fact_check'
                await query.edit_message_text(
                    "✅ **راستی‌آزمایی**\n\n"
                    "ادعا یا اطلاعاتی که می‌خواهید بررسی شود را ارسال کنید.\n\n"
                    "🔍 بررسی شامل:\n"
                    "• تحلیل منابع\n"
                    "• درجه اطمینان\n"
                    "• راهنمایی عملی"
                )
                
            elif query.data == "news_interview":
                context.user_data['state'] = 'waiting_for_interview_topic'
                await query.edit_message_text(
                    "💬 **تولید سوالات مصاحبه**\n\n"
                    "موضوع مصاحبه را بنویسید.\n\n"
                    "📝 مثال:\n"
                    "مصاحبه با مدیرعامل استارتاپ"
                )
                
            elif query.data == "news_press":
                context.user_data['state'] = 'waiting_for_press_release'
                await query.edit_message_text(
                    "📢 **بیانیه مطبوعاتی**\n\n"
                    "اطلاعات کلیدی رویداد یا خبر را بنویسید:\n\n"
                    "📋 شامل:\n"
                    "• موضوع اصلی\n"
                    "• جزئیات مهم\n"
                    "• تاریخ و مکان"
                )
                
        except Exception as e:
            logger.error(f"خطا در handle_news: {e}")
            await self._send_error(query)
    
    async def process_news_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید تیتر و لید"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🔄 در حال تولید...")
        
        try:
            result = await ai_service.generate_headlines(text)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📰 **تیتر و لید تولید شده:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_news_topic: {e}")
            await self._edit_error(processing_msg)
    
    async def process_article_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """خلاصه‌سازی مقاله"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🔄 در حال خلاصه‌سازی...")
        
        try:
            prompt = f"این مقاله را به صورت خلاصه و روان خلاصه کن (حداکثر 200 کلمه):\n\n{text}"
            result = await ai_service.general_ai_chat(prompt)
            
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📋 **خلاصه مقاله:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_article_summary: {e}")
            await self._edit_error(processing_msg)
    
    async def process_fact_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """راستی‌آزمایی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🔍 در حال بررسی...")
        
        try:
            result = await ai_service.fact_check(text)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"✅ **گزارش راستی‌آزمایی:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_fact_check: {e}")
            await self._edit_error(processing_msg)
    
    async def process_interview_questions(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید سوالات مصاحبه"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("💬 در حال تولید سوالات...")
        
        try:
            prompt = f"""
برای موضوع "{text}" ، 10 سوال مصاحبه حرفه‌ای بنویس.

سوالات باید:
- متنوع و جذاب
- از ساده به پیچیده
- شماره‌گذاری شده
- به فارسی

فرمت:
1. [سوال اول]
2. [سوال دوم]
...
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"💬 **سوالات مصاحبه:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_interview_questions: {e}")
            await self._edit_error(processing_msg)
    
    async def process_press_release(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید بیانیه مطبوعاتی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("📢 در حال تولید بیانیه...")
        
        try:
            prompt = f"""
بیانیه مطبوعاتی حرفه‌ای برای این اطلاعات بنویس:

{text}

ساختار:
- تیتر جذاب
- پاراگراف اول (مهم‌ترین اطلاعات)
- جزئیات
- نقل قول (اگر ممکن)
- اطلاعات تماس

زبان: رسمی و حرفه‌ای
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📢 **بیانیه مطبوعاتی:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_press_release: {e}")
            await self._edit_error(processing_msg)
    
    async def _send_error(self, query):
        """ارسال پیام خطا"""
        await query.edit_message_text(
            "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.",
            reply_markup=MainKeyboard.get_main_menu()
        )
    
    async def _edit_error(self, message):
        """ویرایش پیام با خطا"""
        await message.edit_text(
            "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
            reply_markup=MainKeyboard.get_main_menu()
        )
