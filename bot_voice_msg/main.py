import logging
import re

from converter import get_text
from punk_processor import enhance_text
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)
    downloaded_file = await file.download_as_bytearray()
    with open("new_file.ogg", "wb") as new_file:
        new_file.write(downloaded_file)
    result = get_text("new_file.ogg")
    convert_result = re.sub(
        r"\\u([0-9A-Fa-f]{4})", lambda x: chr(int(x.group(1), 16)), result[0]
    )
    result_with_punk = enhance_text(convert_result)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"{user}: {result_with_punk}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("5420433351:AAHxEwFYSn-6_Ld1mm_ujEVJbUx62rtpP5s")
        .build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.ALL, convert))
    application.run_polling()
