# 🐍 Base image with Python
FROM python:3.11-slim

# 📁 Set working directory
WORKDIR /app

# 📦 Copy bot files into container
COPY . /app

# 🔧 Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🕒 Optional: Set timezone (India)
ENV TZ=Asia/Kolkata

# 🚀 Run the bot
CMD ["python", "bot.py"]
