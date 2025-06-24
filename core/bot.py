# core/bot.py - هسته اصلی ربات

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from core.config import config
from utils.keyboards import MainKeyboard
from handlers.news_handlers import NewsHandler
from handlers.media_handlers import MediaHandler
from handlers.ai_handlers import AIHandler

logger = logging.getLogger(__name__)

class JournalistBot:
    def __init__(self):
        self.app = Application.builder().token(config.BOT_TOKEN).build()
        
        # ایجاد handlers
        self.news_handler = NewsHandler()
        self.media_handler = MediaHandler()
        self.ai_handler = AIHandler()
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """تنظیم handlers ربات"""
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("menu", self.menu_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, self.handle_audio))
        self.app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور شروع"""
        user = update.effective_user
        welcome_text = f"""
🤖 **سلام {user.first_name}!**

به ربات **Assistant Journalist Bot** خوش آمدید!

🎯 **ویژگی‌های من:**
📰 تولید تیتر و لید خبری
🔍 راستی‌آزمایی اطلاعات  
🎬 تولید اسکریپت ویدیو
🤖 مهندسی پرامپت
💬 طراحی چت‌بات

برای شروع از منوی زیر استفاده کنید:
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش منوی اصلی"""
        await update.message.reply_text(
            "📋 **منوی اصلی:**",
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """راهنمای استفاده"""
        help_text = """
📚 **راهنمای استفاده:**

**دستورات:**
/start - شروع ربات
/menu - نمایش منو
/help - راهنما

**بخش‌های اصلی:**
📰 **تولید محتوا**: تیتر، لید، مصاحبه
🔍 **تحقیق**: راستی‌آزمایی، جستجو
🎬 **رسانه**: اسکریپت ویدیو، پادکست
⚙️ **AI**: مهندسی پرامپت، چت‌بات

**نحوه استفاده:**
1. روی گزینه مورد نظر کلیک کنید
2. متن یا درخواست خود را ارسال کنید
3. نتیجه را دریافت کنید

⚡ **نکته**: برای بهترین نتیجه، متن‌های واضح و مفصل ارسال کنید.
        """
        
        await update.message.reply_text(
            help_text,
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت callback queries"""
        query = update.callback_query
        data = query.data
        
        try:
            # منوی اصلی
            if data == "main_menu":
                await query.edit_message_text(
                    "📋 **منوی اصلی:**",
                    reply_markup=MainKeyboard.get_main_menu(),
                    parse_mode='Markdown'
                )
            
            # بخش تولید محتوا
            elif data in ["show_content_menu", "news_write", "news_summary", "news_factcheck", "news_interview", "news_press"]:
                await self.news_handler.handle_news(update, context)
            
            # بخش رسانه
            elif data in ["show_media_menu", "media_video_script", "media_podcast", "media_social", "media_compress"]:
                await self.media_handler.handle_media(update, context)
            
            # بخش AI
            elif data in ["show_ai_menu", "ai_prompt_engineer", "ai_text_to_image", "ai_chatbot", "ai_templates"]:
                await self.ai_handler.handle_ai(update, context)
            
            # راهنما و درباره ما
            elif data == "show_help":
                await self.help_command(update, context)
            elif data == "show_about":
                await self.show_about(update, context)
            
            else:
                await query.answer("این گزینه هنوز پیاده‌سازی نشده است.")
                
        except Exception as e:
            logger.error(f"خطا در handle_callback: {e}")
            await query.answer("خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های متنی"""
        text = update.message.text
        user_state = context.user_data.get('state', 'idle')
        
        # بررسی وضعیت کاربر و هدایت به handler مناسب
        if user_state == 'waiting_for_news_topic':
            await self.news_handler.process_news_topic(update, context, text)
        elif user_state == 'waiting_for_article_text':
            await self.news_handler.process_article_summary(update, context, text)
        elif user_state == 'waiting_for_fact_check':
            await self.news_handler.process_fact_check(update, context, text)
        elif user_state == 'waiting_for_interview_topic':
            await self.news_handler.process_interview_questions(update, context, text)
        elif user_state == 'waiting_for_press_release':
            await self.news_handler.process_press_release(update, context, text)
        elif user_state == 'waiting_for_video_topic':
            await self.media_handler.process_video_script(update, context, text)
        elif user_state == 'waiting_for_podcast_topic':
            await self.media_handler.process_podcast_script(update, context, text)
        elif user_state == 'waiting_for_social_content':
            await self.media_handler.process_social_content(update, context, text)
        elif user_state == 'waiting_for_prompt_requirements':
            await self.ai_handler.process_prompt_requirements(update, context, text)
        elif user_state == 'waiting_for_image_description':
            await self.ai_handler.process_image_description(update, context, text)
        elif user_state == 'waiting_for_chatbot_specs':
            await self.ai_handler.process_chatbot_specs(update, context, text)
        else:
            # پیام عمومی
            await update.message.reply_text(
                "لطفاً از منوی ربات استفاده کنید یا /menu تایپ کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های ارسالی"""
        await self.media_handler.process_document(update, context)
    
    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های صوتی"""
        await self.media_handler.process_audio(update, context)
    
    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های ویدیویی"""
        await self.media_handler.process_video(update, context)
    
    async def show_about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """درباره ربات"""
        about_text = """
🤖 **Assistant Journalist Bot v1.0**

**توسعه‌دهنده:** تیم توسعه AI
**تاریخ انتشار:** 2025
**نسخه:** 1.0.0

**تکنولوژی‌های استفاده شده:**
• Python & python-telegram-bot
• OpenAI GPT & Google Gemini
• Advanced Prompt Engineering
• FFmpeg & OpenCV

**ویژگی‌های کلیدی:**
✅ سیستم پرامپت‌های حرفه‌ای
✅ راستی‌آزمایی با پروتکل SWIFT-VERIFY
✅ تولید اسکریپت بهینه‌شده
✅ رابط کاربری فارسی

🔗 **پشتیبانی:** @your_support_username
        """
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                about_text,
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                about_text,
                reply_markup=MainKeyboard.get_main_menu(),
                parse_mode='Markdown'
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت خطاها"""
        logger.error(f"خطای ربات: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    def run(self):
        """اجرای ربات"""
        print("🚀 ربات در حال اجراست...")
        logger.info("ربات Assistant Journalist Bot آغاز شد")
        
        try:
            self.app.run_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"خطا در اجرای ربات: {e}")
            raise
