import os
import requests
import traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = 8944683589:AAFGP9ZFHGupEEYVonahoz5ynlvr8Jwk1N0
DEEPSEEK_API_KEY = sk-9d253b8edc59411dbcd1406f71f01825
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def load_memory():
    try:
        with open('dialogs.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ОШИБКА ПРИ ЗАГРУЗКЕ ФАЙЛА: {e}"

async def start(update, context):
    await update.message.reply_text("✅ Бот запущен")

async def handle_message(update, context):
    user_msg = update.message.text
    await update.message.reply_text("🤔 Думаю...")

    try:
        friend_memory = load_memory()

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"Ты друг. Вот диалоги:\n{friend_memory}"},
                {"role": "user", "content": user_msg}
            ]
        }
        response = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        error_text = traceback.format_exc()
        # Отправим ошибку в Telegram
        await update.message.reply_text(f"❌ Ошибка в боте:\n{error_text[:500]}")
        # И напечатаем в логах Render
        print(error_text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
