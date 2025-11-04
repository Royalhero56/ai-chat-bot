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

# ====== AI Response Function ======
def generate_content(prompt: str) -> str:
    try:
        full_prompt = f"""
        Tum "Heroin" ho — ek friendly, sweet aur thodi naughty ladki 💕
        Tum Hinglish (Hindi + English mix) me baat karti ho jaise normal log karte hain.
        Emoji kabhi kabhi use karna (😄, 🤭, 😅, ❤️, 😉 etc).

        Example:
        User: kya kar rahi ho
        Heroin: bas chill kar rahi hu 😅 tu kya kar raha hai?

        User: hello
        Heroin: heyy 😄 kya haal chaal?

        Ab user ka message niche likha hai 👇
        User: {prompt}
        Heroin:
        """
        response = model.generate_content(full_prompt)
        return response.text.strip() if hasattr(response, 'text') else "umm... samajh nahi aaya 😅"
    except Exception as e:
        return f"Oops! kuch gadbad lag rahi hai 😅 ({str(e)})"


# ====== /start Command ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Heyy {user} 💖 main Heroin hu 😄 kaise ho?")


# ====== Smart Chat Filter ======
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_type = update.message.chat.type
    text = message.text or ""

    # Group chat logic
    if chat_type in ["group", "supergroup"]:
        # ✅ Bot sirf tab reply kare jab:
        # 1️⃣ Message me "heroin" ya "aisha" ho
        # 2️⃣ Ya message Heroin ke message ka reply ho
        if (
            "heroin" not in text.lower()
            and "aisha" not in text.lower()
            and not message.reply_to_message
        ):
            return  # ❌ Ignore sabka message

    # ✅ Normal reply (private or mentioned)
    reply = generate_content(text)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(random.uniform(1.5, 3))
    await update.message.reply_text(reply)


# ====== Main App ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("💖 Heroin is live and replying smartly!")
    app.run_polling()
