import json
import math


# opens json file and returns its contents
def get_file_data(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# updates the json file with new data
def update_file(filepath: str, new_data: dict):
    with open(filepath, "w") as f:
        f.seek(0) # move cursor to the start of the file
        json.dump(new_data, f)
        f.truncate() # incase the updated data is less


def find_dict_in_list(dict_list: list, key: str):
    for i, v in enumerate(dict_list):
        if key in v:
            return i, v
    return None, None

# mostly did this to try and learn how classes worked
class Student():
    def __init__(self, name: str, group: str) -> None:
        self.name = name
        self.group = group
        self.scores = {}

    # gets student data from database, if any
    def extract(self, jsondata: dict):
        if self.group in jsondata:
            _, student = find_dict_in_list(jsondata[self.group], self.name)
            if student is not None:
                self.scores = student[self.name]
                return True
        return False
    
    # updates the database with the student data
    def update(self, jsondata: dict):
        if self.group in jsondata:
            index, _ = find_dict_in_list(jsondata[self.group], self.name)
            if index is not None: # i don't know why a simple 'if index' doesn't work.
                jsondata[self.group][index] = {self.name: self.scores}
            else:
                jsondata[self.group].append({self.name: self.scores})
        else:
            jsondata[self.group] = [{self.name: self.scores}]


schooldata = get_file_data("scores.json")


"""jacob = Student("Jacob", "Lower 6th")
jacob.extract(schooldata)
print(jacob.scores)
jacob.update(schooldata)
update_file("scores.json", schooldata)"""


# asks yes or no question
def ask_question(question):
    answer = None
    valid_responses = {"yes": True, "no": False, "y": True, "n": False, "": True}
    while answer not in valid_responses:
        answer = input(question).lower()
    return valid_responses[answer]


def display_menu(groupname: str):
    print("MENU FOR", groupname)
    print("Option 1: change your class")
    print("Option 2: enter student test scores")
    print("Option 3: display class average")
    print("Option 4: display class list")
    print("Option 5: quit")


def enter_student_scores(group: str):
    print("Reply with q when asked the student name to quit")
    testname = input("Please enter the exam name\n")
    while True:
        try:
            studentname = input("Please enter the student name\n")
            if studentname == "q":
                break
            student = Student(studentname, group)
            if student.extract(schooldata) or ask_question("This student has no data. Continue? (y/n)\n"):
                score = input("Please enter their score\n")
                student.scores[testname] = int(score)
            print("Student name:", studentname)
            print("Score:", score)
            print("Exam:", testname)
            if ask_question("Is this correct?\n"):
                student.update(schooldata)
            del student
        except ValueError:
            print("Invalid score.")
            pass
    if ask_question("Apply changes (y/n)?"):
        update_file("scores.json", schooldata)


def display_average(group: str):
    testname = input("Input the exam name\n")
    scores = []
    if group not in schooldata:
        print("No data to display")
        return
    for i in schooldata[group]:
        studentname = next(iter(i)) # gets first key in dictionary. Python 3.7+ supported!!!!
        student = i[studentname]
        if testname in student: # checks if the student has data related to the test
            scores.append(student[testname])
        else:
            print("WARNING: no data for", studentname)
    if len(scores) == 0:
        print("Average: 0.0")
    else:
        print("Average: ", math.floor((sum(scores) / len(scores)) + 0.5))


def display_class(group: str):
    if group not in schooldata:
        print("No data to display")
        return
    for i in schooldata[group]:
        print(next(iter(i)))


def main():
    valid_options = ["1", "2", "3", "4", "5"]
    group = ""
    while True:
        # enter class details
        while not group:
            group = input("Good day, please enter the class you teach.\n")
            if group in schooldata:
                break
            elif ask_question("Couldn't find your class. Do you want to continue (y/n)?\n"):
                break
        display_menu(group)
        option = None
        while option not in valid_options:
            option = input("What do you want to do (1-5)?\n").strip()
        if option == "1":
            group = ""
        elif option == "2":
            enter_student_scores(group)
        elif option == "3":
            display_average(group)
        elif option == "4":
            display_class(group)
        elif option == "5":
            return
                        
main()