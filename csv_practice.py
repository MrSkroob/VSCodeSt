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
        attributes = self.__dict__.items() # __dict__ gets all attributes of the class. 
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


def save_to_file(file: str, data: list):
    with open(file, "w") as f:
        f.write(data[0].get_headers()) # write the header
        for i in data:
            f.write(i.get_csv_entry()) # Write the csv entries 


def read_from(file: str) -> list:
    with open(file, "r") as f:
        data_list = []
        for line in f:
            line = line.strip("\n")
            engine_data = line.split(", ")
            data_list.append(Engine(engine_data[0], engine_data[1], engine_data[2]))
        return data_list


engines_list = []
engines_list.append(Engine('Thomas', 600, 'blue'))
engines_list.append(Engine('Percy', 600, 'Green'))
engines_list.append(Engine('James', 650, 'red'))
engines_list.append(Engine('Edward', 1000, 'blue'))
engines_list.append(Engine('Gordon', 2500, 'blue'))
engines_list.append(Engine('Henry', 2100, 'green'))

save_to_file("csv_practice.csv", engines_list)
engines_list = read_from("csv_practice.csv")
for e in engines_list:
    e.display_engine()
    