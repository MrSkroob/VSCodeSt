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


def merge(array_L, array_R, array):
    i, j = 0, 0
    l_size = len(array_L)
    r_size = len(array_R)
    arr_size = len(array)
    while i + j < arr_size:
        if j == r_size or (i < l_size and array_L[i] < array_R[i]):
            array[i + j] = array_L[i]
            i += 1
        else:
            array[i + j] = array_R[j]
            j += 1
    # if add_pointer == len(array) - 1:
    #     return
    # if left_pointer == len(array_L) - 1:
    #     data = array_R[right_pointer]
    #     right_pointer += 1
    # elif right_pointer == len(array_R) - 1:
    #     data = array_L[left_pointer]
    #     left_pointer += 1
    # else:
    #     if array_L[left_pointer] < array_R[right_pointer]:
    #         data = array_L[left_pointer]
    #         left_pointer += 1
    #     else:
    #         data = array_R[right_pointer]
    #         right_pointer += 1
    # array[add_pointer] = data
    # add_pointer += 1
    # merge(array_L, array_R, array, left_pointer, right_pointer, add_pointer)


def merge_sort(array):
    size = len(array)
    if size < 2:
        return
    middle = size // 2
    array_L = array[0:middle]
    array_R = array[middle:size]

    merge_sort(array_L)
    merge_sort(array_R)
    merge(array_L, array_R, array)



list_to_search = []
for i in range(0, 100):
    list_to_search.append(random.randint(0, 100))


merge_sort(list_to_search)
print(list_to_search)