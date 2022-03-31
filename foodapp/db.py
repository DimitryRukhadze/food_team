from enum import Enum

from flask import current_app, g
from tinydb import TinyDB


class Schema(Enum):
    USER = 'User'
    SUBSCRIPTION = 'Subscription'
    RECIPE = 'Recipe'


FIELD_LISTS = {
    'cousine_types': [
        'Классическое',
        'Низкоуглеводное',
        'Вегетарианское',
        'Кето'],
    'allergies': [
        'Рыба и морепродукты',
        'Мясо',
        'Зерновые',
        'Продукты пчеловодства',
        'Орехи и бобовые',
        'Молочные продукты'
    ]
}


def test_get_sample_recipe():
    return {
        "name": "Тестовый рецепт 1",
        "description": (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore"
            "et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
            "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cil"
            "lum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa "
            "qui officia deserunt mollit anim id est laborum."),
        "img_url": "images/1.png",
        "cousine_type": "Классическое",
        "contains": ["Мясо", "Зерновые"],
        "calories": 420,
        "steps": [
            {
                "num": 0,
                "title": "Заголовок шага 1",
                "text": "Описание шага 1"
            },
            {
                "num": 1,
                "title": "Заголовок шага 2",
                "text": "Описание шага 2"
            }
        ],
        "ingredients": [
            {
                "pos": 0,
                "name": "Ингредиент 1",
                "countable": True,
                "amount": 500,
                "units": "г"
            },
            {
                "pos": 1,
                "name": "Ингредиент 2",
                "countable": True,
                "amount": 1,
                "units": "шт"
            },
            {
                "pos": 2,
                "name": "Ингредиент 3",
                "countable": True
            }
        ]
    }


def get_database():
    if 'db' not in g:
        database_path = current_app.config['DATABASE']
        g.db = TinyDB(database_path)

    return g.db
