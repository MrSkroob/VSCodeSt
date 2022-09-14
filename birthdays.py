import datetime


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    nowdatetime = datetime.datetime.now() # create datetime object for right now
    birthdaydate = datetime.datetime(nowdatetime.year, birthdaymonth, birthdayday) # create datetime object for birthday
    difference = nowdatetime - birthdaydate
    if difference.days < 0: # check if birthday has passed
        birthdaydate = datetime.datetime(nowdatetime.year + 1, birthdaymonth, birthdayday)
        difference = nowdatetime - birthdaydate # calculate difference again
    return difference.days


def input_date():
    try:
        day = int(input("Day of your birthday"))
        month = int(input("Month of your birthday"))
        year = int(input("Year of your birthday"))
        datetime.datetime(year, month, day) # forces error to raise if date invalid
    except ValueError:
        return
    daysleft = days_until_next_birthday(month, day)
    if daysleft == 0:
        print("Happy birthday!")
    else:
        additionalmessage = "days left until your birthday!"
        if daysleft == 1:
            additionalmessage = "day left until your birthday!"
        print(daysleft, additionalmessage)
    

input_date()

