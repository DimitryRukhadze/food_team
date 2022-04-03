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

def customize_menu_2(sub_id, menu_names, cols=''):
    if not len(menu_names)%2:
        cols = 2
    else:
        cols = 3
    menu_buttons = [
        InlineKeyboardButton(type, callback_data=sub_id)
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

# def get_json_content(json_file):
#     """ Читает json файлы, возвращает содержимое """
#     with open(json_file, "r", encoding="utf_8") as file:
#         file_contents = file.read()
#         content = json.loads(file_contents)
#         return content


# def get_subscriptions(user_id, subs):
#     user_subs = []
#     for sub in subs["subscriptions"]:
#         if sub["user_id"] == user_id:
#             user_subs.append(sub)
#     return user_subs


def show_recipe(content):
    # content = get_json_content("./recipe_maker/food_menu.json")
    recepi_name = content[0]["name"]
    recepi_description = content[0]["description"].replace(".", "\.")
    cousine = content[0]["cousine_type"]
    calories = content[0]["calories"]
    steps_content = []
    new_ingredient = []
    allergens = ", ".join(content[0]["contains"]).lower()
    for step in content[0]["steps"]:
        line = ""
        name = step["title"]
        text = step["text"]
        line = f"_\n{name}:_\n{text}"
        steps_content.append(line)
    steps = "".join(steps_content)
    for ingredient in content[0]["ingredients"]:
        line = ""
        name = ingredient["name"]
        if ingredient["countable"]:
            amount = ingredient["amount"]
            units = ingredient["units"]
            line = f"\n{name} \- {amount} {units}"
        else:
            line = f"\n{name}"
        new_ingredient.append(line)
    ingredients = ";".join(new_ingredient).lower()
    image_url = content[0]["img_url"]
    # ужасная f строка, но пока оставил так на первое время
    text = f"*_\n{recepi_name}_*\n*Меню:* {cousine} \n*Описание рецепта:* {recepi_description}\n*Ингредиенты:* {ingredients}\n*Калории:* {calories} Ккал\n*Аллергены:* {allergens}\n*Шаги:* {steps}"
    return text, image_url