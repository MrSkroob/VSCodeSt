import csv

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
        return ",".join([str(i) for i in headers])
    
    def get_csv_entry(self):
        _, attributes = self._get_csv_data()
        return ",".join([str(i) for i in attributes])


def save_to_file(file: str, data: list):
    with open(file, "w") as f:
        f.write(data[0].get_headers()) # write the header
        for i in data:
            f.write(i.get_csv_entry()) # Write the csv entries 


def save_to_file_csv(file: str, data: list):
    """Works similar to save_to_file but uses the csv module"""
    if file.split(".")[1] != "csv":
        raise TypeError("Wrong file format")
    with open(file, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        assert not "\n" in data[0].get_headers()
        writer.writerow(data[0].get_headers().strip().split(","))
        for i in data:
            assert not "\n" in i.get_csv_entry()
            writer.writerow(i.get_csv_entry().strip().split(","))


def read_from_csv(file: str) -> list:
    if file.split(".")[1] != "csv":
        raise TypeError("Wrong file format")
    with open(file, "r") as f:
        data_list = []
        reader = csv.reader(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for i in reader:
            print(i)
            # data_list.append(Engine(i[0], i[1], i[2]))
        return data_list


def read_from(file: str) -> list:
    with open(file, "r") as f:
        f.readline() # advances the pointer by 1 line to skip the header
        data_list = []
        for line in f:
            if line != "\n":
                line = line.strip("\n")
                engine_data = line.split(",")
                data_list.append(Engine(engine_data[0], engine_data[1], engine_data[2]))
        return data_list


engines_list = []
engines_list.append(Engine('Thomas', 6000, 'blue'))
engines_list.append(Engine('Percy', 600, 'Green'))
engines_list.append(Engine('James', 650, 'red'))
engines_list.append(Engine('Edward', 1000, 'blue'))
engines_list.append(Engine('Gordon', 2500, 'blue'))
engines_list.append(Engine('Henry', 2100, 'green'))

# save_to_file("csv_practice.csv", engines_list)
save_to_file_csv("csv_practice.csv", engines_list)
engines_list = read_from_csv("csv_practice.csv") # read_from("csv_practice.csv")
for e in engines_list:
    e.display_engine()

