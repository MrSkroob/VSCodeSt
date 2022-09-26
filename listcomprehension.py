fruits = ['mango', 'kiwi', 'strawberry', 'guava', 'pineapple', 'mandarin orange']

numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 19, 23, 256, -8, -4, -2, 5, -9]


capitalized_fruits = [i.upper() for i in fruits]
print(capitalized_fruits)

fruits_longer_than_5_letters = [i for i in fruits if len(i) > 5]
print(fruits_longer_than_5_letters)

fruits_with_only_5_letters = [i for i in fruits if len(i) == 5]
print(fruits_with_only_5_letters)

fruits_shorter_than_5_letters = [i for i in fruits if len(i) < 5]
print(fruits_shorter_than_5_letters)