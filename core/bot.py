# bot.py - هسته اصلی ربات

import asyncio
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from core.config import Config
from handlers.main_menu import MainMenuHandler
from handlers.news_handlers import NewsHandler
from handlers.media_handlers import MediaHandler
from handlers.ai_handlers import AIHandler
from utils.keyboards import MainKeyboard

# تنظیم لاگ
logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
)
logger = logging.getLogger(__name__)

class JournalistBot:
   def __init__(self):
       self.config = Config()
       self.app = Application.builder().token(self.config.BOT_TOKEN).build()
       
       # هندلرها
       self.main_menu = MainMenuHandler()
       self.news_handler = NewsHandler()
       self.media_handler = MediaHandler()
       self.ai_handler = AIHandler()
       
   def setup_handlers(self):
       """تنظیم هندلرهای ربات"""
       
       # دستورات اصلی
       self.app.add_handler(CommandHandler("start", self.start_command))
       self.app.add_handler(CommandHandler("help", self.help_command))
       self.app.add_handler(CommandHandler("menu", self.menu_command))
       
       # هندلرهای callback query
       self.app.add_handler(CallbackQueryHandler(self.main_menu.handle_main_menu, pattern="^main_"))
       self.app.add_handler(CallbackQueryHandler(self.news_handler.handle_news, pattern="^news_"))
       self.app.add_handler(CallbackQueryHandler(self.media_handler.handle_media, pattern="^media_"))
       self.app.add_handler(CallbackQueryHandler(self.ai_handler.handle_ai, pattern="^ai_"))
       
       # هندلر پیام‌های متنی
       self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
       
       # هندلر فایل‌ها
       self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
       self.app.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
       self.app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
       
   async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """دستور شروع"""
       user = update.effective_user
       
       welcome_text = f"""
🏠 سلام {user.first_name}!

به ربات دستیار خبرنگار خوش آمدید 📰

این ربات می‌تواند شما را در موارد زیر یاری دهد:
- تولید محتوای خبری 📝
- تحقیق و راستی‌آزمایی 🔍
- تولید محتوای رسانه‌ای 🎬
- ابزارهای هوشمند AI 🤖

برای شروع، روی دکمه منو کلیک کنید یا /menu تایپ کنید.
       """
       
       keyboard = MainKeyboard.get_main_menu()
       await update.message.reply_text(welcome_text, reply_markup=keyboard)
       
   async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """دستور راهنما"""
       help_text = """
📚 راهنمای استفاده از ربات:

🏠 /start - شروع کار با ربات
📋 /menu - نمایش منوی اصلی
❓ /help - نمایش این راهنما

📰 بخش تولید محتوا:
- نگارش خبر با ساختار استاندارد
- خلاصه‌سازی مقالات طولانی
- تولید سوالات مصاحبه

🔍 بخش تحقیق:
- جستجوی اخبار از منابع معتبر
- راستی‌آزمایی اطلاعات
- تحلیل روندهای خبری

🎬 بخش رسانه:
- نگارش اسکریپت ویدیو
- تولید محتوای شبکه‌های اجتماعی
- پردازش فایل‌های صوتی و تصویری

پشتیبانی: @support_bot
       """
       await update.message.reply_text(help_text)
       
   async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """نمایش منوی اصلی"""
       keyboard = MainKeyboard.get_main_menu()
       await update.message.reply_text("📋 منوی اصلی:", reply_markup=keyboard)
       
   async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """پردازش پیام‌های متنی"""
       text = update.message.text
       user_id = update.effective_user.id
       
       # بررسی وضعیت کاربر
       user_state = context.user_data.get('state', 'idle')
       
       if user_state == 'waiting_for_news_topic':
           await self.news_handler.process_news_topic(update, context, text)
       elif user_state == 'waiting_for_article_text':
           await self.news_handler.process_article_summary(update, context, text)
       elif user_state == 'waiting_for_fact_check':
           await self.news_handler.process_fact_check(update, context, text)
       else:
           # پیام عمومی
           await update.message.reply_text(
               "لطفاً از منوی ربات استفاده کنید یا /menu تایپ کنید.",
               reply_markup=MainKeyboard.get_main_menu()
           )
           
   async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """پردازش فایل‌های اسناد"""
       await self.media_handler.process_document(update, context)
       
   async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """پردازش فایل‌های صوتی"""
       await self.media_handler.process_audio(update, context)
       
   async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """پردازش فایل‌های ویدیویی"""
       await self.media_handler.process_video(update, context)
       
   async def set_bot_commands(self):
       """تنظیم دستورات ربات"""
       commands = [
           BotCommand("start", "شروع کار با ربات"),
           BotCommand("menu", "نمایش منوی اصلی"),
           BotCommand("help", "راهنمای استفاده"),
       ]
       await self.app.bot.set_my_commands(commands)
       
   async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       """مدیریت خطاها"""
       logger.error(f"Update {update} caused error {context.error}")
       
       if update and update.effective_message:
           await update.effective_message.reply_text(
               "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید."
           )
           
   def run(self):
       """اجرای ربات"""
       logger.info("شروع ربات دستیار خبرنگار...")
       
       # تنظیم هندلرها
       self.setup_handlers()
       
       # تنظیم error handler
       self.app.add_error_handler(self.error_handler)
       
       # تنظیم دستورات ربات
       asyncio.create_task(self.set_bot_commands())
       
       # اجرای ربات
       logger.info("ربات آماده است!")
       self.app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
   bot = JournalistBot()
   bot.run()
