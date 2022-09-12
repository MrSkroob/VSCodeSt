import datetime


def is_leap_year(year: int):
    if year % 400 == 0: # basically checks if both statements below are true
        return True
    if year % 100 == 0: # prevents 2100 from being considered a leap year
        return False
    if year % 4 == 0: # divisible by 4 rule
        return True
    return False


def days_in_months(month: int, year: int):
    if month in (1, 3, 5, 7, 8, 10, 12): # checks if month is a 31 month
        return 31
    if month == 2: # if February...
        if is_leap_year(year):
            return 29
        return 28
    return 30 # returns 30 if not February


def days_until_next_birthday(birthdaymonth: int, birthdayday: int):
    todaydatetime = datetime.datetime.today() # get the datetime object for today
    todaydate = datetime.datetime.date(todaydatetime) # convert it to date format
    year = todaydate.year
    birthdaytotal = days_in_months(birthdaymonth, year) + birthdayday # get days value of birthday since start of year

    month = todaydate.month
    day = todaydate.day
    datetotal = days_in_months(month, year) + day # get number of days today since start of year

    nextbirthday = None
    if birthdaytotal - datetotal < 0: # checks if birthday has already passed
        nextbirthday = datetime.date(todaydate.year + 1, birthdaymonth, birthdayday)
    else:
        nextbirthday = datetime.date(todaydate.year, birthdaymonth, birthdayday)
    difference = nextbirthday - todaydate # difference between the next birthday and today
    return difference.days


def input_date():
    try:
        day = int(input("Day of your birthday"))
        month = int(input("Month of your birthday"))
        year = int(input("Year of your birthday"))
    except ValueError:
        return
    if not (0 < month < 13 and 0 < day < days_in_months(month, year) + 1): # invalid date
        print("Invalid date")
        return
    print(days_until_next_birthday(month, day), "days until your birthday!")
    

input_date()

