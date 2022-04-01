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


def get_database():
    if 'db' not in g:
        database_path = current_app.config['DATABASE']
        g.db = TinyDB(database_path)

    return g.db
