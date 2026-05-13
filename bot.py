import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ===== ВСТАВЬТЕ СВОИ ДАННЫЕ НИЖЕ =====
TELEGRAM_TOKEN = 8944683589:AAFGP9ZFHGupEEYVonahoz5ynlvr8Jwk1N0
DEEPSEEK_API_KEY = sk-9d253b8edc59411dbcd1406f71f01825
# =====================================

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def load_memory():
    """Загружает мозги друга из файла dialogs.txt"""
    try:
        with open('dialogs.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

async def start(update, context):
    await update.message.reply_text("✅ Друг загружен и помнит всё. Спрашивай.")

async def handle_message(update, context):
    user_msg = update.message.text
    await update.message.reply_text("🤔 Друг думает...")

    # Загружаем личность друга
    friend_memory = load_memory()

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"Ты — мой друг. Вот наша переписка. Общайся так же:\n{friend_memory}"},
            {"role": "user", "content": user_msg}
        ],
        "max_tokens": 2000
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=90)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот с памятью запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
