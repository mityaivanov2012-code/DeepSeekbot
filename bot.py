import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = "8944683589:AAFGP9ZFHGupEEYVonahoz5ynlvr8Jwk1N0"
DEEPSEEK_API_KEY = "sk-9d253b8edc59411dbcd1406f71f01825"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# === ВЕБ-СЕРВЕР ДЛЯ RENDER ===
flask_app = Flask(__name__)

@flask_app.route('/')
def health():
    return "Бот работает", 200

def run_webserver():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# === ФУНКЦИИ БОТА ===
def load_memory():
    try:
        with open('dialogs.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

async def start(update, context):
    await update.message.reply_text("✅ Бот запущен. Друг загружен.")

async def handle_message(update, context):
    user_msg = update.message.text
    await update.message.reply_text("🤔 Друг думает...")

    friend_memory = load_memory()

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"Ты — мой друг. Вот наша переписка:\n{friend_memory}"},
            {"role": "user", "content": user_msg}
        ],
        "max_tokens": 2000
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=60)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен и готов к работе")
    app.run_polling()

if __name__ == "__main__":
    # Запускаем веб-сервер в фоне
    threading.Thread(target=run_webserver, daemon=True).start()
    main()
