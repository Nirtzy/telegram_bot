# Telegram Python Learning Bot

A Telegram bot for learning Python interactively! Features include:
- Multiple-choice Python quiz questions with explanations
- Vocabulary training with English and Russian definitions
- Audio recognition: transcribe and evaluate user voice messages (Vosk in development, switching to OpenAI/Google soon)
- Reminders and motivational messages

## Features
- `/start` — Welcome and onboarding
- `/help` — List all commands and usage
- `/remind <seconds> <message>` — Set a reminder
- `/question` — Get a random Python multiple-choice question
- `/score` — See your quiz score
- `/vocab` — Get 10 random Python terms with definitions (EN/RU)
- **Voice messages** — Send a voice message and get a transcription

## Installation
1. Clone the repo:
   ```sh
   git clone https://github.com/Nirtzy/telegram_bot.git
   cd telegram_bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables (`.env` or Render dashboard):
   - `BOT_TOKEN` — your Telegram bot token
   - `OPENAI_API_KEY` — (optional, for OpenAI features)
4. (Optional) Install ffmpeg if not present:
   ```sh
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```
5. Run the bot:
   ```sh
   python reminder_bot.py
   ```

## Usage
- Interact with the bot on Telegram using the commands above.
- Send a voice message to get a transcription.

## Roadmap
- [x] Multiple-choice questions with explanations
- [x] Vocabulary with EN/RU definitions
- [x] Audio recognition with Vosk (did not work reliably in production)
- [ ] Switch to OpenAI Whisper or Google Cloud Speech-to-Text for audio recognition
- [ ] Pronunciation scoring and feedback
- [ ] Inline buttons for answering questions
- [ ] User leaderboards and statistics
- [ ] Daily/weekly challenges
- [ ] More question categories and difficulty levels
- [ ] Webhook support for production deployment

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT 