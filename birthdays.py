import datetime


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    nowdatetime = datetime.datetime.now()
    birthdaydate = datetime.datetime(nowdatetime.year, birthdaymonth, birthdayday)
    difference = birthdaydate - nowdatetime
    if difference.days < 0:
        birthdaydate = datetime.datetime(nowdatetime.year + 1, birthdaymonth, birthdayday)
    difference = birthdaydate - nowdatetime
    return difference.days


def input_date():
    try:
        day = int(input("Day of your birthday"))
        month = int(input("Month of your birthday"))
        year = int(input("Year of your birthday"))
        datetime.datetime(year, month, day) # forces error to raise if date invalid
    except ValueError:
        return
    print(days_until_next_birthday(month, day), "days until your birthday!")
    

input_date()

