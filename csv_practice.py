name = ["Tom", "Dick", "Harry"]
age = [12, 15, 16]
fav_colour = ["red", "blue", "green"]
with open("csv_practice.csv", "w") as f:
    for x, y, z in zip(name, age, fav_colour):
        f.write(f"{x}, {y}, {z}\n")
