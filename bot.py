print("🔥 NEW CODE VERSION 1.2 LOADED 🔥")

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
import os

TOKEN = "8735791546:AAF-GZ-vaFIIUVfp2OwbuQLyWoJA0ALBJYg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello human 🤖\n\n"
        "Usage:\n/remind <minutes> <message>\n\n"
        "Example:\n/remind 1 drink water"
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(context.args[0])
        message = " ".join(context.args[1:])

        if not message:
            await update.message.reply_text("Give me something to remind you about.")
            return

        context.job_queue.run_once(
            send_voice_reminder,
            when=minutes * 60,
            data={
                "chat_id": update.effective_chat.id,
                "text": message
            }
        )

        await update.message.reply_text(
            f"⏰ Reminder set!\n"
            f"I will remind you in {minutes} minute(s)."
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def send_voice_reminder(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    text = job_data["text"]

    filename = f"reminder_{chat_id}.mp3"

    tts = gTTS(text=f"Reminder. {text}", lang="en")
    tts.save(filename)

    with open(filename, "rb") as audio:
        await context.bot.send_voice(chat_id=chat_id, voice=InputFile(audio))

    os.remove(filename)

def main():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))

    print("🤖 Bot is alive and listening...")

    app.run_polling()

if __name__ == "__main__":
    main()
