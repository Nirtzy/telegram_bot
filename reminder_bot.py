from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import os
from dotenv import load_dotenv
import random
from vocabulary import VOCABULARY
from mc_questions import MC_QUESTIONS
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Load your token securely

# Store user states: user_id -> correct answer
user_current_answer = {}
user_scores = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(f"👋 Hi, {name}! I'm your Python Learning Bot. Use /help to see what I can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/remind <seconds> <message> - Set a reminder\n"
        "/question - Get a Python multiple-choice question\n"
        "/vocab - Get 10 random Python terms with definitions\n"
        "/score - Show your quiz score\n"
        "/help - Show this help message"
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = int(context.args[0])
        message = " ".join(context.args[1:])
        await update.message.reply_text(f"✅ Reminder set! I'll remind you in {seconds} seconds.")

        await asyncio.sleep(seconds)
        await update.message.reply_text(f"🔔 Reminder: {message}")
    except (IndexError, ValueError):
        await update.message.reply_text("❗ Use this format: /remind 10 Take a break")

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(MC_QUESTIONS)
    user_id = update.effective_user.id
    user_current_answer[user_id] = (q["answer"], q.get("explanation", None))
    options = '\n'.join([f"{k}) {v}" for k, v in q["options"].items()])
    await update.message.reply_text(f"\U0001F4AC {q['question']}\n\n{options}\n\nReply with a, b, c, or d.")

async def vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    terms = random.sample(list(VOCABULARY.items()), k=10)
    messages = [f"\U0001F4D6 {term}:\n{defs['en']}\n🇷🇺 {defs['ru']}" for term, defs in terms]
    await update.message.reply_text("\n\n".join(messages))

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, 0)
    await update.message.reply_text(f"🏅 Your score: {score} correct answers!")

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()
    if user_id in user_current_answer and text in ["a", "b", "c", "d"]:
        correct, explanation = user_current_answer[user_id]
        if text == correct:
            user_scores[user_id] = user_scores.get(user_id, 0) + 1
            msg = "✅ Correct!"
        else:
            msg = f"❌ Incorrect. The correct answer was '{correct}'."
        if explanation:
            msg += f"\nExplanation: {explanation}"
        await update.message.reply_text(msg)
        del user_current_answer[user_id]
    elif text in ["a", "b", "c", "d"]:
        await update.message.reply_text("❗ Please use /question to get a new question first.")
    else:
        await update.message.reply_text("❓ I didn't understand that. Use /help to see available commands.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(CommandHandler("vocab", vocab))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()