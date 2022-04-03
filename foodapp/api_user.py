import random
import time
from datetime import datetime, timedelta
from flask import Blueprint
from tinydb import Query

from foodapp.db import get_database, Schema, REFERENCE
from webargs import fields
from webargs.flaskparser import use_args


user_bp = Blueprint('user', __name__, url_prefix='/api')


new_user_args = {
    'bot_token': fields.Str(required=True),
    'chat_id': fields.Int(required=True),
    'firstname': fields.Str(required=True),
    'lastname': fields.Str(required=True),
    'phone': fields.Str(required=True)
}


@user_bp.route('/registerUser', methods=['POST'])
@use_args(new_user_args)
def register_user_api(args):
    db = get_database()
    users = db.table(Schema.USER.name)

    new_user = {
        'chat_id': args['chat_id'],
        'firstname': args['firstname'],
        'lastname': args['lastname'],
        'phone': args['phone'],
        'joined_on': int(time.time())
    }

    new_user_id = users.insert(new_user)


    return {'id': new_user_id}


get_user_args = {
    'bot_token': fields.Str(required=True),
    'chat_id': fields.Int(required=True),
}


@user_bp.route('/getUser', methods=['POST'])
@use_args(get_user_args)
def get_user_api(args):
    db = get_database()
    users = db.table(Schema.USER.name)
    user = users.get(Query()['chat_id'] == args['chat_id'])

    return {'id': user.doc_id if user else 0}


add_user_subscription_args = {
    'bot_token': fields.Str(required=True),
    'chat_id': fields.Int(required=True),
    'cousine_type': fields.Str(required=True, validate=lambda val: val in REFERENCE['cousine_types']),
    'allergies': fields.List(fields.Str(validate=lambda val: val in REFERENCE['allergies'])),
    'num_persons': fields.Int(missing=4),
    'num_servings': fields.Int(missing=6),
    'plan': fields.Int(required=True)
}


@user_bp.route('/addSubscription', methods=['POST'])
@use_args(add_user_subscription_args)
def add_user_subscription_api(args):
    db = get_database()
    subscriptions = db.table(Schema.SUBSCRIPTION.name)

    current_date = datetime.now()
    expiration_date = current_date + timedelta(weeks=args['plan']*4)
    new_plan = {
        'chat_id': args['chat_id'],
        'cousine_type': args['cousine_type'],
        'allergies': args['allergies'],
        'num_persons': args['num_persons'],
        'num_servings': args['num_servings'],
        'acquired_on': int(current_date.timestamp()),
        'expires_on': int(expiration_date.timestamp())
    }

    subscription_id = subscriptions.insert(new_plan)
    new_subcription = subscriptions.get(doc_id = subscription_id)
    return {'id': subscription_id, 'data': new_subcription}


@user_bp.route('/getSubscriptions', methods=['POST'])
@use_args(get_user_args)
def get_user_subscriptions_api(args):
    db = get_database()
    subs = db.table(Schema.SUBSCRIPTION.name)
    user_subs = subs.search(Query()['chat_id'] == args['chat_id'])
    for user_sub in user_subs:
        user_sub['id'] = user_sub.doc_id
    return {'subs': user_subs}


get_recipe_args = {
    'bot_token': fields.Str(required=True),
    'sub_id': fields.Int(required=True)
}


@user_bp.route('/getRecipe', methods=['POST'])
@use_args(get_recipe_args)
def get_recipe_api(args):
    db = get_database()
    subs = db.table(Schema.SUBSCRIPTION.name)
    sub = subs.get(doc_id=args['sub_id'])

    if not sub:
        return {'recipe': -1}

    recipe_table = db.table(Schema.RECIPE.name)
    Recipe = Query()
    recipes = recipe_table.search(
        (Recipe.cousine_type == sub['cousine_type'])
        & (~ (Recipe.contains.any(sub['allergies'])))
        )
    
    print(recipes)

    result = random.choice(recipes)

    return {'recipe': result if result else -1}


@user_bp.route('/getReference', methods=['POST'])
def get_reference():
    return {
        'plans': REFERENCE['plans'],
        'cousine_types': REFERENCE['cousine_types'],
        'allergies': REFERENCE['allergies']
    }