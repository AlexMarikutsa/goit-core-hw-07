from classes import AddressBook, AppException, Phone, Record

# constants
EXIT = "exit"
CLOSE = "close"
ERROR_MESSAGE = "Invalid command."

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppException as e:
            return str(e)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Incomplete input. Please provide all required arguments."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, book: AddressBook):
    try:
        name, birthday = args
    except ValueError:
        raise AppException(f"Give me name and birthday in format DD.MM.YYYY.")

    book.add_birthday(name, birthday)
    return f"Birthday for {name} added: {birthday}"


@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        return "Give me name"
    contact = book.find(args[0])
    if contact is None:
        return "Contact not found."
    if contact.birthday is None:
        return f"{contact.name.value} has no birthday set."
    return f"{contact.name.value}'s birthday: {contact.birthday.value}"


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record is None:
        return "Contact not found."

    phone_new = Phone(phone)
    record.phone = [phone_new]

    return "Contact updated"


@input_error
def show_phone(args, book: AddressBook):
    if not args:
        return "Invalid input data"
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return f"{record.name.value}'s phone: {', '.join(phone.value for phone in record.phones)}"


def show_all(book: AddressBook):
    if not book.data:
        return "Contacts are empty."
    contactsList = ""

    for key, value in book.items():
        contactsList += f"{key} => {value}\n"

    return contactsList


def show_upcoming_birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays(days=7)
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next 7 days."

    return "\n".join(
        f"{item['name']}: {item['birthday']}" for item in upcoming_birthdays
    )


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(show_upcoming_birthdays(book))
            case _:
                print(ERROR_MESSAGE)

if __name__ == "__main__":
    main()
