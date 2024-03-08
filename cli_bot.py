from adress_book import AddressBook, Record
from exceptions import IncorectFormatError,ContactNotFoundError,NotFoundDataError

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact for entered name does not exist."
        except IndexError:
            return "Contact list is empty."
        except IncorectFormatError as e:
            return "Incorect format: " + str(e)
        except ContactNotFoundError:
            return "Contact for entered name does not exist." 
        except NotFoundDataError as e:
            return str(e)       

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    new_record = Record(name)
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    record.change_phone(phone)
    return 'Contact updated.'

@input_error
def display_phone(args, book: AddressBook):
    name = ''.join(args)
    record = book.find(name)
    return record.all_phones() 

@input_error
def display_all(book: AddressBook):
    if len(book) == 0:
        raise IndexError("")
    else:
        contacts = [str(record) for record in book.values()]
        return '\n'.join(contacts)

@input_error
def add_birthday(args, book: AddressBook):
    name, new_date = args
    record = book.find(name)
    record.add_birthday(new_date)
    return "Birthday has been added"

@input_error
def show_birthday(args, book: AddressBook):
    name = ''.join(args)
    record = book.find(name)
    return record.get_birthday() 

@input_error
def get_birthday_per_week(book: AddressBook):
    return book.get_birthdays_per_week   


def main():
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "all":
            print(display_all(book))
        elif command == "phone":
            print(display_phone(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))                   
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()