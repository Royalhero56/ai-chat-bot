import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Store user who is currently chatting with Heroin
active_user_id = None

def generate_content(prompt: str) -> str:
    try:
        custom_prompt = f"""
        Tum "Heroin" ho — ek cute, friendly, emotional aur thodi naughty ladki 💖
        Tum Hinglish me baat karti ho (Hindi + English mix), natural tone me.
        Har reply short, natural aur thoda expressive hona chahiye.
        Emoji kabhi kabhi use karna (😄, 🤭, ❤️, 😉, 😅 etc).

        Example:
        User: kya kar rahi ho
        Heroin: bas chill kar rahi hu 😅 tu kya kar raha hai?

        User: hello
        Heroin: heyy 😄 kya haal chaal?

        User: bore ho gaya
        Heroin: haha same 😅 kuch masti karte hain kya?

        User: {prompt}
        Heroin:
        """
        response = model.generate_content(custom_prompt)
        return response.text.strip() if hasattr(response, 'text') else "umm... samajh nahi aaya 😅"
    except Exception as e:
        return f"Oops kuch gadbad lag rahi hai 😅 ({str(e)})"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_user_id
    user = update.effective_user
    active_user_id = user.id
    await update.message.reply_text(f"Heyy {user.first_name} 💕 main Heroin hu 😄 kaise ho?")
    print(f"💬 Active user set to: {user.first_name} ({user.id})")

# Chat handler
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_user_id
    user = update.effective_user

    # Ignore messages from others if not active user
    if active_user_id and user.id != active_user_id:
        return

    user_text = update.message.text
    reply = generate_content(user_text)

    # typing delay
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(random.uniform(1.5, 3))
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("💖 Heroin is ready and will only chat with the active user!")
    app.run_polling()
