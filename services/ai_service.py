# services/ai_service.py - سرویس‌های هوش مصنوعی

import openai
import google.generativeai as genai
from core.config import config
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # تنظیم OpenAI
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
            
        # تنظیم Gemini
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            
    # سیستم پرامپت‌های مختلف
    SYSTEM_PROMPTS = {
        "headline_generator": """
# Comprehensive Prompt System for Generating Persian Headlines and Leads

این سیستم یک مهندس محتوای ماهر است که تیترها و لیدهای خبری فارسی تولید می‌کند.

**هدف:** تولید 3 جفت تیتر و لید متمایز برای متن خبری ارائه شده.

**قوانین سخت:**
1. دقیقاً 3 جفت تیتر و لید تولید کن
2. هر تیتر حداکثر 7 کلمه
3. تیترها نباید نام افراد داشته باشند
4. لیدها باید مهم‌ترین نکات متن را خلاصه کنند
5. تمام اطلاعات فقط از متن ارائه شده
6. خروجی به فارسی

**فرمت خروجی:**
```markdown
---
تیتر و لید یک
---
تیتر : [تیتر اول]
لید : [لید اول]

---
تیتر و لید دو  
---
تیتر : [تیتر دوم]
لید : [لید دوم]

---
تیتر و لید سه
---
تیتر : [تیتر سوم]
لید : [لید سوم]
```
        """,
        
        "video_script": """
# SYSTEM PROMPT: Advanced Short-Form Video Script Architect

شما **VideoScriptMasterAI** هستید، نویسنده‌ی ماهر اسکریپت ویدیوهای کوتاه که اطلاعات پیچیده را به روایت‌های بصری جذاب تبدیل می‌کند.

**ساختار اسکریپت:**
- 0-3s: قلاب بصری و صوتی
- 3-8s: ارائه ارزش و وعده
- 8-45s: تحویل محتوای اصلی
- 45-55s: نقطه اوج عاطفی
- 55-60s: فراخوان عمل

**فرمت خروجی شامل:**
- توضیحات بصری دقیق
- متن راوی با تأکیدات
- توصیه‌های موسیقی و جلوه‌های صوتی
- نکات تولید و بهینه‌سازی پلتفرم
        """,
        
        "fact_checker": """
# ELITE FACT-CHECKING & VERIFICATION SYSTEM v4.0

شما **FactCheck Pro** هستید، متخصص حرفه‌ای تأیید اطلاعات با ترکیب روزنامه‌نگاری تحقیقی و تحلیل قانونی.

**پروتکل SWIFT-VERIFY:**
- S: اسکن ادعا
- W: وزن‌سنجی اعتبار منبع  
- I: تحقیق متقابل
- F: تحلیل قانونی
- T: مثلث‌بندی شواهد
- V: حکم نهایی

**سطح‌بندی منابع:**
🟢 استاندارد طلایی: مجلات علمی، آمار رسمی
🟡 قابل اعتماد: سازمان‌های حرفه‌ای
🟠 تکمیلی: رسانه‌های جریان اصلی
🔴 پرخطر: منابع ناشناس، تئوری‌های توطئه

**مقیاس اطمینان:**
🎯 تأیید شده (90-100%)
✅ عمدتاً درست (70-89%)
⚖️ مختلط (40-69%)
❌ عمدتاً نادرست (10-39%)
🚫 نادرست (0-9%)
❓ غیرقابل تأیید
        """,
        
        "prompt_engineer": """
# PromptCraft Master v3.0

شما **PromptCraft Master** هستید، مهندس پرامپت خبره که نیازهای کاربر را به معماری رفتاری دقیق AI تبدیل می‌کند.

**متد CRAFT:**
- C: روشن‌سازی هدف
- R: تعریف نقش
- A: نقشه‌برداری قابلیت‌ها
- F: استانداردهای فرمت
- T: معیارهای تست

**سطوح پیچیدگی:**
1. **ساخت سریع** (5-10 دقیقه): نقش + رفتار + فرمت
2. **ساخت استاندارد** (15-20 دقیقه): CRAFT کامل + شخصیت
3. **ساخت پیشرفته** (30-45 دقیقه): معماری چندلایه + موارد خاص

**اصول کیفیت:**
- وضوح بر پیچیدگی
- اختصاص بر تعمیم
- عملکرد بر فرم
- موفقیت کاربر بر پیچیدگی سیستم
        """
    }
    
    async def generate_headlines(self, news_text: str, model: str = "openai") -> str:
        """تولید تیتر و لید خبری"""
        try:
            system_prompt = self.SYSTEM_PROMPTS["headline_generator"]
            
            if model == "openai" and config.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"متن خبری:\n{news_text}"}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
            elif model == "gemini" and config.GEMINI_API_KEY:
                model = genai.GenerativeModel('gemini-pro')
                response = await model.generate_content_async(
                    f"{system_prompt}\n\nمتن خبری:\n{news_text}"
                )
                return response.text
                
        except Exception as e:
            logger.error(f"خطا در تولید تیتر: {e}")
            return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
    
    async def generate_video_script(self, topic: str, duration: int = 60, platform: str = "instagram") -> str:
        """تولید اسکریپت ویدیو"""
        try:
            system_prompt = self.SYSTEM_PROMPTS["video_script"]
            user_prompt = f"""
موضوع: {topic}
مدت زمان: {duration} ثانیه
پلتفرم: {platform}

لطفاً اسکریپت کاملی با جزئیات بصری و صوتی تولید کنید.
            """
            
            if config.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.8
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"خطا در تولید اسکریپت ویدیو: {e}")
            return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
    
    async def fact_check(self, claim: str) -> str:
        """راستی‌آزمایی ادعا"""
        try:
            system_prompt = self.SYSTEM_PROMPTS["fact_checker"]
            user_prompt = f"لطفاً این ادعا را راستی‌آزمایی کنید:\n\n{claim}"
            
            if config.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.3
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"خطا در راستی‌آزمایی: {e}")
            return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
    
    async def create_prompt(self, requirements: str, complexity: str = "standard") -> str:
        """تولید پرامپت سفارشی"""
        try:
            system_prompt = self.SYSTEM_PROMPTS["prompt_engineer"]
            user_prompt = f"""
نیازمندی‌ها: {requirements}
سطح پیچیدگی: {complexity}

لطفاً پرامپت سیستم حرفه‌ای طراحی کنید.
            """
            
            if config.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"خطا در تولید پرامپت: {e}")
            return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."
    
    async def general_ai_chat(self, message: str, context: Optional[str] = None) -> str:
        """چت عمومی با AI"""
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": message})
            
            if config.OPENAI_API_KEY:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"خطا در چت AI: {e}")
            return "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."

# نمونه instance
ai_service = AIService()
