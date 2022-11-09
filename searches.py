import random
import math


def binary_search(array, item):
    lower_bound = 0
    upper_bound = len(array) - 1
    while lower_bound < upper_bound:
        middle = math.ceil((lower_bound + upper_bound) / 2)
        searched = array[middle]
        if searched > item:
            upper_bound = middle - 1
        elif searched < item:
            lower_bound = middle + 1
        else:
            return searched
    return None


def recursive_binary(array, item, lower_bound=None, upper_bound=None):
    if lower_bound is None:
        lower_bound = 0
        upper_bound = len(array) - 1
    if lower_bound > upper_bound: # type: ignore
        # item not found
        return None
    middle = math.ceil((lower_bound + upper_bound) / 2)  # type: ignore
    searched = array[middle]
    if searched > item:
        # search right side
        return recursive_binary(array, item, lower_bound, middle - 1)
    elif searched < item:
        # search left side
        return recursive_binary(array, item, middle + 1, upper_bound)
    else:
        # item found
        return searched



list_to_search = []
for i in range(0, 100):
    list_to_search.append(random.randint(0, 100))

list_to_search.sort()

item_to_search = random.randint(0, 100)
if item_to_search in list_to_search:
    assert recursive_binary(list_to_search, item_to_search) == item_to_search, f"The function should've returned {item_to_search}"
else:
    assert recursive_binary(list_to_search, item_to_search) is None, "The function shouldn't have found anything!"
print(recursive_binary(list_to_search, item_to_search))
# print(binary_search(list_to_search, random.randint(0, 100)))
