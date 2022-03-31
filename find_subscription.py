import json

def get_json_content(json_file):
    """ Читает json файлы, возвращает содержимое """
    with open(json_file, "r", encoding="utf_8") as file:
        file_contents = file.read()
        content = json.loads(file_contents)
        return content


def get_subscriptions(user_id, subs):
    user_subs = []
    for sub in subs["subscriptions"]:
        if sub["user_id"] == user_id:
            user_subs.append(sub)
    return user_subs


def present_subscriptions(user_subs):
    pretty_view = []
    for sub in user_subs:
        view = {
            "Номер подписки": sub["id"],
            "Название подписки": sub["cousine_type"],
            "Действует до": sub["expires_on"]
            }
        pretty_view.append(view)
    return pretty_view
