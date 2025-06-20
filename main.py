from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Load your token securely

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your Reminder Bot. Use /remind <seconds> <message> to set a reminder.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use this format:\n/remind 10 Take a break")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = int(context.args[0])
        message = " ".join(context.args[1:])
        await update.message.reply_text(f"✅ Reminder set! I’ll remind you in {seconds} seconds.")

        await asyncio.sleep(seconds)
        await update.message.reply_text(f"🔔 Reminder: {message}")
    except (IndexError, ValueError):
        await update.message.reply_text("❗ Use this format: /remind 10 Take a break")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()