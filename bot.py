import os
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

# ========== Gemini Chat Function ==========
def generate_content(full_prompt: str) -> str:
    try:
        # Improved prompt for natural, human-like replies
        custom_prompt = (
            "You are a friendly and expressive human-like AI chatbot. "
            "Talk like a real person having a natural chat with the user. "
            "Keep your answers warm, casual, and a little fun when possible. "
            "Avoid sounding robotic or formal.\n\n"
            f"User: {full_prompt}"
        )

        response = model.generate_content(custom_prompt)

        # Return response safely
        return response.text if hasattr(response, 'text') else "Sorry, I couldn’t think of a reply right now 😅."
    except Exception as e:
        return f"There was an error generating the response: {str(e)}"

# ========== Start Command ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    welcome_message = f"Hey {user_name}! 👋\nI’m your AI Chatbot powered by Gemini. Let’s talk — what’s on your mind?"
    await update.message.reply_text(welcome_message)

# ========== Chat Handler ==========
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    reply_text = generate_content(user_message)
    await update.message.reply_text(reply_text)

# ========== Main App ==========
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run bot
    print("🤖 Bot is running... (powered by Gemini)")
    app.run_polling()
