print("reminder_bot.py is starting up...")
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import os
from dotenv import load_dotenv
import random
from vocabulary import VOCABULARY
from mc_questions import MC_QUESTIONS
import openai
import subprocess
import json
import requests
import difflib

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Load your token securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Store user states: user_id -> correct answer
user_current_answer = {}
user_scores = {}

# Add a list of phrases for pronunciation practice
PHRASES = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a powerful programming language.",
    "Artificial intelligence is the future.",
    "Practice makes perfect.",
    "Never stop learning.",
    "Hello, how are you today?",
    "Can you pronounce this sentence clearly?",
    "Consistency is the key to success.",
    "I enjoy solving challenging problems.",
    "Let's improve our English pronunciation."
]

# Store user pronunciation state: user_id -> phrase
user_pronounce_phrase = {}

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
        "/pronounce - Practice pronunciation\n"
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

async def pronounce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import requests
    import tempfile
    import shutil
    import uuid

    user_id = update.effective_user.id
    phrase = random.choice(PHRASES)
    user_pronounce_phrase[user_id] = phrase

    await update.message.reply_text(f"🔊 Please listen and repeat:\n\n{phrase}")

    # Generate TTS audio with ElevenLabs
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # You can use a specific voice or let ElevenLabs pick default
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": phrase,
        "model_id": "eleven_monolingual_v1"
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        # Save audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            shutil.copyfileobj(response.raw, f)
            audio_path = f.name
        # Send audio to user
        with open(audio_path, "rb") as audio_file:
            await update.message.reply_voice(audio_file)
        os.remove(audio_path)
    else:
        print("ElevenLabs error:", response.status_code, response.text)
        await update.message.reply_text("❗ Sorry, could not generate pronunciation audio.")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = "voice.ogg"
    await file.download_to_drive(file_path)
    mp3_path = "voice.mp3"
    subprocess.run(["ffmpeg", "-i", file_path, mp3_path], check=True)

    # Transcribe with Whisper
    with open(mp3_path, "rb") as audio_file:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": audio_file},
            data={"model": "whisper-1"}
        )
        if response.status_code == 200:
            text = response.json().get("text", "(no text returned)")
        else:
            text = f"Sorry, there was an error: {response.text}"

    # Check if user is in pronunciation mode
    if user_id in user_pronounce_phrase:
        target = user_pronounce_phrase[user_id]
        # Evaluate similarity
        ratio = difflib.SequenceMatcher(None, text.lower(), target.lower()).ratio()
        percent = int(ratio * 100)
        if percent > 90:
            feedback = "🌟 Excellent pronunciation!"
        elif percent > 75:
            feedback = "👍 Good job! A little more practice and you'll be perfect."
        elif percent > 50:
            feedback = "🙂 Not bad, but try to be clearer."
        else:
            feedback = "🔄 Let's try again! Listen carefully and repeat."
        await update.message.reply_text(f"You said: {text}\n\nSimilarity: {percent}%\n{feedback}")
        del user_pronounce_phrase[user_id]
    else:
        await update.message.reply_text(f"🗣 You said: {text}")

    os.remove(file_path)
    os.remove(mp3_path)

def main():
    print("Starting main()...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    print("App built.")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(CommandHandler("vocab", vocab))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("pronounce", pronounce))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    print("🤖 Bot is running in polling mode...")
    app.run_polling()

if __name__ == '__main__':
    main()