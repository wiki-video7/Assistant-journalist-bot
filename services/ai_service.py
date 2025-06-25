# services/ai_service.py - نسخه بهبود یافته با Retry، Caching و Load Balancing

import asyncio
import hashlib
import json
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum

from openai import OpenAI
import google.generativeai as genai
from core.config import config
from data.prompts import get_prompt

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    """نوع ارائه‌دهندگان AI"""
    OPENAI = "openai"
    GEMINI = "gemini"

@dataclass
class CacheEntry:
    """ورودی کش"""
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    hit_count: int = 0
    provider: str = ""
    
    def is_expired(self, ttl_hours: int = 24) -> bool:
        """بررسی انقضای کش"""
        return datetime.now() - self.timestamp > timedelta(hours=ttl_hours)

@dataclass
class ProviderStats:
    """آمار ارائه‌دهنده"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    last_error: Optional[str] = None
    last_success: Optional[datetime] = None
    consecutive_failures: int = 0
    
    @property
    def success_rate(self) -> float:
        """نرخ موفقیت"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def avg_response_time(self) -> float:
        """میانگین زمان پاسخ"""
        if self.successful_requests == 0:
            return 0.0
        return self.total_response_time / self.successful_requests
    
    @property
    def is_healthy(self) -> bool:
        """وضعیت سلامت ارائه‌دهنده"""
        return self.consecutive_failures < 3 and self.success_rate > 50

class IntelligentCache:
    """سیستم کش هوشمند"""
    
    def __init__(self, max_size: int = 1000, ttl_hours: int = 24):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.ttl_hours = ttl_hours
        self.hit_count = 0
        self.miss_count = 0
        logger.info(f"Intelligent cache initialized: max_size={max_size}, ttl={ttl_hours}h")
    
    def _generate_key(self, prompt: str, provider: str = "") -> str:
        """تولید کلید کش"""
        # نرمال‌سازی پرامپت
        normalized = prompt.strip().lower()
        
        # حذف whitespace اضافی
        normalized = ' '.join(normalized.split())
        
        # ایجاد hash
        content = f"{normalized}:{provider}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str, provider: str = "") -> Optional[str]:
        """دریافت از کش"""
        key = self._generate_key(prompt, provider)
        
        if key not in self.cache:
            self.miss_count += 1
            return None
        
        entry = self.cache[key]
        
        # بررسی انقضا
        if entry.is_expired(self.ttl_hours):
            del self.cache[key]
            self.miss_count += 1
            logger.debug(f"Cache entry expired and removed: {key[:8]}...")
            return None
        
        # به‌روزرسانی آمار
        entry.hit_count += 1
        self.hit_count += 1
        
        logger.debug(f"Cache hit: {key[:8]}... (hits: {entry.hit_count})")
        return entry.content
    
    def set(self, prompt: str, content: str, provider: str = ""):
        """ذخیره در کش"""
        key = self._generate_key(prompt, provider)
        
        # مدیریت اندازه کش
        if len(self.cache) >= self.max_size:
            self._evict_lru()
        
        self.cache[key] = CacheEntry(
            content=content,
            provider=provider
        )
        
        logger.debug(f"Cache set: {key[:8]}... (size: {len(self.cache)})")
    
    def _evict_lru(self):
        """حذف کمترین استفاده شده"""
        if not self.cache:
            return
        
        # پیدا کردن کمترین hit_count
        lru_key = min(self.cache.keys(), key=lambda k: self.cache[k].hit_count)
        del self.cache[lru_key]
        logger.debug(f"Cache LRU eviction: {lru_key[:8]}...")
    
    def clear_expired(self):
        """پاک کردن ورودی‌های منقضی"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired(self.ttl_hours)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleared {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """آمار کش"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 2),
            "ttl_hours": self.ttl_hours
        }

class LoadBalancer:
    """تعادل بار بین ارائه‌دهندگان"""
    
    def __init__(self):
        self.providers: Dict[AIProvider, ProviderStats] = {
            AIProvider.OPENAI: ProviderStats(),
            AIProvider.GEMINI: ProviderStats()
        }
        logger.info("Load balancer initialized")
    
    def select_provider(self) -> AIProvider:
        """انتخاب بهترین ارائه‌دهنده"""
        available_providers = []
        
        # بررسی در دسترس بودن
        if config.OPENAI_API_KEY and self.providers[AIProvider.OPENAI].is_healthy:
            available_providers.append(AIProvider.OPENAI)
        
        if config.GEMINI_API_KEY and self.providers[AIProvider.GEMINI].is_healthy:
            available_providers.append(AIProvider.GEMINI)
        
        if not available_providers:
            # اگر هیچ‌کدام سالم نیستند، استفاده از هر کدام که در دسترس است
            if config.OPENAI_API_KEY:
                available_providers.append(AIProvider.OPENAI)
            if config.GEMINI_API_KEY:
                available_providers.append(AIProvider.GEMINI)
        
        if not available_providers:
            raise RuntimeError("هیچ ارائه‌دهنده AI در دسترس نیست")
        
        if len(available_providers) == 1:
            return available_providers[0]
        
        # انتخاب بر اساس عملکرد
        best_provider = max(
            available_providers,
            key=lambda p: (
                self.providers[p].success_rate,
                -self.providers[p].avg_response_time,
                -self.providers[p].consecutive_failures
            )
        )
        
        logger.debug(f"Selected provider: {best_provider.value}")
        return best_provider
    
    def record_request(self, provider: AIProvider, success: bool, response_time: float, error: str = None):
        """ثبت نتیجه درخواست"""
        stats = self.providers[provider]
        stats.total_requests += 1
        
        if success:
            stats.successful_requests += 1
            stats.total_response_time += response_time
            stats.last_success = datetime.now()
            stats.consecutive_failures = 0
        else:
            stats.failed_requests += 1
            stats.last_error = error
            stats.consecutive_failures += 1
        
        logger.debug(f"Provider {provider.value} stats updated: "
                    f"success_rate={stats.success_rate:.1f}%, "
                    f"avg_time={stats.avg_response_time:.2f}s")
    
    def get_stats(self) -> Dict[str, Any]:
        """آمار تعادل بار"""
        return {
            provider.value: {
                "total_requests": stats.total_requests,
                "success_rate": round(stats.success_rate, 2),
                "avg_response_time": round(stats.avg_response_time, 3),
                "consecutive_failures": stats.consecutive_failures,
                "is_healthy": stats.is_healthy,
                "last_success": stats.last_success.isoformat() if stats.last_success else None
            }
            for provider, stats in self.providers.items()
        }

class AIService:
    """سرویس AI پیشرفته با قابلیت‌های کامل"""
    
    def __init__(self):
        # کلاینت‌ها
        self.openai_client = None
        if config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            logger.info("OpenAI client initialized")
        
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            logger.info("Gemini client initialized")
        
        # سیستم‌های پیشرفته
        self.cache = IntelligentCache(max_size=500, ttl_hours=12)
        self.load_balancer = LoadBalancer()
        
        # تنظیمات retry
        self.max_retries = 3
        self.base_delay = 1.0  # ثانیه
        self.max_delay = 10.0  # ثانیه
        
        logger.info("Advanced AI Service initialized successfully")
    
    async def _retry_with_backoff(self, func, *args, **kwargs) -> Tuple[Any, bool, float, str]:
        """اجرای تابع با retry و backoff"""
        last_error = ""
        
        for attempt in range(self.max_retries):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                response_time = time.time() - start_time
                return result, True, response_time, ""
                
            except Exception as e:
                response_time = time.time() - start_time
                last_error = str(e)
                
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                
                if attempt < self.max_retries - 1:
                    # محاسبه تأخیر exponential backoff
                    delay = min(
                        self.base_delay * (2 ** attempt) + random.uniform(0, 1),
                        self.max_delay
                    )
                    logger.info(f"Waiting {delay:.2f}s before retry...")
                    await asyncio.sleep(delay)
        
        return None, False, response_time, last_error
    
    async def generate_headlines(self, news_text: str) -> str:
        """تولید تیتر و لید خبری"""
        prompt_template = get_prompt("headlines_and_leads")
        full_prompt = f"{prompt_template}\n\nمتن خبری:\n{news_text}"
        
        return await self._call_ai_with_cache(full_prompt, "headlines")
    
    async def generate_video_script(self, topic: str, duration: int = 60, platform: str = "instagram") -> str:
        """تولید اسکریپت ویدیو"""
        prompt_template = get_prompt("video_script")
        
        context = f"""
موضوع: {topic}
مدت: {duration} ثانیه
پلتفرم: {platform}
        """
        
        full_prompt = f"{prompt_template}\n\n{context}"
        return await self._call_ai_with_cache(full_prompt, "video_script")
    
    async def fact_check(self, claim: str) -> str:
        """راستی‌آزمایی"""
        prompt_template = get_prompt("fact_check")
        full_prompt = f"{prompt_template}\n\nادعای مورد بررسی:\n{claim}"
        
        return await self._call_ai_with_cache(full_prompt, "fact_check")
    
    async def create_prompt(self, requirements: str, complexity: str = "standard") -> str:
        """تولید پرامپت"""
        prompt_template = get_prompt("prompt_engineering")
        
        context = f"""
نیازمندی‌ها: {requirements}
سطح پیچیدگی: {complexity}
        """
        
        full_prompt = f"{prompt_template}\n\n{context}"
        return await self._call_ai_with_cache(full_prompt, "prompt_engineering")
    
    async def general_ai_chat(self, message: str, context: str = None) -> str:
        """چت عمومی"""
        if context:
            full_prompt = f"{context}\n\n{message}"
        else:
            prompt_template = get_prompt("general_chat")
            full_prompt = f"{prompt_template}\n\n{message}"
        
        return await self._call_ai_with_cache(full_prompt, "general_chat")
    
    async def _call_ai_with_cache(self, prompt: str, operation_type: str = "general") -> str:
        """فراخوانی AI با کش و load balancing"""
        # بررسی کش
        cached_result = self.cache.get(prompt)
        if cached_result:
            logger.info(f"Cache hit for {operation_type}")
            return cached_result
        
        # انتخاب ارائه‌دهنده
        try:
            provider = self.load_balancer.select_provider()
        except RuntimeError as e:
            logger.error(f"No AI providers available: {e}")
            return "⚠️ هیچ سرویس AI در دسترس نیست. لطفاً بعداً تلاش کنید."
        
        # فراخوانی با retry
        if provider == AIProvider.OPENAI:
            result, success, response_time, error = await self._retry_with_backoff(
                self._openai_call, prompt
            )
        else:  # GEMINI
            result, success, response_time, error = await self._retry_with_backoff(
                self._gemini_call, prompt
            )
        
        # ثبت آمار
        self.load_balancer.record_request(provider, success, response_time, error)
        
        if success and result:
            # ذخیره در کش
            self.cache.set(prompt, result, provider.value)
            logger.info(f"Successful {operation_type} request via {provider.value} "
                       f"in {response_time:.2f}s")
            return result
        else:
            logger.error(f"All retry attempts failed for {operation_type}: {error}")
            return f"❌ خطا در پردازش درخواست. لطفاً دوباره تلاش کنید.\n\nجزئیات فنی: {error[:100]}..."
    
    async def _openai_call(self, prompt: str) -> str:
        """فراخوانی OpenAI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")
        
        def sync_call():
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "تو یک دستیار هوشمند و حرفه‌ای هستی که به زبان فارسی پاسخ می‌دهی."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=1500,
                    temperature=0.7,
                    timeout=30.0
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                raise
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_call)
    
    async def bulk_process(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """پردازش دسته‌ای درخواست‌ها"""
        logger.info(f"Starting bulk processing of {len(requests)} requests")
        
        results = []
        semaphore = asyncio.Semaphore(3)  # محدودیت همزمانی
        
        async def process_single(request):
            async with semaphore:
                try:
                    prompt = request.get('prompt', '')
                    operation_type = request.get('type', 'general')
                    
                    result = await self._call_ai_with_cache(prompt, operation_type)
                    
                    return {
                        'id': request.get('id'),
                        'success': True,
                        'result': result,
                        'error': None
                    }
                except Exception as e:
                    logger.error(f"Bulk processing error for request {request.get('id')}: {e}")
                    return {
                        'id': request.get('id'),
                        'success': False,
                        'result': None,
                        'error': str(e)
                    }
        
        # اجرای همزمان درخواست‌ها
        tasks = [process_single(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # فیلتر نتایج
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    'success': False,
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        successful = sum(1 for r in processed_results if r.get('success'))
        logger.info(f"Bulk processing completed: {successful}/{len(requests)} successful")
        
        return processed_results
    
    async def optimize_prompt(self, prompt: str, target_length: int = None) -> str:
        """بهینه‌سازی پرامپت"""
        optimization_prompt = f"""
پرامپت زیر را بهینه‌سازی کن:

{prompt}

اهداف بهینه‌سازی:
- وضوح و دقت بیشتر
- کاهش ابهام
- بهبود ساختار
{"- محدود کردن به " + str(target_length) + " کلمه" if target_length else ""}

پرامپت بهینه‌شده را بنویس:
        """
        
        return await self._call_ai_with_cache(optimization_prompt, "prompt_optimization")
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """تحلیل احساسات متن"""
        analysis_prompt = f"""
احساسات متن زیر را تحلیل کن:

"{text}"

نتیجه را به صورت JSON برگردان:
{{
    "sentiment": "positive/negative/neutral",
    "confidence": 0.0-1.0,
    "emotions": ["emotion1", "emotion2"],
    "summary": "خلاصه تحلیل"
}}
        """
        
        try:
            result = await self._call_ai_with_cache(analysis_prompt, "sentiment_analysis")
            # تلاش برای parse کردن JSON
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            # اگر JSON نبود، خام برگردان
            return {"raw_result": result}
    
    def get_service_stats(self) -> Dict[str, Any]:
        """آمار کلی سرویس"""
        cache_stats = self.cache.get_stats()
        lb_stats = self.load_balancer.get_stats()
        
        return {
            "cache": cache_stats,
            "load_balancer": lb_stats,
            "configuration": {
                "max_retries": self.max_retries,
                "base_delay": self.base_delay,
                "max_delay": self.max_delay,
                "openai_available": bool(self.openai_client),
                "gemini_available": bool(config.GEMINI_API_KEY)
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """بررسی سلامت سرویس"""
        logger.info("Performing AI service health check...")
        
        health_status = {
            "overall": "healthy",
            "providers": {},
            "cache": self.cache.get_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        # تست سریع هر ارائه‌دهنده
        test_prompt = "سلام، این یک تست سلامت است."
        
        # تست OpenAI
        if self.openai_client:
            try:
                start_time = time.time()
                await asyncio.wait_for(self._openai_call(test_prompt), timeout=10.0)
                response_time = time.time() - start_time
                
                health_status["providers"]["openai"] = {
                    "status": "healthy",
                    "response_time": round(response_time, 3),
                    "error": None
                }
            except Exception as e:
                health_status["providers"]["openai"] = {
                    "status": "unhealthy",
                    "response_time": None,
                    "error": str(e)
                }
                health_status["overall"] = "degraded"
        else:
            health_status["providers"]["openai"] = {
                "status": "unavailable",
                "response_time": None,
                "error": "Client not initialized"
            }
        
        # تست Gemini
        if config.GEMINI_API_KEY:
            try:
                start_time = time.time()
                await asyncio.wait_for(self._gemini_call(test_prompt), timeout=10.0)
                response_time = time.time() - start_time
                
                health_status["providers"]["gemini"] = {
                    "status": "healthy",
                    "response_time": round(response_time, 3),
                    "error": None
                }
            except Exception as e:
                health_status["providers"]["gemini"] = {
                    "status": "unhealthy",
                    "response_time": None,
                    "error": str(e)
                }
                if health_status["overall"] != "degraded":
                    health_status["overall"] = "degraded"
        else:
            health_status["providers"]["gemini"] = {
                "status": "unavailable",
                "response_time": None,
                "error": "API key not configured"
            }
        
        # بررسی وضعیت کلی
        healthy_providers = sum(
            1 for provider in health_status["providers"].values()
            if provider["status"] == "healthy"
        )
        
        if healthy_providers == 0:
            health_status["overall"] = "critical"
        elif healthy_providers < len([p for p in health_status["providers"].values() if p["status"] != "unavailable"]):
            health_status["overall"] = "degraded"
        
        logger.info(f"Health check completed: {health_status['overall']}")
        return health_status
    
    async def periodic_maintenance(self):
        """نگهداری دوره‌ای"""
        logger.info("Starting periodic maintenance...")
        
        # پاک کردن کش منقضی
        self.cache.clear_expired()
        
        # ریست آمار ناسالم
        for provider, stats in self.load_balancer.providers.items():
            if stats.consecutive_failures > 5:
                logger.warning(f"Resetting consecutive failures for {provider.value}")
                stats.consecutive_failures = max(0, stats.consecutive_failures - 1)
        
        logger.info("Periodic maintenance completed")
    
    def __del__(self):
        """پاکسازی منابع"""
        logger.info("AI Service cleanup completed")

# نمونه global برای استفاده آسان
ai_service = AIService()
    
    async def _gemini_call(self, prompt: str) -> str:
        """فراخوانی Gemini"""
        def sync_call():
            try:
                model = genai.GenerativeModel('gemini-pro')
                
                # تنظیمات مدل
                generation_config = genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1500,
                )
                
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    raise RuntimeError("Empty response from Gemini")
                    
            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                raise
