import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# ====== Gemini Chat Function ======
def generate_content(full_prompt: str) -> str:
    try:
        custom_prompt = f"""
        Tum "Heroin" ho — ek cute, friendly aur thodi naughty ladki 💕
        Tum Hinglish (Hindi + English mix) me baat karti ho jaise normal log karte hain.
        Tumhare replies short, sweet aur natural hone chahiye.
        Emoji kabhi kabhi use karna (😄, 🤭, 😅, ❤️, 😉 etc).
        Avoid robotic ya formal style — ek real ladki jaisa tone rakho.

        Example:
        User: kya kar rahi ho
        Heroin: bas chill kar rahi hu 😅 tu kya kar raha hai?

        User: hello
        Heroin: heyy 😄 kya haal chaal?

        User: bore ho gaya
        Heroin: haha same 😅 kuch masti karte hain kya?

        Ab user ka message niche likha hai 👇
        User: {full_prompt}
        Heroin:
        """

        response = model.generate_content(custom_prompt)
        return response.text.strip() if hasattr(response, 'text') else "umm... samajh nahi aaya 😅"
    except Exception as e:
        return f"Oops! kuch gadbad lag rahi hai 😅 ({str(e)})"


# ====== Start Command ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Heyy {user} 💕! main Heroin hu 😄 kaise ho?")


# ====== Smart Chat Handler ======
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Check if group chat
    if update.message.chat.type in ["group", "supergroup"]:
        # Bot will only reply if:
        # 1. Someone replies to Heroin's message, OR
        # 2. Message contains her name ("Heroin")
        if (
            not message.reply_to_message
            and "heroin" not in message.text.lower()
        ):
            return  # ignore others' messages

    user_text = message.text
    reply = generate_content(user_text)

    # Simulate typing delay
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(random.uniform(1.5, 3.5))
    await update.message.reply_text(reply)


# ====== Main App ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("💖 Heroin is now chatting smartly in groups!")
    app.run_polling()
