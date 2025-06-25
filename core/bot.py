# core/bot.py - نسخه بهبود یافته با Rate Limiting، Metrics و Logging پیشرفته

import logging
import time
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, NetworkError, TimedOut

from core.config import config
from utils.keyboards import MainKeyboard
from handlers.news_handlers import NewsHandler
from handlers.media_handlers import MediaHandler
from handlers.ai_handlers import AIHandler

# تنظیم logging پیشرفته
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class UserMetrics:
    """متریک‌های کاربر"""
    user_id: int
    username: str = ""
    first_seen: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    total_messages: int = 0
    total_commands: int = 0
    total_callbacks: int = 0
    ai_requests: int = 0
    error_count: int = 0
    session_start: datetime = field(default_factory=datetime.now)

@dataclass
class BotMetrics:
    """متریک‌های کلی ربات"""
    start_time: datetime = field(default_factory=datetime.now)
    total_users: int = 0
    active_users_today: int = 0
    total_messages: int = 0
    total_ai_requests: int = 0
    total_errors: int = 0
    avg_response_time: float = 0.0
    popular_features: Dict[str, int] = field(default_factory=dict)

class RateLimiter:
    """سیستم محدودیت نرخ درخواست"""
    
    def __init__(self, max_requests: int = 30, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests: Dict[int, deque] = defaultdict(deque)
        logger.info(f"Rate limiter initialized: {max_requests} requests per {time_window} seconds")
    
    def is_allowed(self, user_id: int) -> tuple[bool, Optional[int]]:
        """بررسی مجاز بودن درخواست"""
        now = time.time()
        user_queue = self.user_requests[user_id]
        
        # حذف درخواست‌های قدیمی
        while user_queue and user_queue[0] < now - self.time_window:
            user_queue.popleft()
        
        # بررسی محدودیت
        if len(user_queue) >= self.max_requests:
            wait_time = int(user_queue[0] + self.time_window - now)
            logger.warning(f"Rate limit exceeded for user {user_id}. Wait time: {wait_time}s")
            return False, wait_time
        
        # اضافه کردن درخواست جدید
        user_queue.append(now)
        return True, None
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """دریافت آمار کاربر"""
        user_queue = self.user_requests[user_id]
        now = time.time()
        
        # فیلتر درخواست‌های فعال
        active_requests = [req for req in user_queue if req > now - self.time_window]
        
        return {
            "active_requests": len(active_requests),
            "max_requests": self.max_requests,
            "time_window": self.time_window,
            "remaining": max(0, self.max_requests - len(active_requests))
        }

class MetricsCollector:
    """جمع‌آوری و مدیریت متریک‌ها"""
    
    def __init__(self):
        self.bot_metrics = BotMetrics()
        self.user_metrics: Dict[int, UserMetrics] = {}
        self.performance_log: deque = deque(maxlen=1000)  # نگه‌داری 1000 آخرین عملیات
        logger.info("Metrics collector initialized")
    
    def track_user_activity(self, user_id: int, username: str = "", activity_type: str = "message"):
        """ردیابی فعالیت کاربر"""
        if user_id not in self.user_metrics:
            self.user_metrics[user_id] = UserMetrics(user_id=user_id, username=username)
            self.bot_metrics.total_users += 1
            logger.info(f"New user registered: {user_id} (@{username})")
        
        user_metric = self.user_metrics[user_id]
        user_metric.last_activity = datetime.now()
        user_metric.username = username or user_metric.username
        
        if activity_type == "message":
            user_metric.total_messages += 1
            self.bot_metrics.total_messages += 1
        elif activity_type == "command":
            user_metric.total_commands += 1
        elif activity_type == "callback":
            user_metric.total_callbacks += 1
        elif activity_type == "ai_request":
            user_metric.ai_requests += 1
            self.bot_metrics.total_ai_requests += 1
    
    def track_feature_usage(self, feature: str):
        """ردیابی استفاده از ویژگی‌ها"""
        if feature not in self.bot_metrics.popular_features:
            self.bot_metrics.popular_features[feature] = 0
        self.bot_metrics.popular_features[feature] += 1
    
    def track_error(self, user_id: int, error_type: str, error_msg: str):
        """ردیابی خطاها"""
        if user_id in self.user_metrics:
            self.user_metrics[user_id].error_count += 1
        self.bot_metrics.total_errors += 1
        
        logger.error(f"Error tracked - User: {user_id}, Type: {error_type}, Message: {error_msg}")
    
    def track_performance(self, operation: str, duration: float, success: bool = True):
        """ردیابی عملکرد"""
        self.performance_log.append({
            'timestamp': datetime.now(),
            'operation': operation,
            'duration': duration,
            'success': success
        })
        
        # محاسبه میانگین زمان پاسخ
        recent_operations = [p for p in self.performance_log if p['success']]
        if recent_operations:
            total_time = sum(p['duration'] for p in recent_operations)
            self.bot_metrics.avg_response_time = total_time / len(recent_operations)
    
    def get_daily_active_users(self) -> int:
        """محاسبه کاربران فعال روزانه"""
        today = datetime.now().date()
        active_count = 0
        
        for user_metric in self.user_metrics.values():
            if user_metric.last_activity.date() == today:
                active_count += 1
        
        self.bot_metrics.active_users_today = active_count
        return active_count
    
    def get_bot_stats(self) -> Dict[str, Any]:
        """دریافت آمار کلی ربات"""
        uptime = datetime.now() - self.bot_metrics.start_time
        daily_active = self.get_daily_active_users()
        
        return {
            "uptime_hours": round(uptime.total_seconds() / 3600, 2),
            "total_users": self.bot_metrics.total_users,
            "active_users_today": daily_active,
            "total_messages": self.bot_metrics.total_messages,
            "total_ai_requests": self.bot_metrics.total_ai_requests,
            "total_errors": self.bot_metrics.total_errors,
            "avg_response_time": round(self.bot_metrics.avg_response_time, 3),
            "popular_features": dict(sorted(
                self.bot_metrics.popular_features.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10])
        }
    
    def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """دریافت آمار کاربر خاص"""
        if user_id not in self.user_metrics:
            return None
        
        user_metric = self.user_metrics[user_id]
        session_duration = datetime.now() - user_metric.session_start
        
        return {
            "user_id": user_id,
            "username": user_metric.username,
            "first_seen": user_metric.first_seen.strftime("%Y-%m-%d %H:%M"),
            "last_activity": user_metric.last_activity.strftime("%Y-%m-%d %H:%M"),
            "session_duration_minutes": round(session_duration.total_seconds() / 60, 2),
            "total_messages": user_metric.total_messages,
            "total_commands": user_metric.total_commands,
            "ai_requests": user_metric.ai_requests,
            "error_count": user_metric.error_count
        }

class JournalistBot:
    """ربات خبرنگار پیشرفته با قابلیت‌های کامل"""
    
    def __init__(self):
        # اجزای اصلی
        self.app = Application.builder().token(config.BOT_TOKEN).build()
        
        # سیستم‌های پیشرفته
        self.rate_limiter = RateLimiter(
            max_requests=config.FREE_DAILY_LIMIT if not config.ADMIN_IDS else 100,
            time_window=60
        )
        self.metrics = MetricsCollector()
        
        # Handlers
        self.news_handler = NewsHandler()
        self.media_handler = MediaHandler()
        self.ai_handler = AIHandler()
        
        # آمار عملکرد
        self.start_time = time.time()
        
        self._setup_handlers()
        logger.info("JournalistBot initialized successfully")
    
    def _setup_handlers(self):
        """تنظیم handlers ربات"""
        logger.info("Setting up bot handlers...")
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("menu", self.menu_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("mystats", self.user_stats_command))
        
        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, self.handle_audio))
        self.app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
        
        logger.info("All handlers configured successfully")
    
    async def _check_rate_limit(self, update: Update) -> bool:
        """بررسی محدودیت نرخ درخواست"""
        user_id = update.effective_user.id
        allowed, wait_time = self.rate_limiter.is_allowed(user_id)
        
        if not allowed:
            rate_stats = self.rate_limiter.get_user_stats(user_id)
            await update.effective_message.reply_text(
                f"⚠️ **محدودیت درخواست**\n\n"
                f"شما بیش از حد مجاز درخواست ارسال کرده‌اید.\n\n"
                f"📊 **وضعیت شما:**\n"
                f"• درخواست‌های فعال: {rate_stats['active_requests']}/{rate_stats['max_requests']}\n"
                f"• زمان انتظار: {wait_time} ثانیه\n"
                f"• بازنشانی هر: {rate_stats['time_window']} ثانیه\n\n"
                f"💡 **نکته:** لطفاً کمی صبر کنید و سپس دوباره تلاش کنید.",
                parse_mode='Markdown'
            )
            return False
        return True
    
    async def _track_operation(self, operation_name: str, func, *args, **kwargs):
        """ردیابی عملیات با اندازه‌گیری زمان"""
        start_time = time.time()
        success = True
        result = None
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
        except Exception as e:
            success = False
            logger.error(f"Operation {operation_name} failed: {e}")
            raise
        finally:
            duration = time.time() - start_time
            self.metrics.track_performance(operation_name, duration, success)
            
            if duration > 5.0:  # هشدار برای عملیات‌های طولانی
                logger.warning(f"Slow operation detected: {operation_name} took {duration:.2f}s")
        
        return result
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور شروع با ردیابی کامل"""
        user = update.effective_user
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        # ردیابی فعالیت
        self.metrics.track_user_activity(user.id, user.username, "command")
        self.metrics.track_feature_usage("start_command")
        
        welcome_text = f"""
🤖 **سلام {user.first_name}!**

به ربات **Assistant Journalist Bot** خوش آمدید!

🎯 **ویژگی‌های من:**
📰 تولید تیتر و لید خبری
🔍 راستی‌آزمایی اطلاعات  
🎬 تولید اسکریپت ویدیو
🤖 مهندسی پرامپت
💬 طراحی چت‌بات

📊 **آمار شما:**
• این بازدید شماره {self.metrics.user_metrics.get(user.id, UserMetrics(user.id)).total_commands + 1} شماست
• کاربر شماره {self.metrics.bot_metrics.total_users} ما هستید

برای شروع از منوی زیر استفاده کنید:
        """
        
        await self._track_operation(
            "start_command_response",
            update.message.reply_text,
            welcome_text,
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
        
        logger.info(f"Start command executed for user {user.id} (@{user.username})")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش آمار ربات (فقط برای ادمین‌ها)"""
        user_id = update.effective_user.id
        
        if not config.is_admin(user_id):
            await update.message.reply_text("❌ این دستور فقط برای مدیران در دسترس است.")
            return
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        stats = self.metrics.get_bot_stats()
        
        stats_text = f"""
📊 **آمار کلی ربات**

⏱️ **زمان فعالیت:** {stats['uptime_hours']} ساعت
👥 **کل کاربران:** {stats['total_users']}
🟢 **کاربران فعال امروز:** {stats['active_users_today']}
💬 **کل پیام‌ها:** {stats['total_messages']}
🤖 **درخواست‌های AI:** {stats['total_ai_requests']}
❌ **کل خطاها:** {stats['total_errors']}
⚡ **میانگین زمان پاسخ:** {stats['avg_response_time']}s

🔥 **محبوب‌ترین ویژگی‌ها:**
"""
        
        for feature, count in list(stats['popular_features'].items())[:5]:
            stats_text += f"• {feature}: {count} بار\n"
        
        await self._track_operation(
            "stats_command_response",
            update.message.reply_text,
            stats_text,
            parse_mode='Markdown'
        )
        
        logger.info(f"Stats command executed by admin {user_id}")
    
    async def user_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش آمار شخصی کاربر"""
        user_id = update.effective_user.id
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        user_stats = self.metrics.get_user_stats(user_id)
        rate_stats = self.rate_limiter.get_user_stats(user_id)
        
        if not user_stats:
            await update.message.reply_text("❌ آمار شما در دسترس نیست.")
            return
        
        stats_text = f"""
📊 **آمار شخصی شما**

👤 **اطلاعات کلی:**
• نام کاربری: @{user_stats.get('username', 'نامشخص')}
• اولین بازدید: {user_stats['first_seen']}
• آخرین فعالیت: {user_stats['last_activity']}
• مدت جلسه فعلی: {user_stats['session_duration_minutes']} دقیقه

📈 **آمار فعالیت:**
• کل پیام‌ها: {user_stats['total_messages']}
• کل دستورات: {user_stats['total_commands']} 
• درخواست‌های AI: {user_stats['ai_requests']}
• تعداد خطا: {user_stats['error_count']}

⚡ **وضعیت محدودیت:**
• درخواست‌های باقی‌مانده: {rate_stats['remaining']}/{rate_stats['max_requests']}
• بازنشانی هر {rate_stats['time_window']} ثانیه
        """
        
        await self._track_operation(
            "user_stats_response",
            update.message.reply_text,
            stats_text,
            parse_mode='Markdown'
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش منوی اصلی"""
        if not await self._check_rate_limit(update):
            return
        
        user_id = update.effective_user.id
        self.metrics.track_user_activity(user_id, update.effective_user.username, "command")
        
        await self._track_operation(
            "menu_command",
            update.message.reply_text,
            "📋 **منوی اصلی:**",
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """راهنمای استفاده"""
        if not await self._check_rate_limit(update):
            return
        
        user_id = update.effective_user.id
        self.metrics.track_user_activity(user_id, update.effective_user.username, "command")
        self.metrics.track_feature_usage("help_command")
        
        help_text = """
📚 **راهنمای استفاده:**

**دستورات اصلی:**
/start - شروع ربات
/menu - نمایش منو
/help - راهنما
/mystats - آمار شخصی شما

**بخش‌های اصلی:**
📰 **تولید محتوا**: تیتر، لید، مصاحبه
🔍 **تحقیق**: راستی‌آزمایی، جستجو
🎬 **رسانه**: اسکریپت ویدیو، پادکست
⚙️ **AI**: مهندسی پرامپت، چت‌بات

**نحوه استفاده:**
1. روی گزینه مورد نظر کلیک کنید
2. متن یا درخواست خود را ارسال کنید
3. نتیجه را دریافت کنید

⚡ **نکات مهم:**
• برای بهترین نتیجه، متن‌های واضح ارسال کنید
• شما {self.rate_limiter.max_requests} درخواست در {self.rate_limiter.time_window} ثانیه حق دارید
• از /mystats برای مشاهده آمار استفاده کنید

🆘 **پشتیبانی:** در صورت بروز مشکل با مدیریت تماس بگیرید.
        """
        
        await self._track_operation(
            "help_command",
            update.message.reply_text,
            help_text,
            reply_markup=MainKeyboard.get_main_menu(),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت callback queries با ردیابی کامل"""
        query = update.callback_query
        user_id = update.effective_user.id
        data = query.data
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        # ردیابی فعالیت
        self.metrics.track_user_activity(user_id, update.effective_user.username, "callback")
        self.metrics.track_feature_usage(f"callback_{data}")
        
        try:
            await query.answer()
            
            # مسیریابی به handlers مناسب
            if data == "main_menu":
                await self._track_operation(
                    "main_menu_callback",
                    query.edit_message_text,
                    "📋 **منوی اصلی:**",
                    reply_markup=MainKeyboard.get_main_menu(),
                    parse_mode='Markdown'
                )
            
            # بخش تولید محتوا
            elif data in ["show_content_menu", "news_write", "news_summary", "news_factcheck", "news_interview", "news_press"]:
                await self._track_operation(
                    f"news_handler_{data}",
                    self.news_handler.handle_news,
                    update, context
                )
            
            # بخش رسانه
            elif data in ["show_media_menu", "media_video_script", "media_podcast", "media_social", "media_compress"]:
                await self._track_operation(
                    f"media_handler_{data}",
                    self.media_handler.handle_media,
                    update, context
                )
            
            # بخش AI
            elif data in ["show_ai_menu", "ai_prompt_engineer", "ai_text_to_image", "ai_chatbot", "ai_templates"]:
                await self._track_operation(
                    f"ai_handler_{data}",
                    self.ai_handler.handle_ai,
                    update, context
                )
            
            # راهنما و درباره ما
            elif data == "show_help":
                await self.help_command(update, context)
            elif data == "show_about":
                await self.show_about(update, context)
            
            else:
                await query.answer("این گزینه هنوز پیاده‌سازی نشده است.")
                logger.warning(f"Unhandled callback data: {data} from user {user_id}")
                
        except Exception as e:
            logger.error(f"خطا در handle_callback: {e} - User: {user_id}, Data: {data}")
            self.metrics.track_error(user_id, "callback_error", str(e))
            await query.answer("خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های متنی"""
        user_id = update.effective_user.id
        text = update.message.text
        user_state = context.user_data.get('state', 'idle')
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        # ردیابی فعالیت
        self.metrics.track_user_activity(user_id, update.effective_user.username, "message")
        
        logger.info(f"Text message from user {user_id}: state={user_state}, length={len(text)}")
        
        try:
            # بررسی وضعیت کاربر و هدایت به handler مناسب
            if user_state == 'waiting_for_news_topic':
                await self._track_operation("news_topic_processing", self.news_handler.process_news_topic, update, context, text)
            elif user_state == 'waiting_for_article_text':
                await self._track_operation("article_summary_processing", self.news_handler.process_article_summary, update, context, text)
            elif user_state == 'waiting_for_fact_check':
                await self._track_operation("fact_check_processing", self.news_handler.process_fact_check, update, context, text)
            elif user_state == 'waiting_for_interview_topic':
                await self._track_operation("interview_processing", self.news_handler.process_interview_questions, update, context, text)
            elif user_state == 'waiting_for_press_release':
                await self._track_operation("press_release_processing", self.news_handler.process_press_release, update, context, text)
            elif user_state == 'waiting_for_video_topic':
                await self._track_operation("video_script_processing", self.media_handler.process_video_script, update, context, text)
            elif user_state == 'waiting_for_podcast_topic':
                await self._track_operation("podcast_script_processing", self.media_handler.process_podcast_script, update, context, text)
            elif user_state == 'waiting_for_social_content':
                await self._track_operation("social_content_processing", self.media_handler.process_social_content, update, context, text)
            elif user_state == 'waiting_for_prompt_requirements':
                await self._track_operation("prompt_engineering_processing", self.ai_handler.process_prompt_requirements, update, context, text)
            elif user_state == 'waiting_for_image_description':
                await self._track_operation("image_prompt_processing", self.ai_handler.process_image_description, update, context, text)
            elif user_state == 'waiting_for_chatbot_specs':
                await self._track_operation("chatbot_design_processing", self.ai_handler.process_chatbot_specs, update, context, text)
            else:
                # پیام عمومی
                self.metrics.track_feature_usage("general_message")
                await update.message.reply_text(
                    "لطفاً از منوی ربات استفاده کنید یا /menu تایپ کنید.\n\n"
                    "💡 **نکته:** برای مشاهده آمار شخصی خود از /mystats استفاده کنید.",
                    reply_markup=MainKeyboard.get_main_menu()
                )
        
        except Exception as e:
            logger.error(f"خطا در handle_text: {e} - User: {user_id}")
            self.metrics.track_error(user_id, "text_processing_error", str(e))
            await update.message.reply_text(
                "❌ متأسفانه خطایی در پردازش پیام شما رخ داد.\n"
                "لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.",
                reply_markup=MainKeyboard.get_main_menu()
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های ارسالی"""
        user_id = update.effective_user.id
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        self.metrics.track_user_activity(user_id, update.effective_user.username, "message")
        self.metrics.track_feature_usage("document_upload")
        
        await self._track_operation(
            "document_processing",
            self.media_handler.process_document,
            update, context
        )
    
    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های صوتی"""
        user_id = update.effective_user.id
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        self.metrics.track_user_activity(user_id, update.effective_user.username, "message")
        self.metrics.track_feature_usage("audio_upload")
        
        await self._track_operation(
            "audio_processing",
            self.media_handler.process_audio,
            update, context
        )
    
    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش فایل‌های ویدیویی"""
        user_id = update.effective_user.id
        
        # بررسی محدودیت نرخ
        if not await self._check_rate_limit(update):
            return
        
        self.metrics.track_user_activity(user_id, update.effective_user.username, "message")
        self.metrics.track_feature_usage("video_upload")
        
        await self._track_operation(
            "video_processing",
            self.media_handler.process_video,
            update, context
        )
    
    async def show_about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """درباره ربات"""
        stats = self.metrics.get_bot_stats()
        
        about_text = f"""
🤖 **Assistant Journalist Bot v1.0**

**توسعه‌دهنده:** تیم توسعه AI
**تاریخ انتشار:** 2025
**نسخه:** 1.0.0

**تکنولوژی‌های استفاده شده:**
• Python & python-telegram-bot
• OpenAI GPT & Google Gemini
• Advanced Prompt Engineering
• Rate Limiting & Metrics
• FFmpeg & OpenCV

**ویژگی‌های کلیدی:**
✅ سیستم پرامپت‌های حرفه‌ای
✅ راستی‌آزمایی با پروتکل SWIFT-VERIFY
✅ تولید اسکریپت بهینه‌شده
✅ رابط کاربری فارسی
✅ مدیریت ترافیک پیشرفته
✅ ردیابی عملکرد real-time

📊 **آمار فعلی:**
• کاربران فعال: {stats['total_users']}
• درخواست‌های پردازش شده: {stats['total_ai_requests']}
• زمان فعالیت: {stats['uptime_hours']} ساعت

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
        """مدیریت خطاها با ردیابی کامل"""
        error = context.error
        user_id = update.effective_user.id if update and update.effective_user else 0
        
        # ردیابی خطا
        self.metrics.track_error(user_id, type(error).__name__, str(error))
        
        logger.error(f"Bot error: {error}", exc_info=context.error)
        
        # تشخیص نوع خطا و پاسخ مناسب
        error_message = "❌ متأسفانه خطایی رخ داد."
        
        if isinstance(error, NetworkError):
            error_message = "🌐 مشکل در اتصال به اینترنت. لطفاً دوباره تلاش کنید."
        elif isinstance(error, TimedOut):
            error_message = "⏱️ زمان درخواست به پایان رسید. لطفاً دوباره تلاش کنید."
        elif isinstance(error, TelegramError):
            error_message = "📱 خطای تلگرام. لطفاً چند لحظه صبر کنید."
        
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    f"{error_message}\n\n"
                    f"🆔 **کد خطا:** {hash(str(error)) % 10000}\n"
                    f"⏰ **زمان:** {datetime.now().strftime('%H:%M:%S')}\n\n"
                    f"💡 اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید.",
                    reply_markup=MainKeyboard.get_main_menu(),
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send error message: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """دریافت وضعیت سلامت ربات"""
        stats = self.metrics.get_bot_stats()
        
        # محاسبه وضعیت سلامت
        health_score = 100
        issues = []
        
        if stats['total_errors'] > 50:
            health_score -= 20
            issues.append("تعداد خطاهای بالا")
        
        if stats['avg_response_time'] > 3.0:
            health_score -= 15
            issues.append("زمان پاسخ بالا")
        
        if len(self.rate_limiter.user_requests) > 1000:
            health_score -= 10
            issues.append("ترافیک بالا")
        
        return {
            "health_score": health_score,
            "status": "healthy" if health_score > 80 else "warning" if health_score > 60 else "critical",
            "issues": issues,
            "uptime_hours": stats['uptime_hours'],
            "total_users": stats['total_users'],
            "active_users_today": stats['active_users_today'],
            "avg_response_time": stats['avg_response_time'],
            "error_rate": stats['total_errors'] / max(stats['total_messages'], 1) * 100
        }
    
    async def periodic_cleanup(self):
        """تمیزکاری دوره‌ای"""
        logger.info("Starting periodic cleanup...")
        
        # تمیز کردن rate limiter
        current_time = time.time()
        cleaned_users = 0
        
        for user_id, requests in list(self.rate_limiter.user_requests.items()):
            # حذف درخواست‌های قدیمی
            while requests and requests[0] < current_time - self.rate_limiter.time_window:
                requests.popleft()
            
            # حذف کاربران غیرفعال
            if not requests:
                del self.rate_limiter.user_requests[user_id]
                cleaned_users += 1
        
        logger.info(f"Cleanup completed: removed {cleaned_users} inactive users from rate limiter")
    
    def run(self):
        """اجرای ربات با قابلیت‌های پیشرفته"""
        print("🚀 ربات در حال اجراست...")
        logger.info("Assistant Journalist Bot started with advanced features")
        
        # نمایش آمار اولیه
        health = self.get_health_status()
        logger.info(f"Bot health status: {health['status']} (score: {health['health_score']})")
        
        try:
            # راه‌اندازی تمیزکاری دوره‌ای
            asyncio.create_task(self._schedule_periodic_tasks())
            
            self.app.run_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True,
                close_loop=False
            )
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Critical error in bot execution: {e}")
            raise
        finally:
            self._log_final_stats()
    
    async def _schedule_periodic_tasks(self):
        """برنامه‌ریزی وظایف دوره‌ای"""
        while True:
            try:
                await asyncio.sleep(300)  # هر 5 دقیقه
                await self.periodic_cleanup()
                
                # لاگ آمار دوره‌ای
                if int(time.time()) % 3600 == 0:  # هر ساعت
                    stats = self.metrics.get_bot_stats()
                    logger.info(f"Hourly stats: {stats['total_users']} users, "
                              f"{stats['total_messages']} messages, "
                              f"{stats['avg_response_time']:.2f}s avg response")
                
            except Exception as e:
                logger.error(f"Error in periodic tasks: {e}")
    
    def _log_final_stats(self):
        """لاگ آمار نهایی"""
        final_stats = self.metrics.get_bot_stats()
        uptime = time.time() - self.start_time
        
        logger.info("=== BOT SHUTDOWN STATISTICS ===")
        logger.info(f"Total uptime: {uptime/3600:.2f} hours")
        logger.info(f"Total users served: {final_stats['total_users']}")
        logger.info(f"Total messages processed: {final_stats['total_messages']}")
        logger.info(f"Total AI requests: {final_stats['total_ai_requests']}")
        logger.info(f"Total errors: {final_stats['total_errors']}")
        logger.info(f"Average response time: {final_stats['avg_response_time']:.3f}s")
        logger.info("=== END STATISTICS ===")
        
        print("👋 ربات با موفقیت متوقف شد")
        print(f"📊 آمار نهایی: {final_stats['total_users']} کاربر، "
              f"{final_stats['total_messages']} پیام، "
              f"{uptime/3600:.1f} ساعت فعالیت")
