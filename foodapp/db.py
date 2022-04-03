from enum import Enum

from flask import current_app, g
from tinydb import TinyDB


USER = 'User'
SUBSCRIPTION = 'Subscription'
RECIPE = 'Recipe'


REFERENCE = {
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
    ],
    'plans': [
        {'name': '1 месяц', 'price' : 100, 'duration': 1},
        {'name': '3 месяца', 'price' : 285, 'duration': 3},
        {'name': '6 месяцев', 'price' : 550, 'duration': 6},
        {'name': '12 месяцев', 'price' : 1000, 'duration': 12}
    ]
}


def get_database():
    if 'db' not in g:
        database_path = current_app.config['DATABASE']
        g.db = TinyDB(database_path)

    return g.db
