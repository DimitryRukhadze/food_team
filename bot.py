#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.


import logging
import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"

TITLES = {
    CALLBACK_BUTTON1_LEFT: "Мои подписки",
    CALLBACK_BUTTON2_RIGHT: "Оформить подписку",
}

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\!",
    )
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Пожалуйста выберите:", reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    data = query.data

    if data == CALLBACK_BUTTON1_LEFT:
        query.edit_message_text(text=f"Смотрим подписки")
    else:
        query.edit_message_text(text=f"Оформляем подписку")


def main() -> None:
    load_dotenv()
    """Start the bot."""
    updater = Updater(os.getenv("TG_TOKEN"))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()