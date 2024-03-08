from datetime import datetime
from collections import defaultdict

users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Elon Musk", "birthday": datetime(1971, 6, 28)},
    {"name": "Angela Merkel", "birthday": datetime(1954, 7, 17)},
    {"name": "Oprah Winfrey", "birthday": datetime(1954, 1, 29)},
    {"name": "Volodymyr Zelenskiy", "birthday": datetime(1980, 7, 12)},
    {"name": "Mia Skorokhod", "birthday": datetime(2020, 2, 24)},
    {"name": "Test User", "birthday": datetime(1992, 2, 29)}
]

def get_birthdays_per_week(users):
    today = datetime.today().date()
    grouped_users = defaultdict(list)
    
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days
        if delta_days < 7:
            weekday = birthday_this_year.weekday()
            if weekday == 5 or weekday == 6:
                day_name = 'Monday'
            else:
                day_name = birthday_this_year.strftime("%A")
            grouped_users[day_name].append(name)

    for day, names in grouped_users.items():
        print(day + ': ' + ', '.join(names))

get_birthdays_per_week(users)