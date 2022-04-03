import requests


def add_subscription_api(chat_id, cousine_type, allergies, num_persons, num_servings, plan):
    url = 'http://127.0.0.1:5000/api/addSubscription'
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
    url = 'http://127.0.0.1:5000/api/getSubscriptions'
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['subs']


def register_user_api(chat_id, firstname, lastname, phone):
    url = 'http://127.0.0.1:5000/api/registerUser'
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
    url = 'http://127.0.0.1:5000/api/getUser'
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['id']


def get_reference_api():
    url = 'http://127.0.0.1:5000/api/getReference'

    response = requests.post(url)
    response.raise_for_status()

    return response.json()


def get_recipe(sub_id):
    url = 'http://127.0.0.1:5000/api/getRecipe'
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'sub_id': sub_id
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['recipe']


def main():
    pass


if __name__ == "__main__":
    main()
