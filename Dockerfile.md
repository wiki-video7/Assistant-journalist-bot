# Dockerfile - Assistant Journalist Bot

FROM python:3.9-slim

# نصب پیش‌نیازهای سیستم
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# تنظیم working directory
WORKDIR /app

# کپی requirements و نصب
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد
COPY . .

# ایجاد پوشه‌های ضروری
RUN mkdir -p logs uploads cache data

# اجرا
CMD ["python", "main.py"]
