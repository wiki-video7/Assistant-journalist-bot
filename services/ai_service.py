# services/ai_service.py - اصلاح شده

import openai
import google.generativeai as genai
from core.config import config
import logging
import asyncio

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # تنظیم OpenAI
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
            
        # تنظیم Gemini
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
    
    async def generate_headlines(self, news_text: str) -> str:
        """تولید تیتر و لید خبری"""
        prompt = f"""
شما یک خبرنگار حرفه‌ای هستید. برای متن زیر، دقیقاً 3 جفت تیتر و لید تولید کنید:

قوانین:
- هر تیتر حداکثر 7 کلمه
- بدون نام افراد در تیتر
- لید باید خلاصه مهم‌ترین نکات باشد

متن خبری:
{news_text}

فرمت خروجی:

**تیتر و لید یک:**
تیتر: [تیتر اول]
لید: [لید اول]

**تیتر و لید دو:**
تیتر: [تیتر دوم]  
لید: [لید دوم]

**تیتر و لید سه:**
تیتر: [تیتر سوم]
لید: [لید سوم]
        """
        
        return await self._call_ai(prompt)
    
    async def generate_video_script(self, topic: str, duration: int = 60, platform: str = "instagram") -> str:
        """تولید اسکریپت ویدیو"""
        prompt = f"""
برای موضوع "{topic}" اسکریپت ویدیو {duration} ثانیه‌ای برای پلتفرم {platform} بنویس.

ساختار:
- 0-3 ثانیه: قلاب جذاب
- 3-15 ثانیه: معرفی موضوع
- 15-45 ثانیه: محتوای اصلی
- 45-60 ثانیه: جمع‌بندی و CTA

شامل:
- متن راوی دقیق
- توصیف صحنه‌ها
- پیشنهاد موسیقی
- نکات فنی
        """
        
        return await self._call_ai(prompt)
    
    async def fact_check(self, claim: str) -> str:
        """راستی‌آزمایی ادعا"""
        prompt = f"""
ادعای زیر را راستی‌آزمایی کن:

"{claim}"

گزارش شامل:
- وضعیت: ✅ درست / ❌ نادرست / ⚠️ مختلط / ❓ نامعلوم
- درجه اطمینان: %
- دلایل کلیدی
- منابع احتمالی برای بررسی بیشتر
- نکته‌های مهم

به زبان ساده و روان پاسخ بده.
        """
        
        return await self._call_ai(prompt)
    
    async def create_prompt(self, requirements: str, complexity: str = "standard") -> str:
        """تولید پرامپت سفارشی"""
        prompt = f"""
نیازمندی‌ها: {requirements}
سطح: {complexity}

یک پرامپت سیستم حرفه‌ای طراحی کن که شامل:

1. **نقش و هویت**
2. **قوانین کلیدی**  
3. **سبک کار**
4. **فرمت خروجی**
5. **مثال‌های عملی**

پرامپت باید آماده استفاده و موثر باشد.
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
        """تماس با سرویس AI"""
        try:
            # اولویت با OpenAI
            if config.OPENAI_API_KEY:
                return await self._call_openai(prompt)
            elif config.GEMINI_API_KEY:
                return await self._call_gemini(prompt)
            else:
                return "⚠️ هیچ سرویس AI فعال نیست. لطفاً API Key را در تنظیمات قرار دهید."
                
        except Exception as e:
            logger.error(f"خطا در AI service: {e}")
            return "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
    
    async def _call_openai(self, prompt: str) -> str:
        """تماس با OpenAI"""
        try:
            # استفاده از روش sync با wrapper
            def _sync_call():
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            # اجرای async
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, _sync_call)
            return result
            
        except Exception as e:
            logger.error(f"خطا در OpenAI: {e}")
            # fallback به Gemini
            if config.GEMINI_API_KEY:
                return await self._call_gemini(prompt)
            raise
    
    async def _call_gemini(self, prompt: str) -> str:
        """تماس با Gemini"""
        try:
            def _sync_call():
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, _sync_call)
            return result
            
        except Exception as e:
            logger.error(f"خطا در Gemini: {e}")
            raise

# نمونه سراسری
ai_service = AIService()
