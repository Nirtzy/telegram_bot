# Telegram Python Learning Bot

A Telegram bot for learning Python interactively! Features include:
- Multiple-choice Python quiz questions with explanations
- Vocabulary training with English and Russian definitions
- Audio recognition: transcribe and evaluate user voice messages (now using OpenAI Whisper)
- Pronunciation game: listen to a phrase, repeat it, and get feedback (using ElevenLabs TTS and Whisper)
- Reminders and motivational messages

## Features
- `/start` — Welcome and onboarding
- `/help` — List all commands and usage
- `/remind <seconds> <message>` — Set a reminder
- `/question` — Get a random Python multiple-choice question
- `/score` — See your quiz score
- `/vocab` — Get 10 random Python terms with definitions (EN/RU)
- `/pronounce` — Practice pronunciation: get a phrase, hear it, repeat it, and get feedback
- **Voice messages** — Send a voice message and get a transcription (powered by OpenAI Whisper)

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
   - `OPENAI_API_KEY` — your OpenAI API key (required for voice transcription)
   - `ELEVENLABS_API_KEY` — your ElevenLabs API key (required for pronunciation game)
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
- Send a voice message to get a transcription (uses OpenAI Whisper API).
- Use `/pronounce` to practice your pronunciation: listen to a phrase, repeat it, and get instant feedback!

## Roadmap
- [x] Multiple-choice questions with explanations
- [x] Vocabulary with EN/RU definitions
- [x] Audio recognition with Vosk (deprecated)
- [x] Switch to OpenAI Whisper for audio recognition
- [x] Pronunciation game with ElevenLabs TTS and Whisper evaluation
- [ ] Pronunciation scoring and advanced feedback
- [ ] Inline buttons for answering questions
- [ ] User leaderboards and statistics
- [ ] Daily/weekly challenges
- [ ] More question categories and difficulty levels
- [ ] Webhook support for production deployment

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT 