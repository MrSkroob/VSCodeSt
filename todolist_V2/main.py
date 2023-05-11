import sqlite3
import datetime

# SETUP
projects_db_file = "projects.db"

db_connection = sqlite3.connect(projects_db_file)

create_table_projects_query = """
CREATE TABLE IF NOT EXISTS projects(
    ProjectId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Title VARCHAR(20) NOT NULL,
    BeginDate DATE,
    Deadline DATE
);
"""

create_table_tasks_query = """
CREATE TABLE IF NOT EXISTS tasks(
    TaskId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ProjectId INTEGER NOT NULL,
    Title VARCHAR(20) NOT NULL,
    Description TEXT,
    Priority INTEGER DEFAULT 1,
    BeginDate DATE,
    Deadline DATE,
    FOREIGN KEY (ProjectId) REFERENCES projects (ProjectId)
);
"""

# priority ranges between 1-10 for now, with 1 being the lowest

db_connection.execute(create_table_projects_query)
projects_cursor = db_connection.cursor()
projects_cursor.execute(create_table_tasks_query)


def print_menu(options: dict):
    print("========MAIN MENU========")
    for i, v in enumerate(options):
        print(i + 1, v)

# forces user to return a valid option of the index of the item 
def choose_option(user_question: str, options: dict, required: bool):
    choice = input(user_question)
    if not required and choice == "":
        return "cancel"
    available_choices = range(len(options))
    while not choice.isnumeric() or (int(choice) - 1) not in available_choices:
        choice = input("Invalid, try again ")
        if choice == "" and not required:
            return "cancel"
    return choice

# forces user to return a valid option of the key of the item
def choose_option_key(user_question: str, options: dict, required: bool):
    choice = input(user_question)
    if not required and choice == "":
        return "cancel"
    available_choices = list(options.keys())
    while choice not in available_choices:
        choice = input("Invalid, try again ")
        if choice == "" and not required:
            return "cancel"
    return choice


def search_for_row_user(cursor: tuple | list):
    print_projects(cursor)
    table_dict = {}
    for i in cursor:
        table_dict[str(i[0])] = i
    table_dict["cancel"] = "cancel"

    if len(table_dict) != 0:
        print("Leave blank to cancel")
        choice = choose_option_key("Choose ID of table ", table_dict, True)
        return choice
    else:
        return "cancel"


def get_date_from_user(user_question: str, required: bool) -> datetime.date | None:
    date = input(user_question)
    date_split = date.split("/")

    if not date_split[0] and not required:
        return None

    while True:
        while len(date_split) != 3:
            date_split = input(user_question).split("/")

        day = date_split[2] or ""
        month = date_split[1] or ""
        year = date_split[0] or ""

        try: # checking all parameters fullfilled and are numbers
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            pass
        else:
            try: # checking if valid date
                datetime.date(year, month, day)
            except ValueError as e:
                print(e)
            else:
                if datetime.date(year, month, day) < datetime.datetime.today().date():
                    print("Must be a future date")
                else:
                    break
        date_split = [""]
    return datetime.date(year, month, day)


def get_string_from_user(user_question: str, min_chars: int, max_chars: int):
    string = input(user_question)
    while min_chars > len(string) or len(string) > max_chars:
        string = input(f"Must be between {min_chars} - {max_chars} characters ")
    return string


def get_int_from_user(user_question, lower_bound: int, upper_bound: int):
    number = input(user_question)
    while not number.isnumeric() or (lower_bound >= int(number) or upper_bound <= int(number)):
        try:
            number = int(input(f"Must be a number between {lower_bound} - {upper_bound} inclusive "))
        except ValueError:
            pass
        else:
            break
    return number


def create_row_project(title: str, start_date: datetime.date, deadline: datetime.date):
    query = """
    INSERT INTO projects (Title, BeginDate, Deadline)
    VALUES (?, ?, ?);
    """
    projects_cursor.execute(query, (title, start_date, deadline))
    db_connection.commit()


def create_task_row(project_id: str, title: str, description: str, priority: int, start_date: datetime.date, deadline: datetime.date):
    query = """
    INSERT INTO tasks (ProjectId, Title, Description, Priority, BeginDate, Deadline)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    projects_cursor.execute(query, (project_id, title, description, priority, start_date, deadline))
    db_connection.commit()


def delete_project_row(id: object):
    project_query = f"""
    DELETE FROM projects 
    WHERE ProjectId = {id};
    """
    task_query = f""""
    DELETE FROM tasks
    WHERE ProjectId = {id}
    """
    db_connection.execute(project_query)
    db_connection.execute(task_query)
    db_connection.commit()



def delete_task_row(id: object):
    query = f""""
    DELETE FROM tasks
    WHERE TaskId = {id}
    """
    db_connection.execute(query)
    db_connection.commit()
    

def create_table_user(): # wrapper function to be run, is a procedure
    today = datetime.datetime.today().date()
    project_name = get_string_from_user("Enter the project name: ", 5, 20)
    start_date = get_date_from_user(f"Enter the start date (leave blank for {today}): ", False) or today
    deadline = get_date_from_user("Enter deadline date (YYYY/MM/DD): ", True)
    create_row_project(project_name, start_date, deadline)


def create_task_user():
    today = datetime.datetime.today().date()

    project_name = get_string_from_user("Enter the task name: ", 5, 20)
    
    description = input("Enter a short description: ")
    priority = get_int_from_user("Enter a priority ", 0, 10)

    start_date = get_date_from_user(f"Enter the start date (leave blank for {today}): ", False) or today
    deadline = get_date_from_user("Enter deadline date (YYYY/MM/DD): ", True)

    table_name = get_string_from_user("Which project is this task for? ", 0, 100)

    query = """
    SELECT * FROM projects
    WHERE Title LIKE ?"""

    cursor = get_table(query, ("%"+table_name+"%",))
    results = cursor.fetchall()

    choice = search_for_row_user(results)

    if choice != "cancel":
        create_task_row(choice, project_name, description, priority, start_date, deadline)


def delete_project_user():
    table_name = get_string_from_user("Enter the project name ", 0, 100)
    query = """
    SELECT * FROM projects
    WHERE Title LIKE ?
    """
    cursor = get_table(query, ("%"+table_name+"%",))

    results = cursor.fetchall()

    choice = search_for_row_user(results)
    
    if choice != "cancel":
        delete_project_row(choice)


def get_table(query: str, parameters=None):
    if parameters is not None:
        cursor = projects_cursor.execute(query, parameters)
    else:
        cursor = projects_cursor.execute(query)
    return cursor


def print_projects(cursor: tuple | list):
    print("========Projects========")
    print("{:<4} {:<24} {:<13} {:<13}".format("ID", "Title", "Start date", "Deadline"))
    for (id, title, date_start, date_end) in cursor:
        print("{:<4} {:<24} {:<13} {:<13}".format(id, title, date_start, date_end))


def print_tasks(cursor: tuple | list):
    print("========Tasks========")
    print("{:<3} {:<21} {:<3} {:<10} {:<10}".format("ID", "Title", "Priority", "Start date", "Deadline"))
    for (id, _, title, priority, date_start, date_end) in cursor:
        print("{:<3} {:<21} {:<3} {:<10} {:<10}".format(id, title, priority, date_start, date_end))


def print_columns(cursor: tuple | list):
    print("========Collumns========")
    for i, v in enumerate(cursor):
        print(i + 1, v[1])


def view_table_user(table: str):
    collumns_query = f"""
    PRAGMA table_info({table})
    """
    collumns = get_table(collumns_query)
    results = collumns.fetchall()
    print_columns(results)
    response = choose_option("Select a column to sort by, leave blank to skip ", results, False)
    if response != "cancel":
        collumn = results[int(response) - 1][1]
    
    query = f"""
    SELECT * FROM {table}
    """

    if response != "cancel":
        query += f"""
        ORDER BY {collumn}
        """

    cursor = get_table(query)
    print_projects(cursor)
    input("Continue ")


def view_projects_user():
    view_table_user("projects")


def view_tasks_user():
    view_table_user("tasks")


options = {
    "Create project": create_table_user,
    "Delete project": delete_project_user,
    "Create task": create_task_user,
    ""
    "View projects": view_projects_user,
    "View tasks": view_tasks_user,
}


def main():
    while True:
        print_menu(options)
        choice = choose_option("Choose an option ", options, True)
        available_keys = list(options.keys())
        options[available_keys[int(choice) - 1]]() # running function in the options dictionary


main()


