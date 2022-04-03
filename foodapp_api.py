import os
from urllib.parse import urljoin
import requests


def add_subscription_api(chat_id, cousine_type, allergies, num_persons, num_servings, plan):
    '''Add subscription based on arguments'''

    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/addSubscription')

    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id,
        'cousine_type': cousine_type,
        'allergies': allergies,
        'num_persons': num_persons,
        'num_servings': num_servings,
        'plan': plan
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()


def get_subscriptions_api(chat_id):
    '''Get subscription based on chat_id'''
    
    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/getSubscriptions')

    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['subs']


def register_user_api(chat_id, firstname, lastname, phone):
    '''Register user based on credentials'''
    
    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/registerUser')

    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id,
        'firstname': firstname,
        'lastname': lastname,
        'phone': phone
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['id']


def get_user_api(chat_id):
    '''Get user data by chat_id'''

    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/getUser')

    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()


def get_reference_api():
    '''Get reference dictionary for constant values'''

    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/getReference')

    response = requests.post(url)
    response.raise_for_status()

    return response.json()


def get_recipe(sub_id):
    '''Get random recipe based on sub_id'''

    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, 'api/getRecipe')

    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'sub_id': sub_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['recipe']


def get_image_from_server(img_name):
    '''Get image from server directory'''

    host_address = os.getenv('APP_HOST', 'http://127.0.0.1:5000')
    url = urljoin(host_address, f'images/{img_name}')

    response = requests.get(url)
    response.raise_for_status()

    return response.content
    

def main():
    pass


if __name__ == "__main__":
    main()
