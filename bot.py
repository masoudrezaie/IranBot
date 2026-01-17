import os
import openai
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ====== 1️⃣ Load API keys from environment ======
openai.api_key = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# ====== 2️⃣ Define topic buttons ======
keyboard = [
    ["🛜 Internet", "🗣️ Protests"],
    ["⚖️ Human Rights", "👩 Women & Freedom"],
    ["💰 Economy"]
]

reply_keyboard = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True,
    one_time_keyboard=False
)

# ====== 3️⃣ Start command ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Choose a topic to generate an English tweet about Iran 👇",
        reply_markup=reply_keyboard
    )

# ====== 4️⃣ Function to generate tweet from ChatGPT ======
async def generate_tweet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    styles = ["informative", "analytical", "neutral", "serious"]
    style = random.choice(styles)

    prompt = f"""
Write a concise, professional, and publishable tweet about Iran.
Keep it under 280 characters.
Tone: {style}.
Include 1-3 relevant hashtags.
Topic: {topic}
Language: English
"""

    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80
        )
        tweet = response.choices[0].message.content.strip()
        await update.message.reply_text(tweet)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")
        print("OpenAI API error:", e)

# ====== 5️⃣ Run the bot ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_tweet))

    print("🤖 Bot is running...")
    app.run_polling()
