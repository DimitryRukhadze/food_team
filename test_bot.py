import logging
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler
from find_subscription import get_subscriptions, get_json_content, present_subscriptions, get_recipe
from time import sleep


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH = range(4)

MY_SUBSCRIPTIONS, SUBSCRIBE = range(2)


def start(update, context):
    chat_id = update.effective_chat.id
    menu_buttons = [
        InlineKeyboardButton('Мои подписки', callback_data=str(MY_SUBSCRIPTIONS)),
        InlineKeyboardButton('Оформить подписку', callback_data=str(SUBSCRIBE))
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(menu_buttons, n_cols=2))
    context.bot.send_message(chat_id=chat_id, text='Что вы хотите сделать?', reply_markup=reply_markup)

    return FIRST


def show_subscriptions(update, context) -> None:
    chat_id = update.effective_chat.id
    query = update.callback_query
    user = update.effective_user
    user_id = user.id

    json_content = get_json_content("subscriptions.json")

    user_subscriptions = get_subscriptions(
        user_id,
        json_content
    )

    if user_subscriptions:
        view = present_subscriptions(user_subscriptions)
        for sub in view:
            result = ', '.join([f'{key}: {value}' for key, value in sub.items()])
            context.bot.send_message(chat_id=chat_id, text=result)

    else:
        query.edit_message_text(text="Подписок не найдено. Вернитесь в стартовое меню и оформите подписку.")


def get_menu_type(update, context):
    chat_id = update.effective_chat.id
    menu_types = ['classic', 'vegetarian', 'keto', 'low_carbs']
    menu_types_markup = customize_menu(menu_types)

    context.bot.send_message(
        chat_id=chat_id,
        text='Выберите тип меню',
        reply_markup=menu_types_markup
    )

    return SECOND

def get_persons_number(update, context):
    chat_id = update.effective_chat.id
    num_of_persons = [x for x in range(1, 7)]
    persons_markup = customize_menu(num_of_persons)
    context.bot.send_message(
        chat_id=chat_id,
        text='На сколько человек будете готовить?',
        reply_markup=persons_markup
    )

    return THIRD


def get_meals_number(update, context):
    chat_id = update.effective_chat.id
    num_of_meals = [x for x in range(1,7)]
    num_of_meals_markup = customize_menu(num_of_meals)
    context.bot.send_message(
        chat_id=chat_id,
        text='Сколько приёмов пищи?',
        reply_markup=num_of_meals_markup
    )

    return FOURTH


def customize_menu(menu_names):
    if not len(menu_names)%2:
        cols = 2
    else:
        cols = 3

    menu_buttons = [
        InlineKeyboardButton(type, callback_data=type)
        for type in menu_names
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(menu_buttons, n_cols=cols))

    return reply_markup


def build_menu(buttons, n_cols):

    menu = [
        buttons[button:button + n_cols]
        for button in range(0, len(buttons), n_cols)
    ]

    return menu


if __name__ == "__main__":

    load_dotenv()
    updater = Updater(os.getenv("TG_TOKEN"))

    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(show_subscriptions, pattern='^' + str(MY_SUBSCRIPTIONS) + '$'),
                CallbackQueryHandler(get_menu_type, pattern='^' + str(SUBSCRIBE) + '$')
            ],
            SECOND:[CallbackQueryHandler(get_persons_number)],
            THIRD:[CallbackQueryHandler(get_meals_number)],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()