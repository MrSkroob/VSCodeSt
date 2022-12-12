import json
import random
import urllib.request


def get_ingredients(drink):
    ingredients = []
    index = 1
    while True:
        try:
            ingredient = drink[f"strIngredient{index}"]
            if ingredient is None:
                break
            ingredients.append(ingredient)
        except KeyError:
            break
        index += 1
    return ingredients


def get_supported_languages_for(drink):
    supported_languages = []
    for i in drink.keys():
        if i[:15] == "strInstructions":
            language = i[15:]
            if not language:
                supported_languages.append("EN")
            elif drink[f"strInstructions{language}"]:
                supported_languages.append(language)
    return supported_languages


def get_instructions(drink, language: str):
    return drink["strInstructions" + language]


def main():
    drink = None
    while True:
        while drink is None:
            drink_type = input("What drink do you want to know about?")
            url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink_type
            data = urllib.request.urlopen(url).read().decode()
            readable = json.loads(data)
            if readable["drinks"][0] is not None:
                drink = random.choice(readable["drinks"])

        print("Available languages:")
        languages = get_supported_languages_for(drink)
        for i, v in enumerate(languages):
            print(i + 1, v)

        language_index = None
        while language_index not in range(1, len(languages) + 1):
            language_index = input("Which language do you want?")
            if language_index.isnumeric():
                language_index = int(language_index)
        language = languages[language_index - 1]
        if language == "EN":
            language = ""

        print("Ingredients: ")
        for i, v in enumerate(get_ingredients(drink)):
            print(i + 1, v)
            
        print(get_instructions(drink, language))
        if input("New drink?").lower()[0] == "y":
            drink = None
       

main()