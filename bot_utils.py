import json
from datetime import datetime

import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def present_subscriptions(user_subs):
    pretty_view = []
    tz = pytz.timezone('Europe/Moscow')
    for sub in user_subs:
        expiration_date = datetime.fromtimestamp(sub["expires_on"], tz)
        view = {
            "Номер подписки": sub["id"],
            "Тип меню": sub["cousine_type"],
            "Действует до": expiration_date
            }
        pretty_view.append(view)
    return pretty_view


def get_date_from_timestamp(timestamp):
    tz = pytz.timezone('Europe/Moscow')
    return datetime.fromtimestamp(timestamp, tz).strftime('%d.%m.%Y')


def customize_menu(field, menu_names, cols=''):
    if not cols and not len(menu_names)%2:
        cols = 2
    elif not cols:
        cols = 3

    menu_buttons = [
        InlineKeyboardButton(type, callback_data=f'{field}:{type}')
        for type in menu_names
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(menu_buttons, n_cols=cols))

    return reply_markup

def customize_menu_2(subs, cols=''):
    if not len(subs.keys())%2:
        cols = 2
    else:
        cols = 3
    menu_buttons = [
        InlineKeyboardButton(value, callback_data=key)
        for key, value in subs.items()
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(menu_buttons, n_cols=1))
    return reply_markup


def build_menu(buttons, n_cols):
    menu = [
        buttons[button:button + n_cols]
        for button in range(0, len(buttons), n_cols)
    ]

    return menu


def get_plural_for_person(amount):
    if amount > 20 or amount < 1:
        raise ValueError
    elif amount == 1:
        return '1 персону'
    elif 1 < amount < 5:
        return f'{amount} персоны'
    else:
        return f'{amount} персон'

    
def get_plural_for_servings(amount):
    if amount > 20 or amount < 1:
        raise ValueError
    elif 0 < amount < 5:
        return f'{amount} порции'
    else:
        return f'{amount} порций'


def get_readable_allergies(allergies):
    return ', '.join(allergies).lower()


def show_recipe(recipe):
    # content = get_json_content("./recipe_maker/food_menu.json")
    recipe_description = recipe['description']
    calories = recipe["calories"]
    allergens = ', '.join(recipe['contains']).lower()
    steps = [
        f'\n\t<i>{step["title"]}</i> \n{step["text"]}'
        for step in recipe["steps"]
    ]
    steps_as_text = ''.join(steps)

    ingredients = []
    for ingredient in recipe['ingredients']:
        if ingredient['countable'] and ingredient['units']:
            line = f'\n\t{ingredient["name"]} - {ingredient["amount"]} {ingredient["units"]}'
        else:
            line = f'\n\t{ingredient["name"]}'
        ingredients.append(line)
    ingredients_as_text = '; '.join(ingredients).lower()
    image_name = recipe['img_name']
    # ужасная f строка, но пока оставил так на первое время
    text = (
        f'\n<b><i>{recipe["name"]}</i></b>'
        f'\n<b>Меню:</b> {recipe["cousine_type"]}'
        f'\n<b>Описание рецепта:</b> {recipe_description}'
        f'\n<b>Ингредиенты:</b> {ingredients_as_text}'
        f'\n<b>Пищевая ценность:</b> {recipe["calories"]} Ккал'
        f'\n<b>Содержит:</b> {allergens}'
        f'\n<b>Как приготовить:</b> {steps_as_text}'
    )
    return text, image_name