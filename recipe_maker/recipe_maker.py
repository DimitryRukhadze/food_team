import json


from pathlib import Path
from transliterate import translit, get_available_language_codes


def open_recipes_json():

    with open('food_menu.json', 'r') as file:
        recipes_json = json.loads(file.read())

    return recipes_json


def update_recipes_json(new_menu):

    with open('food_menu.json', 'w') as file:
        json.dump(new_menu, file)


def add_recipe():
    recipe_structure = get_recipe_structure()

    new_recipe = recipe_structure.copy()
    new_recipe['name'] = translit(input('Введите название рецепта: '), language_code='ru', reversed=True)

    recipes = open_recipes_json()
    recipes.append(new_recipe)

    update_recipes_json(recipes)


def get_recipe_structure():
    recipes = open_recipes_json()
    recipe_structure = recipes[0].fromkeys(recipes[0],'')

    return recipe_structure



if __name__ == '__main__':
    img_path = Path('recipe_img')
    img_names = [img_name.name for img_name in img_path.iterdir()]
