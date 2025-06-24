# handlers/media_handlers.py - بهبود یافته

from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import MainKeyboard
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class MediaHandler:
    async def handle_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت بخش رسانه"""
        query = update.callback_query
        await query.answer()
        
        try:
            if query.data == "show_media_menu":
                keyboard = MainKeyboard.get_media_menu()
                await query.edit_message_text(
                    "🎬 **بخش تولید رسانه**\n\nگزینه مورد نظر را انتخاب کنید:",
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                
            elif query.data == "media_video_script":
                context.user_data['state'] = 'waiting_for_video_topic'
                await query.edit_message_text(
                    "🎥 **تولید اسکریپت ویدیو**\n\n"
                    "اطلاعات ویدیو را بنویسید:\n\n"
                    "📝 **مثال:**\n"
                    "موضوع: نکات تغذیه سالم\n"
                    "مدت: 60 ثانیه\n"
                    "پلتفرم: اینستاگرام\n\n"
                    "✨ شامل توضیحات بصری و صوتی"
                )
                
            elif query.data == "media_podcast":
                context.user_data['state'] = 'waiting_for_podcast_topic'
                await query.edit_message_text(
                    "📻 **اسکریپت پادکست**\n\n"
                    "موضوع و جزئیات پادکست:\n\n"
                    "📋 **شامل:**\n"
                    "• موضوع اصلی\n"
                    "• مدت زمان\n"
                    "• سبک (گفتگو/مصاحبه)\n"
                    "• مخاطب هدف"
                )
                
            elif query.data == "media_social":
                context.user_data['state'] = 'waiting_for_social_content'
                await query.edit_message_text(
                    "📱 **محتوای شبکه‌های اجتماعی**\n\n"
                    "نوع محتوا و موضوع:\n\n"
                    "🎯 **انواع:**\n"
                    "• پست اینستاگرام\n"
                    "• توییت\n"
                    "• پست لینکدین\n"
                    "• استوری"
                )
                
            elif query.data == "media_compress":
                await query.edit_message_text(
                    "🗜️ **فشرده‌سازی فایل**\n\n"
                    "فایل ویدیو یا صوتی خود را ارسال کنید.\n\n"
                    "⚙️ **قابلیت‌ها:**\n"
                    "• کاهش حجم\n"
                    "• تبدیل فرمت\n"
                    "• بهینه‌سازی کیفیت\n\n"
                    "🔄 در حال توسعه..."
                )
                
        except Exception as e:
            logger.error(f"خطا در handle_media: {e}")
            await self._send_error(query)
    
    async def process_video_script(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید اسکریپت ویدیو"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("🎬 در حال تولید اسکریپت...")
        
        try:
            # استخراج اطلاعات از متن
            topic, duration, platform = self._parse_video_info(text)
            
            result = await ai_service.generate_video_script(topic, duration, platform)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"🎥 **اسکریپت ویدیو:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_video_script: {e}")
            await self._edit_error(processing_msg)
    
    async def process_podcast_script(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید اسکریپت پادکست"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("📻 در حال تولید اسکریپت...")
        
        try:
            prompt = f"""
اسکریپت پادکست کامل برای:

{text}

ساختار:
- مقدمه جذاب (30 ثانیه)
- معرفی موضوع (1 دقیقه)
- بحث اصلی (قسمت‌های مختلف)
- جمع‌بندی و CTA

سبک: گفتاری و دوستانه
زبان: فارسی
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📻 **اسکریپت پادکست:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_podcast_script: {e}")
            await self._edit_error(processing_msg)
    
    async def process_social_content(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """تولید محتوای شبکه‌های اجتماعی"""
        context.user_data['state'] = 'idle'
        
        processing_msg = await update.message.reply_text("📱 در حال تولید محتوا...")
        
        try:
            prompt = f"""
محتوای جذاب برای شبکه‌های اجتماعی:

{text}

شامل:
- متن اصلی کوتاه و جذاب
- هشتگ‌های مناسب
- Call to Action
- ایموجی‌های مناسب

سبک: جذاب و تعاملی
زبان: فارسی
            """
            
            result = await ai_service.general_ai_chat(prompt)
            await processing_msg.delete()
            
            await update.message.reply_text(
                f"📱 **محتوای شبکه‌های اجتماعی:**\n\n{result}",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_social_content: {e}")
            await self._edit_error(processing_msg)
    
    async def process_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل اسناد"""
        document = update.message.document
        
        try:
            file_name = document.file_name.lower()
            file_size = document.file_size
            
            # بررسی حجم فایل
            if file_size > 50 * 1024 * 1024:  # 50MB
                await update.message.reply_text(
                    "❌ حجم فایل بیش از 50MB است.",
                    reply_markup=MainKeyboard.get_main_menu()
                )
                return
            
            # بررسی نوع فایل
            supported_types = ['.pdf', '.doc', '.docx', '.txt']
            if any(file_name.endswith(ext) for ext in supported_types):
                await update.message.reply_text(
                    f"📄 **فایل دریافت شد:**\n"
                    f"📎 نام: {document.file_name}\n"
                    f"📊 حجم: {self._format_size(file_size)}\n\n"
                    "🔄 **پردازش فایل در نسخه‌های بعدی فعال خواهد شد.**\n\n"
                    "**قابلیت‌های آینده:**\n"
                    "• استخراج متن\n"
                    "• خلاصه‌سازی\n"
                    "• تولید سوالات",
                    reply_markup=MainKeyboard.get_main_menu(),
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"📁 فایل {document.file_name} دریافت شد.\n\n"
                    f"⚠️ فرمت‌های پشتیبانی شده: {', '.join(supported_types)}",
                    reply_markup=MainKeyboard.get_main_menu()
                )
                
        except Exception as e:
            logger.error(f"خطا در process_document: {e}")
            await update.message.reply_text(
                "❌ خطا در پردازش فایل.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل صوتی"""
        audio = update.message.audio or update.message.voice
        
        try:
            duration = getattr(audio, 'duration', 0)
            file_size = getattr(audio, 'file_size', 0)
            
            await update.message.reply_text(
                f"🎵 **فایل صوتی دریافت شد**\n"
                f"⏱️ مدت: {self._format_duration(duration)}\n"
                f"📊 حجم: {self._format_size(file_size)}\n\n"
                "🔄 **قابلیت‌های در حال توسعه:**\n"
                "• تبدیل صوت به متن (Whisper)\n"
                "• خلاصه‌سازی گفتگو\n"
                "• تولید زیرنویس\n"
                "• تشخیص زبان",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_audio: {e}")
            await update.message.reply_text(
                "❌ خطا در پردازش فایل صوتی.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def process_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل ویدیویی"""
        video = update.message.video
        
        try:
            duration = getattr(video, 'duration', 0)
            file_size = getattr(video, 'file_size', 0)
            width = getattr(video, 'width', 0)
            height = getattr(video, 'height', 0)
            
            await update.message.reply_text(
                f"🎬 **ویدیو دریافت شد**\n"
                f"⏱️ مدت: {self._format_duration(duration)}\n"
                f"📊 حجم: {self._format_size(file_size)}\n"
                f"📐 رزولوشن: {width}×{height}\n\n"
                "🔄 **قابلیت‌های در حال توسعه:**\n"
                "• فشرده‌سازی ویدیو\n"
                "• تبدیل فرمت\n"
                "• استخراج صدا\n"
                "• تولید thumbnail",
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"خطا در process_video: {e}")
            await update.message.reply_text(
                "❌ خطا در پردازش ویدیو.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    def _parse_video_info(self, text: str):
        """استخراج اطلاعات ویدیو از متن"""
        lines = text.strip().split('\n')
        topic = "موضوع نامشخص"
        duration = 60
        platform = "instagram"
        
        for line in lines:
            line = line.lower()
            if 'موضوع' in line:
                topic = line.split(':', 1)[1].strip()
            elif 'مدت' in line or 'زمان' in line:
                try:
                    duration = int(''.join(filter(str.isdigit, line)))
                except:
                    duration = 60
            elif 'پلتفرم' in line:
                platform = line.split(':', 1)[1].strip()
        
        return topic, duration, platform
    
    def _format_size(self, size_bytes: int) -> str:
        """فرمت حجم فایل"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def _format_duration(self, duration: int) -> str:
        """فرمت مدت زمان"""
        if duration < 60:
            return f"{duration} ثانیه"
        elif duration < 3600:
            minutes = duration // 60
            seconds = duration % 60
            return f"{minutes}:{seconds:02d} دقیقه"
        else:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            return f"{hours}:{minutes:02d} ساعت"
    
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
