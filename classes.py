from collections import UserDict
from datetime import datetime

class AppException(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_number(value):
            raise AppException("Phone number must be 10 digits.")
        super().__init__(value)

    def is_valid_number(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except (ValueError, AttributeError):
            raise AppException("Invalid date format. Use DD.MM.YYYY")


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
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if not phone:
            raise AppException(f"Phone {old_phone} not found.")

        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)    
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    
    def add_birthday(self, name, birthday):
        record = self.find(name)
        if record is None:
            raise AppException(f"Contact {name} not found.")
        record.birthday = Birthday(birthday)

    def get_upcoming_birthdays(self, days=7):
        from datetime import datetime, timedelta

        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                bday_this_year = bday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                if today <= bday_this_year <= end_date:
                    congrats_date = bday_this_year
                    if congrats_date.weekday() == 5:
                        congrats_date += timedelta(days=2)
                    elif congrats_date.weekday() == 6:
                        congrats_date += timedelta(days=1)
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": congrats_date.strftime("%d.%m.%Y")
                    })
        return upcoming
