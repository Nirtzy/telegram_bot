from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import os
from dotenv import load_dotenv
import random
from vocabulary import VOCABULARY
from mc_questions import MC_QUESTIONS
from vosk import Model, KaldiRecognizer
import wave
import subprocess
import json
import urllib.request
import zipfile

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Load your token securely

# Store user states: user_id -> correct answer
user_current_answer = {}
user_scores = {}

# Use the large Vosk model
MODEL_NAME = "vosk-model-en-us-0.22"
MODEL_DIR = os.path.join(os.path.dirname(__file__), MODEL_NAME)
MODEL_ZIP = os.path.join(os.path.dirname(__file__), f"{MODEL_NAME}.zip")
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"

# Download and unzip the model if not present
if not os.path.isdir(MODEL_DIR):
    print("Vosk large model not found, downloading...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_ZIP)
    with zipfile.ZipFile(MODEL_ZIP, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(__file__))
    os.remove(MODEL_ZIP)

# Load the Vosk model once at startup
vosk_model = Model(MODEL_DIR)

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

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Download the voice file from Telegram
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = "voice.ogg"
    await file.download_to_drive(file_path)

    # Convert OGG to WAV (Vosk needs WAV PCM)
    wav_path = "voice.wav"
    subprocess.run(["ffmpeg", "-i", file_path, "-ar", "16000", "-ac", "1", wav_path], check=True)

    # Transcribe with Vosk
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    data = wf.readframes(wf.getnframes())
    if rec.AcceptWaveform(data):
        result = rec.Result()
        text = json.loads(result)["text"]
    else:
        text = "Sorry, I couldn't understand the audio."

    await update.message.reply_text(f"🗣 You said: {text}")

    # Clean up
    os.remove(file_path)
    os.remove(wav_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CommandHandler("question", question))
    app.add_handler(CommandHandler("vocab", vocab))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()