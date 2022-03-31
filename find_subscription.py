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


def get_recipe():
    content = get_json_content("./recipe_maker/food_menu.json")
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