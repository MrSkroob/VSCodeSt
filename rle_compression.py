
def compress(text: str):
    compressed_string = ""
    most_recent_char = ""
    char_count = 0
    for i in text:
        char_count += 1
        if i != most_recent_char:
            if most_recent_char != "":
                compressed_string += most_recent_char + " " + str(char_count) + " "
            char_count = 0
            most_recent_char = i
    compressed_string += text[-1:] + str(char_count + 1)
    return compressed_string


print(compress(input("Input a string to compress\n")))