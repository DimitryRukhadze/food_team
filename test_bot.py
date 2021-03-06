import logging
import os

from dotenv import load_dotenv
from telegram import (
    KeyboardButton, LabeledPrice, ParseMode, ReplyKeyboardMarkup, Update,
    )
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, 
    CallbackQueryHandler, ConversationHandler, 
    PreCheckoutQueryHandler, MessageHandler, Filters
    )


import foodapp_api
from bot_utils import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

START, MY_SUBSCRIPTIONS, SUBSCRIBE = range(3)
REGISTER, FIRSTNAME, LASTNAME, CONTACT = range(3, 7)
SHOW_SUB_OR_MENU, NUM_PERSONS, NUM_MEALS, ALLERGY_OR_PLAN, INVOICE, PROMO, CHECKOUT, QUERY_SUBSCRIPTION, RECIPE = range(7, 16)




def reset_user_input(update: Update, context: CallbackContext):
    invoice = context.user_data.get('invoice')
    if invoice:
        invoice_id, invoice_chat_id = invoice
        context.bot.delete_message(chat_id=invoice_chat_id, message_id=invoice_id)
    if update.callback_query:
            update.callback_query.delete_message()
    context.user_data.clear()


def start(update: Update, context: CallbackContext):
    values_ref = foodapp_api.get_reference_api()
    for key in values_ref:
        context.bot_data[key] = values_ref[key]

    reset_user_input(update, context)

    chat_id = update.effective_chat.id
    
    user = foodapp_api.get_user_api(chat_id)
    user_id = user['id']
    if not user_id:
        text = (
            "Вы не зарегистрированы в системе.\nЕсли вы хотите продолжить,"
            "нам с Вами надо как следует познакомиться.\nГотовы начать?"
        )

        reply_markup = single_button_menu('Начать регистрацию', str(REGISTER))
    else:
        user_data = user['data']
        text = (
            f'С возвращением, {user_data["firstname"]}!\n'
            f'Выберите действие, чтобы продолжить:'
        )
        menu_buttons = [[
            InlineKeyboardButton('Мои подписки', callback_data=str(MY_SUBSCRIPTIONS)),
            InlineKeyboardButton('Оформить подписку', callback_data=str(SUBSCRIBE))
        ]]
        reply_markup = InlineKeyboardMarkup(menu_buttons)

    context.bot.send_message(
        chat_id=chat_id, 
        text=text, 
        reply_markup=reply_markup
        )

    return SHOW_SUB_OR_MENU


def show_subscriptions(update, context) -> None:
    chat_id = update.effective_chat.id
    query = update.callback_query
    query.delete_message()

    try:
        user_subscriptions = foodapp_api.get_subscriptions_api(chat_id)
    except Exception:
        user_subscriptions = []

    if user_subscriptions:
        sub_info = {}

        for sub in user_subscriptions:
            sub_id = sub['id']
            sub_stats = (
                f'{sub["cousine_type"]}, '
                f'по {get_plural_for_servings(sub["num_servings"])} '
                f'на {get_plural_for_person(sub["num_persons"])}\n'
            )

            sub_info[sub_id] = sub_stats
        sub_markups = customize_menu_2(sub_info, cols=1)

        context.bot.send_message(
            chat_id=chat_id, 
            text='Выберите подписку, по которой хотите блюдо: ', 
            reply_markup=sub_markups
            )


        return RECIPE

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Подписок не найдено. Вернитесь в стартовое меню и оформите подписку.',
            reply_markup=single_button_menu('Вернуться в меню', str(START))
            )
        return ConversationHandler.END


def give_user_recipe(update, context):
    chat_id = update.effective_chat.id
    recipe = foodapp_api.get_recipe(int(update.callback_query.data))

    text, image_name = show_recipe(recipe)

    recipe_image = foodapp_api.get_image_from_server(image_name)

    update.callback_query.delete_message()

    context.bot.send_message(
        chat_id=chat_id, 
        text='<b>Ваше блюдо ↓</b>', 
        parse_mode=ParseMode.HTML
    )
    context.bot.send_photo(
        chat_id=chat_id, 
        photo=recipe_image
        )
    context.bot.send_message(
        chat_id=chat_id, 
        text=text, 
        parse_mode=ParseMode.HTML
        )

    return ConversationHandler.END


def get_menu_type(update, context):
    chat_id = update.effective_chat.id

    api_field = 'cousine_type'
    menu_types = context.bot_data['cousine_types']    
    menu_types_markup = customize_menu(api_field, menu_types)


    update.callback_query.delete_message()
    context.bot.send_message(
        chat_id=chat_id,
        text='Выберите тип меню:',
        reply_markup=menu_types_markup
    )

    return NUM_PERSONS

def get_persons_number(update, context):
    key, value = update.callback_query.data.split(':')
    context.user_data[key] = value
    
    chat_id = update.effective_chat.id

    api_field = 'num_persons'
    num_of_persons = [x for x in range(1, 7)]

    persons_markup = customize_menu(api_field, num_of_persons)
    text = (
        f'Тип меню: {context.user_data["cousine_type"]}\n'
        f'Количество персон: \n'
        f'\n'
        f'На сколько человек будете готовить?'
    )

    update.callback_query.delete_message()
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=persons_markup
    )

    return NUM_MEALS


def get_meals_number(update, context):
    key, value = update.callback_query.data.split(':')
    context.user_data[key] = value

    chat_id = update.effective_chat.id

    api_field = 'num_servings'
    num_of_meals = [x for x in range(1,7)]
    num_of_meals_markup = customize_menu(api_field, num_of_meals)

    text = (
        f'Тип меню: {context.user_data["cousine_type"]}\n'
        f'Количество персон: {context.user_data["num_persons"]}\n'
        f'Количество порций:\n'
        f'\n'
        f'Сколько приёмов пищи?'
    )
    update.callback_query.delete_message()
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=num_of_meals_markup
    )

    return ALLERGY_OR_PLAN


def get_allergies(update: Update, context: CallbackContext):
    key, value = update.callback_query.data.split(':')

    if not context.user_data.get('loop'):
        # Save user input from previous step and mark for looping
        context.user_data[key] = value
        context.user_data['allergies'] = []
        context.user_data['loop'] = True
    else:
        context.user_data['allergies'].append(value)

    api_field = 'allergies'
    all_allergy_types = [t for t in context.bot_data['allergies']]
    all_allergy_types.append('Продолжить')
    remaining_allergy_types = [t for t in all_allergy_types if t not in context.user_data['allergies']]

    allergy_types_markup = customize_menu(api_field, remaining_allergy_types, cols=1)
    allergies_chosen = ', '.join(context.user_data['allergies']) if context.user_data["allergies"] else 'нет'
    text = (
        f'Тип меню: {context.user_data["cousine_type"]}\n'
        f'Количество персон: {context.user_data["num_persons"]}\n'
        f'Количество порций: {context.user_data["num_servings"]}\n'
        f'Выбранные аллергии: {allergies_chosen}\n'
        f'\n'
        f'Выберите аллергии или нажмите продолжить:'
    )

    update.callback_query.delete_message()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=allergy_types_markup
    )

    return ALLERGY_OR_PLAN


def get_plan(update: Update, context: CallbackContext):
    del context.user_data['loop']
    plans = context.bot_data['plans']

    api_field = 'plan'
    menu_plans = [f'{plan["name"]} - {plan["price"]} р.' for plan in plans]    
    menu_plans_markup = customize_menu(api_field, menu_plans)

    allergies_chosen = (
        ', '.join(context.user_data["allergies"])
        if context.user_data["allergies"] else 'Нет'
    )

    text = (
        f'Тип меню: {context.user_data["cousine_type"]}\n'
        f'Количество персон: {context.user_data["num_persons"]}\n'
        f'Количество порций: {context.user_data["num_servings"]}\n'
        f'Выбранные аллергии: {allergies_chosen}\n'
        f'\n'
        f'Выберите один из доступных планов подписки:'
    )

    update.callback_query.delete_message()
    chat_id = update.effective_chat.id
    
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=menu_plans_markup
    )
    
    return INVOICE


def get_promo(update:Update, context:CallbackContext):
    if not context.user_data.get('promo'):
        context.user_data['plan'] = update.callback_query.data

    chat_id = update.effective_chat.id
    update.callback_query.delete_message()

    message = context.bot.send_message(
        chat_id=chat_id,
        text=(
            'Введите промокод для получения скидки.\n'
            'Если у Вас не промокода, просто нажмите продолжить.'
        ),
        reply_markup=single_button_menu('Продолжить без промокода', str(INVOICE))
    )

    context.user_data['promo'] = {'message_id':message.message_id}

    return INVOICE


def save_promo(update:Update, context:CallbackContext):
    chat_id = update.effective_chat.id

    context.bot.delete_message(chat_id=chat_id, message_id=context.user_data['promo']['message_id'])

    promo = foodapp_api.get_promo_api(update.message.text)
    valid = (
        promo and
        (promo['cousine_type']=='ALL' 
        or promo['cousine_type']==context.user_data['cousine_type'])
    )
    if valid:
        context.user_data['promo']['code'] = promo["code"]
        context.user_data['promo']['discount'] = promo["discount"]
        text = (
            f'Ваш код - {promo["code"]}\n'
            f'Вы сможете получить {promo["discount"]}% скидки на Вашу подписку!'
        )
        reply_markup = single_button_menu('Использовать промокод', str(INVOICE))
    else:
        text = (
            f'Промокод введен неверно либо не подходит для данного вида подписки.\n'
            f'Вы можете попробовать ввести другой код, либо продолжить без промокода.'
        )
        reply_markup = single_button_menu('Продолжить без промокода', str(INVOICE))

    message = context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )

    context.user_data['promo']['message_id']=message.message_id

    return INVOICE


def get_invoice(update:Update, context:CallbackContext):
    for plan in context.bot_data['plans']:
        if plan['name'] in context.user_data['plan']:
            selected_plan = plan
            
    context.user_data['plan_duration'] = selected_plan['duration']

    chat_id = update.effective_chat.id

    invoice_title = 'Оформление подписки'
    allergies_chosen = (
        ', '.join(context.user_data["allergies"])
        if context.user_data["allergies"] else 'Нет'
    )
    invoice_description = (
        f'Тип меню: {context.user_data["cousine_type"]}'
        f' {context.user_data["num_persons"]} x'
        f' {context.user_data["num_servings"]}'
        f'\n Исключить: {allergies_chosen}'
        f'\nСрок подписки (месяцев): {context.user_data["plan_duration"]}'
    )
    invoice_payload = f'SUB_FOR_{chat_id}'
    provider_token = os.getenv('YUKASSA_TOKEN')
    currency = "RUB"

    prices = [
        LabeledPrice(f'Подписка на {selected_plan["name"]}', selected_plan['price'] * 100)
    ]

    code = context.user_data['promo'].get('code')
    if code:
        discount_percent = context.user_data['promo'].get('discount')
        discount = -int((selected_plan['price'] / 100) * discount_percent)
        prices.append(LabeledPrice(f'Промокод {code}',  discount*100))

    update.callback_query.delete_message()
    invoice = context.bot.send_invoice(
        chat_id=chat_id, 
        title=invoice_title, 
        description=invoice_description, 
        payload=invoice_payload,
        provider_token=provider_token, 
        currency=currency, 
        prices=prices
    )
    
    context.user_data['invoice'] = (invoice.message_id, invoice.chat_id)

    return ConversationHandler.END


def get_checkout(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    
    invoice_id, invoice_chat_id = context.user_data['invoice']

    if query.invoice_payload != f'SUB_FOR_{invoice_chat_id}':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        query.answer(ok=True)

    invoice_id, invoice_chat_id = context.user_data['invoice']
    del context.user_data['invoice']
    context.bot.delete_message(chat_id=invoice_chat_id, message_id=invoice_id)
    return QUERY_SUBSCRIPTION


def query_subscription(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        new_sub = foodapp_api.add_subscription_api(
            chat_id=chat_id,
            cousine_type=context.user_data['cousine_type'],
            num_persons=int(context.user_data['num_persons']),
            num_servings=int(context.user_data['num_servings']),
            allergies=context.user_data['allergies'],
            plan=context.user_data['plan_duration']
        )
    except Exception:
        new_sub = None

    if new_sub:
        sub_data = new_sub['data']
        excluded = (
            f'Исключены {", ".join(sub_data["allergies"]).lower()}' 
            if sub_data["allergies"] else 'Любые продукты'
        )
        text = (
            f'Отлично! Ваша подписка создана!\n\n'
            f'{sub_data["cousine_type"]} меню\n'
            f'По {get_plural_for_servings(sub_data["num_servings"])} '
            f'на {get_plural_for_person(sub_data["num_persons"])}\n'
            f'{excluded}\n'
            f'\n'
            f'Подписка активна до {get_date_from_timestamp(sub_data["expires_on"])}'
        )
    else:
        text = 'Что-то пошло не так... попробуйте повторить попытку позже!\nВы можете вернуться в главное меню командой /start'

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=single_button_menu('Вернуться в меню', str(START))
    )
    

    return ConversationHandler.END


def get_firstname(update: Update, context: CallbackContext):
    update.callback_query.delete_message()
    chat_id = update.effective_chat.id

    text = (
        'Мы бы хотели знать Ваше имя и фамилию\n'
        'Для начала, пожалуйста, введите имя:'
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )

    return FIRSTNAME


def get_lastname(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.user_data['firstname'] = update.message.text

    text = (
        'Введите Вашу фамилию:'
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )

    return LASTNAME


def get_phone(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.user_data['lastname'] = update.message.text

    text = (
        'Отлично!\nДля регистрации в системе нам необходимо знать '
        'Ваш номер телефона.\nНажмите на кнопку, чтобы поделиться '
        'с нами Вашей контактной информацией.'
    )

    reply_markup = ReplyKeyboardMarkup([[
        KeyboardButton(text='Поделиться контатной информацией', request_contact=True)
    ]], one_time_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )

    return CONTACT


def finish_registration(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    foodapp_api.register_user_api(
        chat_id=chat_id,
        firstname=context.user_data['firstname'],
        lastname=context.user_data['lastname'],
        phone=update.message.contact.phone_number
    )

    if update.message.contact.user_id != update.effective_user.id:
        text = (
            'Хм... что-то не сходится.\n'
            'Давайте вернемся к началу'
        )
        reply_markup = single_button_menu('Повторить регистрацию', str(REGISTER))
    else:
        text = (
            'Приятно познакомиться!\n'
            'Теперь Вы можете оформить свою первую подписку.'
        )
        reply_markup = single_button_menu('Оформить подписку', str(SUBSCRIBE))

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )

    return ConversationHandler.END


if __name__ == "__main__":
    load_dotenv()
    updater = Updater(os.getenv("TG_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(PreCheckoutQueryHandler(get_checkout))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, query_subscription))

    registration_conversation = ConversationHandler(
        entry_points=[
                CallbackQueryHandler(get_firstname, pattern=f'^{str(REGISTER)}$')
            ],
        states={
            FIRSTNAME: [MessageHandler(Filters.text & ~Filters.command, get_lastname)],
            LASTNAME: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
            CONTACT: [MessageHandler(Filters.contact, finish_registration)],
        },
        fallbacks=[
            CommandHandler('start', start)
            ],
        map_to_parent={
            ConversationHandler.END: SHOW_SUB_OR_MENU
        }
    )

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(start, pattern=f'^{str(START)}$')
            ],
        states={
            SHOW_SUB_OR_MENU: [
                registration_conversation,
                CallbackQueryHandler(show_subscriptions, pattern=f'^{str(MY_SUBSCRIPTIONS)}$'),
                CallbackQueryHandler(get_menu_type, pattern=f'^{str(SUBSCRIBE)}$')
            ],
            NUM_PERSONS: [CallbackQueryHandler(get_persons_number)],
            NUM_MEALS: [CallbackQueryHandler(get_meals_number)],
            ALLERGY_OR_PLAN: [
                CallbackQueryHandler(get_plan, pattern='^allergies:Продолжить$'),
                CallbackQueryHandler(get_allergies)
                ],
            INVOICE: [
                CallbackQueryHandler(get_invoice, pattern=f'^{str(INVOICE)}$'),
                CallbackQueryHandler(get_promo),
                MessageHandler(Filters.text & ~Filters.command, save_promo)
                ],
            RECIPE: [CallbackQueryHandler(give_user_recipe)]
        },
        fallbacks=[
            CommandHandler('start', start)
            ]
    )
    dispatcher.add_handler(main_conversation)

    updater.start_polling()
    updater.idle()