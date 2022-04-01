import requests


def add_subscription_api(chat_id, cousine_type, allergies, num_persons, num_servings):
    url = 'http://127.0.0.1:5000/api/addSubscription'
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'bot_token':'123',
        'chat_id': chat_id,
        'cousine_type': cousine_type,
        'allergies': allergies,
        'num_persons': num_persons,
        'num_servings': num_servings
    }

    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()

    return response.json()['id']


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


def main():
    pass


if __name__ == "__main__":
    main()
