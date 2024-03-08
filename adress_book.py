from collections import UserDict
from datetime import datetime
from exceptions import ContactNotFoundError, IncorectFormatError, NotFoundDataError

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other    

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise IncorectFormatError("Phone number must be a 10-digit string.")

class Birthday(Field):
    def __init__(self, birthday):
        try:
            parsed_date = datetime.strptime(birthday, '%d.%m.%Y')
            super().__init__(parsed_date)
        except ValueError:
            raise IncorectFormatError('Birthday format must be in DD.MM.YYYY')

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")           

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None   

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"    

    def add_phone(self, phone): 
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def find_phone(self, phone):
        if phone in self.phones:
            return phone

    def all_phones(self):
        return ', '.join(str(phone) for phone in self.phones)      

    def edit_phone(self, existing_phone, new_phone):
        try:
            exist_index = self.phones.index(existing_phone)
            self.phones[exist_index] = Phone(new_phone)
        except ValueError:
            print("Unable to find existing phone: " + existing_phone)

    def change_phone(self, phone):
        self.phones = [Phone(phone)]        
    
    def add_birthday(self, input_date):
        self.birthday = Birthday(input_date)

    def get_birthday(self):
        if self.birthday is None:
            raise NotFoundDataError("Unable to find birthday date")
        else:
            return self.birthday

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
            raise ContactNotFoundError

    def delete(self, name):
        self.data.pop(name)

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        grouped_users = defaultdict(list)
    
        for user in self.data.values:
            name = user.name
            birthday = user.birthday.date()
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

        result = '\n'.join([f"{day}: {'\n'.join(names)}" for day, names in grouped_users.items()])
        return result   
