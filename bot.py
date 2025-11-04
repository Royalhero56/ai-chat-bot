import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# ========== Gemini Chat Function ==========
def generate_content(full_prompt: str) -> str:
    try:
        # Strong natural human-like prompt
        custom_prompt = f"""
        Tum "Aarav" ho — ek friendly, real human jaisa ladka.
        Tum Hindi-English (Hinglish) me baat karte ho, jaise normal log karte hain.
        Tumhare replies short, natural, thode funny aur emotional hone chahiye.
        Kabhi kabhi emoji use karte ho (😄, 😅, ❤️, 😎, 🤔 etc).
        Avoid karo: robotic lines, long explanations, ya overly formal baat.
        Bas insaan jaisa feel dena hai.

        Examples:
        User: kya kar raha hai
        Aarav: bas chill kar raha hu yaar 😅 tu bata?
        
        User: hello
        Aarav: arey hello! kya haal chaal 😄

        User: bore ho gaya
        Aarav: haha same bro 😂 kuch interesting karte hain kya?

        Ab niche user ka message hai — uska reply natural insaan ki tarah do 👇

        User: {full_prompt}
        Aarav:
        """

        response = model.generate_content(custom_prompt)
        return response.text.strip() if hasattr(response, 'text') else "Lagta hai network slow hai 😅"
    except Exception as e:
        return f"Arre yaar, error aa gaya: {str(e)}"

# ========== Start Command ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    welcome_message = f"Hey {user_name}! 👋 kya haal chaal? main Aarav hu 😄"
    await update.message.reply_text(welcome_message)

# ========== Typing Simulation ==========
async def simulate_typing(update: Update, text: str):
    # Random human-like delay (1.5–3 sec)
    delay = random.uniform(1.5, 3.0)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(delay)
    await update.message.reply_text(text)

# ========== Chat Handler ==========
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    reply_text = generate_content(user_message)

    # Typing effect before sending
    delay = random.uniform(1.5, 3.5)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(delay)

    await update.message.reply_text(reply_text)

# ========== Main App ==========
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Aarav is chatting like a real human 😎")
    app.run_polling()
