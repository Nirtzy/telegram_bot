from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os
from dotenv import load_dotenv
import random
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
        await update.message.reply_text(f"✅ Reminder set! I'll remind you in {seconds} seconds.")

        await asyncio.sleep(seconds)
        await update.message.reply_text(f"🔔 Reminder: {message}")
    except (IndexError, ValueError):
        await update.message.reply_text("❗ Use this format: /remind 10 Take a break")

INTERVIEW_QUESTIONS = [
    "What is a list comprehension in Python?",
    "Explain the difference between a list and a tuple.",
    "What is an API?",
    "Describe the concept of Object-Oriented Programming.",
    "What is a foreign key in SQL?",
    "Explain the difference between a stack and a queue.",
    "What is version control and why is it important?",
    "How do you handle errors in Python?",
    "What is the purpose of the 'self' keyword in Python classes?",
    "What is normalization in databases?"
]

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_text = random.choice(INTERVIEW_QUESTIONS)
    await update.message.reply_text(f"\U0001F4AC Interview Question:\n\n{question_text}")

VOCABULARY = {
    "API": {
        "en": "A set of functions and protocols that allow different software applications to communicate with each other.",
        "ru": "Набор функций и протоколов, позволяющих различным программам взаимодействовать друг с другом."
    },
    "OOP": {
        "en": "Object-Oriented Programming, a programming paradigm based on the concept of objects.",
        "ru": "Объектно-ориентированное программирование, парадигма программирования, основанная на концепции объектов."
    },
    "List Comprehension": {
        "en": "A concise way to create lists in Python using a single line of code.",
        "ru": "Краткий способ создания списков в Python в одной строке кода."
    },
    "Tuple": {
        "en": "An immutable sequence type in Python.",
        "ru": "Неизменяемый тип последовательности в Python."
    },
    "Foreign Key": {
        "en": "A field in a database table that creates a relationship between two tables.",
        "ru": "Поле в таблице базы данных, создающее связь между двумя таблицами."
    },
    "Stack": {
        "en": "A data structure that follows Last-In-First-Out (LIFO) principle.",
        "ru": "Структура данных, работающая по принципу LIFO (последний пришёл — первый ушёл)."
    },
    "Queue": {
        "en": "A data structure that follows First-In-First-Out (FIFO) principle.",
        "ru": "Структура данных, работающая по принципу FIFO (первый пришёл — первый ушёл)."
    },
    "Normalization": {
        "en": "The process of organizing data in a database to reduce redundancy.",
        "ru": "Процесс организации данных в базе данных для уменьшения избыточности."
    },
    "Version Control": {
        "en": "A system that records changes to files over time so you can recall specific versions later.",
        "ru": "Система, которая фиксирует изменения файлов с течением времени, чтобы можно было восстановить определённые версии."
    },
    "Exception Handling": {
        "en": "A way to handle errors or exceptions in a program gracefully.",
        "ru": "Способ обработки ошибок или исключений в программе без её аварийного завершения."
    }
}

async def vocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    term, defs = random.choice(list(VOCABULARY.items()))
    await update.message.reply_text(
        f"\U0001F4D6 {term}:\n{defs['en']}\n\n🇷🇺 {defs['ru']}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(CommandHandler("vocab", vocab))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()