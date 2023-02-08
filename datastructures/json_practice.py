import json
import urllib.request


def get_ingredients(drink):
    ingredients = []
    index = 1
    while True:
        try:
            ingredient = drink[f"strIngredient{index}"]
            quantity = drink[f"strMeasure{index}"]
            if ingredient is None:
                break
            if quantity is not None:
                quantity = quantity.strip()
            ingredients.append(f"{ingredient} ({quantity})")
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
    if language == "EN":
        language = ""
    return drink["strInstructions" + language]


def print_list(title: str, contents: list):
    print(title)
    for i, v in enumerate(contents):
        print(i + 1, v)


def get_valid_input_from_list(question: str, list_to_pick_from: list):
    index = None
    while index not in range(1, len(list_to_pick_from) + 1):
        index = input(question)
        if index.isnumeric():
            index = int(index)
    return list_to_pick_from[index - 1], index - 1


def main():
    drink = None
    while True:
        while drink is None:
            drink_type = input("What drink do you want to know about?")
            url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink_type
            data = urllib.request.urlopen(url).read().decode()
            readable = json.loads(data)
            selectable_drinks = [i["strDrink"] for i in readable["drinks"]]
            if selectable_drinks:
                break
            else:
                print("No results found, please check your spelling")

        print_list("Drinks found:", selectable_drinks)
        _, drink_index = get_valid_input_from_list("Select a drink: ", selectable_drinks)
        drink = readable["drinks"][drink_index]

        print("Drink selected:", drink["strDrink"])

        languages = get_supported_languages_for(drink)
        print_list("Available languages:", languages)

        language, _ = get_valid_input_from_list("Select a language: ", languages)
        
        print_list("Ingredients:", get_ingredients(drink))
        print(get_instructions(drink, language))

        valid_options = ["New drink", "Choose from list before"]
        print_list("What next?", valid_options)
        _, index = get_valid_input_from_list("Select an option: ", valid_options)
        if index == 0:
            drink = None
        elif index == 1:
            pass
       
main()