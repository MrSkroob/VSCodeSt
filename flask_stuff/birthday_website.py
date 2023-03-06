import datetime
from flask import Flask, request, abort, render_template


app = Flask(__name__)


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    """Returns number of days until next birthday"""
    today = datetime.datetime.today() # create datetime object for right now
    birthdaydate = datetime.datetime(today.year, birthdaymonth, birthdayday) # create datetime object for birthday
    if birthdaydate > today: # check if birthday has passed
        birthdaydate = datetime.datetime(today.year + 1, birthdaymonth, birthdayday)
    difference = birthdaydate - today
    return difference.days, birthdaydate


def calculate_birthday(day: int, month: int, year: int):
    """Wrapper function which will raise error if date is invalid"""
    datetime.datetime(year, month, day)
    days_until_next_birthday(month, day)
    return days_until_next_birthday(month, day)
    

@app.route("/")
def index():
    return render_template("birthday.html")

@app.route("/birthday", methods=["POST"])
def birthday():
    date_str = request.form["date"]
    if date_str == "":
        """No date inputed, default to today"""
        today = datetime.datetime.today()
        day = today.day
        month = today.month
        year = today.year
    else:
        time = date_str.split("-")
        day = int(time[2])
        month = int(time[1])
        year = int(time[0])
    if year and month and day:
        try: 
            days_left, next_birthday = calculate_birthday(day, month, year)
            # just printing stuff in the console
            date = f"{day}/{month}/{year}"
            next_date = f"{next_birthday.day}/{next_birthday.month}/{next_birthday.year}"
            print("today", datetime.datetime.today().date())
            print(f"next birthday:", next_birthday.date())
            print(f"days left: {next_birthday.date() - datetime.datetime.today().date()}")
            return render_template("birthday.html", date=date, next_date=next_date, days=days_left)
        except (ValueError, OverflowError) as exception:
            # handling different errors
            if type(exception) is ValueError:
                return abort(400, description="Invalid date")
            else:
                return abort(400, description="Number too long")
    else:
        return abort(400, description="Missing arguments")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
