# services/ai_service.py - اصلاح‌شده

from openai import OpenAI
import google.generativeai as genai
from core.config import config
import asyncio
import logging

logger = logging.getLogger(__name__)

class AIService:
    """سرویس AI با تماس‌های صحیح"""
    
    def __init__(self):
        # تنظیم سرویس‌ها
        self.openai_client = None
        if config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
    
    async def generate_headlines(self, news_text: str) -> str:
        """تولید تیتر و لید خبری"""
        prompt = f"""
تو یک خبرنگار حرفه‌ای هستی. برای متن زیر، 3 جفت تیتر و لید بنویس:

قوانین:
- هر تیتر حداکثر 7 کلمه
- بدون نام افراد در تیتر
- لید کوتاه و جذاب

متن: {news_text}

فرمت:
**تیتر ۱:** [تیتر]
**لید ۱:** [لید]

**تیتر ۲:** [تیتر]  
**لید ۲:** [لید]

**تیتر ۳:** [تیتر]
**لید ۳:** [لید]
        """
        return await self._call_ai(prompt)
    
    async def generate_video_script(self, topic: str, duration: int = 60, platform: str = "instagram") -> str:
        """تولید اسکریپت ویدیو"""
        prompt = f"""
اسکریپت ویدیو {duration} ثانیه‌ای برای {platform} بنویس:

موضوع: {topic}

ساختار:
- ۰-۳ ثانیه: قلاب جذاب
- ۳-۱۵ ثانیه: معرفی
- ۱۵-۴۵ ثانیه: محتوا
- ۴۵-۶۰ ثانیه: نتیجه‌گیری

شامل: متن راوی، توصیف تصاویر، نکات فنی
        """
        return await self._call_ai(prompt)
    
    async def fact_check(self, claim: str) -> str:
        """راستی‌آزمایی"""
        prompt = f"""
این ادعا را بررسی کن: "{claim}"

گزارش شامل:
- وضعیت: ✅ درست / ❌ نادرست / ⚠️ مشکوک / ❓ نامعلوم
- درجه اطمینان: %
- دلیل
- توصیه برای بررسی بیشتر

پاسخ کوتاه و واضح بده.
        """
        return await self._call_ai(prompt)
    
    async def create_prompt(self, requirements: str) -> str:
        """تولید پرامپت"""
        prompt = f"""
نیازمندی: {requirements}

یک پرامپت حرفه‌ای بنویس که شامل:
1. نقش AI
2. قوانین کلیدی
3. سبک کار
4. فرمت خروجی

پرامپت باید آماده استفاده باشد.
        """
        return await self._call_ai(prompt)
    
    async def general_ai_chat(self, message: str, context: str = None) -> str:
        """چت عمومی"""
        if context:
            prompt = f"{context}\n\n{message}"
        else:
            prompt = message
        return await self._call_ai(prompt)
    
    async def _call_ai(self, prompt: str) -> str:
        """تماس با AI"""
        try:
            if self.openai_client:
                return await self._openai_call(prompt)
            elif config.GEMINI_API_KEY:
                return await self._gemini_call(prompt)
            else:
                return "⚠️ هیچ سرویس AI فعال نیست"
        except Exception as e:
            logger.error(f"AI Error: {e}")
            return "❌ خطا در AI. دوباره تلاش کنید."
    
    async def _openai_call(self, prompt: str) -> str:
        """تماس با OpenAI - نسخه جدید"""
        def sync_call():
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI Error: {e}")
                raise
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_call)
    
    async def _gemini_call(self, prompt: str) -> str:
        """تماس با Gemini"""
        def sync_call():
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Gemini Error: {e}")
                raise
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_call)

# نمونه global
ai_service = AIService()
