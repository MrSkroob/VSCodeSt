import datetime

tasks = []

def ask_question(question):
    answer = None
    valid_responses = {"yes": True, "no": False, "y": True, "n": False, "": True}
    while answer not in valid_responses:
        answer = input(question).lower()
    return valid_responses[answer]


def print_tasks():
    print("LIST OF TASKS:")
    tasks.sort(key=lambda v: (v.done, v.duedate)) # will push tasks that aren't done to the top
    for i, v in enumerate(tasks):
        print(f"{i}:")
        v.print_task()

class Task():
    def __init__(self, taskname: str, duedate: datetime.date, description=None) -> None:
        today = datetime.datetime.today().date()
        daysleft = duedate - today
        self.title = taskname
        self.description = description or "No description"
        self.duedate = duedate
        self.daysleft = daysleft
        self.done = False
    
    def print_task(self):
        today = datetime.datetime.today().date()
        daysleft = self.duedate - today
        self.daysleft = daysleft
        for i in vars(self).items():
            print(f"{i[0]}: {i[1]}")


def main():
    hour = datetime.datetime.now().hour
    if hour < 12:
        print("Good morning.")
    elif 17 > hour > 12:
        print("Good afternoon.")
    else:
        print("Good evening.")

    valid_inputs = ["1", "2", "3", "4"]
    while True:
        print("""MENU
        1. Add a task
        2. Remove a task
        3. View all tasks
        4. Mark task as done/todo
        5. Quit
        """)
        selection = ""
        while selection not in valid_inputs:
            selection = input("What would you like to do today?\n")
        if selection == "1":
            title = input("Title of task\n")
            description = input("Description of task (if needed)\n")
            days = None
            try:
                days = int(input("How many days from today is it due?\n"))
            except ValueError:
                print("Invalid day")
            if days is not None:
                duedate = datetime.datetime.today().date() + datetime.timedelta(days=days)
                if ask_question("Confirm: (y/n)\n"):
                    tasks.append(Task(title, duedate, description))
        elif selection == "2":
            print_tasks()
            index = None
            if len(tasks) > 0:
                try:
                    index = int(input(f"Which task do you want to remove? (0 - {len(tasks) - 1})"))
                except ValueError:
                    pass
                if index is not None:
                    print("TASK SELECTED:")
                    tasks[index].print_task()
                    if ask_question("Confirm: (y/n)\n"):
                        tasks.pop(index)
            else:
                print("No tasks to display.")
        elif selection == "3":
            print_tasks()
        elif selection == "4":
            print_tasks()
            index = None
            if len(tasks) > 0:
                try:
                    index = int(input(f"Which task do you want to mark as done/todo? (0 - {len(tasks) - 1})"))
                except ValueError:
                    pass
                if index is not None:
                    print("TASK SELECTED:")
                    tasks[index].print_task()
                    if ask_question("Confirm: (y/n)\n"):
                        tasks[index].done = not tasks[index].done
            else:
                print("No tasks to display")
        elif selection == "5":
            break

main()