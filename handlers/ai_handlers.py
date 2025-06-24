# handlers/ai_handlers.py - بهبود یافته

from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import MainKeyboard
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class AIHandler:
    async def handle_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت بخش AI"""
        query = update.callback_query
        await query.answer()
        
        try:
            if query.data == "show_ai_menu":
                keyboard = MainKeyboard.get_ai_menu()
                await query.edit_message_text(
                    "⚙️ **ابزارهای هوشمند AI**\n\nگزینه مورد نظر را انتخاب کنید:",
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                
            elif query.data == "ai_prompt_engineer":
                context.user_data['state'] = 'waiting_for_prompt_requirements'
                await query.edit_message_text(
                    "🤖 **مهندس Prompt**\n\n"
                    "نیازمندی‌های پرامپت خود را بنویسید:\n\n"
                    "📝 **مثال:**\n"
                    "می‌خواهم AI مشاور مالی که:\n"
                    "• به سوالات سرمایه‌گذاری پاسخ دهد\n"
                    "• ریسک‌ها را تحلیل کند\n"
                    "• زبان ساده استفاده کند\n\n"
                    "🎯 **انواع:** مشاور، نویسنده، تحلیل‌گر، معلم"
                )
                
            elif query.data == "ai_text_to_image":
                context.user_data['state'] = 'waiting_for_image_description'
                await query.edit_message_text(
                    "🖼️ **تبدیل متن به تصویر**\n\n"
                    "توضیح تصویر مورد نظر:\n\n"
                    "📝 **نکات:**\n"
                    "• از جزئیات استفاده کنید\n"
                    "• سبک هنری بگویید\n"
                    "• رنگ و نور توضیح دهید\n\n"
                    "**مثال:**\n"
                    "منظره کوه‌های برفی در غروب، آسمان نارنجی، نقاشی رنگ روغن"
                )
                
            elif query.data == "ai_chatbot":
                context.user_data['state'] = 'waiting_for_chatbot_specs'
                await query.edit_message_text(
                    "💬 **مهندس چت‌بات**\n\n"
                    "مشخصات چت‌بات مورد نظر:\n\n"
                    "📋 **شامل:**\n"
                    "• هدف (فروش، پشتیبانی، آموزش)\n"
                    "• مخاطب هدف\n"
                    "• سبک گفتگو\n"
                    "• قابلیت‌های خاص\n\n"
                    "**مثال:**\n"
                    "چت‌بات فروش آنلاین، مخاطب جوان، سبک دوستانه"
                )
                
            elif query.data == "ai_templates":
                await query.edit_message_text(
                    "📚 **کتابخانه الگوهای AI**\n\n"
                    "الگوهای آماده:\n\n"
                    "🎯 **دسته‌بندی‌ها:**\n"
                    "• الگوهای تولید محتوا\n"
                    "• الگوهای تحلیل داده\n"
                    "• الگوهای آموزشی\n"
                    "• الگوهای تجاری\n\n"
                    "🔄 در حال توسعه...",
                    reply_markup=MainKeyboard.get_main_menu(),
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"خطا در handle_ai: {e}")
            await self._send_error(query)
    
    async def process_prompt_requirements(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید پرامپت سفارشی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🤖 در حال طراحی پرامپت...")
        
        try:
            result = await ai_service.create_prompt(text, "standard")
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"🤖 **پرامپت سفارشی:**\n\n```\n{result}\n```\n\n"
                "💡 **نحوه استفاده:**\n"
                "• این پرامپت را کپی کنید\n"
                "• در ابتدای گفتگو با AI قرار دهید\n"
                "• سپس سوالات خود را بپرسید",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_prompt_requirements: {e}")
            await self._edit_error(processing_msg)
    
    async def process_image_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """بهینه‌سازی prompt تصویر"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🎨 در حال بهینه‌سازی...")
        
        try:
            prompt = f"""
توضیح زیر را به یک prompt بهینه برای تولید تصویر تبدیل کن:

{text}

Prompt باید:
- به انگلیسی باشد
- شامل جزئیات بصری دقیق
- سبک هنری مشخص
- کیفیت بالا (high quality, 4K, detailed)
- مناسب برای DALL-E, Midjourney

مثال خروجی:
"A majestic landscape at sunset, oil painting style, highly detailed, 4K"
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"🖼️ **Prompt تصویر بهینه‌شده:**\n\n"
                f"`{result}`\n\n"
                "🎯 **استفاده:**\n"
                "• در DALL-E، Midjourney یا Stable Diffusion\n"
                "• کپی کرده و در AI تصویرساز قرار دهید\n"
                "• تنظیمات مختلف آزمایش کنید",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_image_description: {e}")
            await self._edit_error(processing_msg)
    
    async def process_chatbot_specs(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """طراحی چت‌بات"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("💬 در حال طراحی چت‌بات...")
        
        try:
            prompt = f"""
مشخصات چت‌بات:

{text}

یک پرامپت کامل برای چت‌بات طراحی کن که شامل:

1. **نقش و هویت چت‌بات**
2. **اهداف و قابلیت‌ها**  
3. **سبک گفتگو**
4. **قوانین و محدودیت‌ها**
5. **مثال‌های گفتگو**

پرامپت باید آماده استفاده باشد.
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"💬 **پرامپت چت‌بات:**\n\n```\n{result}\n```\n\n"
                "🚀 **پیاده‌سازی:**\n"
                "• این پرامپت را در سیستم AI قرار دهید\n"
                "• تست‌های مختلف انجام دهید\n"
                "• بر اساس عملکرد تنظیم کنید",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_chatbot_specs: {e}")
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
