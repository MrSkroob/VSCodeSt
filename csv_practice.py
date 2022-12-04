# name = ["Tom", "Dick", "Harry"]
# age = [12, 15, 16]
# fav_colour = ["red", "blue", "green"]
# with open("csv_practice.csv", "w") as f:
#     for x, y, z in zip(name, age, fav_colour):
#         f.write(f"{x}, {y}, {z}\n")
class Engine:
    def __init__(self, name, weight, colour):
        self.name = name
        self.weight = weight
        self.colour = colour

    def display_engine(self):
        print(f"Engine name: {self.name}, weight: {self.weight}, colour: {self.colour}")
    
    def _get_csv_data(self):
        attributes = self.__dict__.items()
        unzipped = list(zip(*attributes)) # * operator tells zip to unzip list
        headers = unzipped[0]
        attributes = unzipped[1]
        return headers, attributes

    def get_headers(self):
        headers, _ = self._get_csv_data()
        return ", ".join([str(i) for i in headers]) + "\n"
    
    def get_csv_entry(self):
        _, attributes = self._get_csv_data()
        return ", ".join([str(i) for i in attributes]) + "\n"


engines_list = []
engines_list.append(Engine('Thomas', 600, 'blue'))
engines_list.append(Engine('James', 650, 'red'))
engines_list.append(Engine('Edward', 1000, 'blue'))
engines_list.append(Engine('Gordon', 2500, 'blue'))
engines_list.append(Engine('Henry', 2100, 'green'))

print(engines_list)
for e in engines_list:
    e.display_engine()

if input("running this program will create a new csv file EACH TIME. reply with 'n' to cancel.").lower() == "n":
    pass
else:
    with open("engines.csv", "x") as f:
        f.write(engines_list[0].get_headers())
        for i in engines_list:
            f.write(i.get_csv_entry())
