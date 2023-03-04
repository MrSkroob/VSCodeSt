import datetime
from flask import Flask, request, abort, render_template


app = Flask(__name__)


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    """Returns number of days until next birthday"""
    nowdatetime = datetime.datetime.now() # create datetime object for right now
    birthdaydate = datetime.datetime(nowdatetime.year, birthdaymonth, birthdayday) # create datetime object for birthday
    difference = birthdaydate - nowdatetime
    if difference.days < 0: # check if birthday has passed
        birthdaydate = datetime.datetime(nowdatetime.year + 1, birthdaymonth, birthdayday)
        difference = abs(birthdaydate - nowdatetime) # calculate difference again
    return difference.days + 1


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
        day = today.day - 1
        month = today.month
        year = today.year
    else:
        time = date_str.split("-")
        day = int(time[2])
        month = int(time[1])
        year = int(time[0])
    if year and month and day:
        try: 
            days_left = calculate_birthday(day, month, year)
            # just printing stuff in the console
            print(f"date: {day}/{month}/{year}")
            print(f"days left: {days_left}")
            return f"Days left until your birthday: {days_left}"
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