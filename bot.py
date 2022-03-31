import logging
import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from find_subscription import get_subscriptions, get_json_content, present_subscriptions, get_recipe
from time import sleep


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
    update.message.reply_text("Use /start to test this bot")


def main_button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    data = query.data
    user = update.effective_user
    id = user.id
    json_content = get_json_content("subscriptions.json")
    if data == CALLBACK_BUTTON1_LEFT:
        user_subscriptions = get_subscriptions(
            id,
            json_content
            )
        query.edit_message_text(text=f"Смотрим подписки пользователя {id}")
        sleep(1)
        if user_subscriptions:
            view = present_subscriptions(user_subscriptions)
            for sub in view:
                result = ', '.join([f'{key}: {value}' for key, value in sub.items()])
                query.edit_message_text(text=result)
        else:
            query.edit_message_text(text="Подписок не найдено. Вернитесь в стартовое меню и оформите подписку.")
    else:
        query.edit_message_text(text=f"Оформляем подписку")


def get_meal(update: Update, context: CallbackContext) -> None:
    text, image = get_recipe()
    update.message.reply_markdown_v2("*Ваше блюдо ↓*")
    with open(image, "rb") as photo:
        update.message.reply_photo(photo)
    update.message.reply_markdown_v2(text)
    # update.message.reply_text(text)
    


def main() -> None:
    load_dotenv()
    """Start the bot."""
    updater = Updater(os.getenv("TG_TOKEN"))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(main_button))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("meal", get_meal))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()