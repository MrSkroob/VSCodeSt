import datetime


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    nowdatetime = datetime.datetime.now() # create datetime object for right now
    birthdaydate = datetime.datetime(nowdatetime.year, birthdaymonth, birthdayday) # create datetime object for birthday
    difference = birthdaydate - nowdatetime
    if difference.days < 0: # check if birthday has passed
        birthdaydate = datetime.datetime(nowdatetime.year + 1, birthdaymonth, birthdayday)
        difference = abs(birthdaydate - nowdatetime) # calculate difference again
    return difference.days + 1


def input_date():
    try:
        day = int(input("Day of your birthday"))
        month = int(input("Month of your birthday"))
        year = int(input("Year of your birthday"))
        datetime.datetime(year, month, day) # forces error to raise if date invalid
    except ValueError:
        return
    daysleft = days_until_next_birthday(month, day)
    if daysleft == 365:
        print("Happy birthday!")
    else:
        print(daysleft, f"day{'s'[:daysleft!=1]} left until your birthday!")
        # ^ is exclusive or in python (!= also works!)
        #'s'[:False] returns None while 's'[:True] returns s
        

input_date()
