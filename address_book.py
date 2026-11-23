from collections import UserDict
from datetime import datetime, timedelta
import calendar

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __str__(self):
        return str(self.value)


# NEW
class Birthday(Field):
    def __init__(self, value):
        try:
            birth_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(birth_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("phone has to be 10 digit characters long")
        super().__init__(value)

    # redefining equals to be able to use ==
    def __eq__(self, another_phone):
        return isinstance(another_phone, Phone) and self.value == another_phone.value

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # adds a phone after checking if the phone already exists
    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        if new_phone in self.phones:
            raise ValueError(f"The phone is already associated with {self.name}")
        
        self.phones.append(new_phone)
          

    def remove_phone(self, phone: str):
        target_phone = Phone(phone)
        if target_phone not in self.phones:
            raise ValueError(f"{phone} isn't associated with {self.name}")
        self.phones.remove(target_phone)
        

    def edit_phone(self, old_phone: str, new_phone: str):
        # will fall if new phone doesn't meet the validation rules
        old = Phone(old_phone)
        new = Phone(new_phone)
        if old not in self.phones:
            raise ValueError(f"{old_phone} not found")
        if new in self.phones and new != old:
            raise ValueError(f"Phone {new_phone} already exists")
        self.phones[self.phones.index(old)] = new


    def find_phone(self, phone: str):
        return (
            self.phones[self.phones.index(Phone(phone))]
            if Phone(phone) in self.phones
            else None
        )

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    # NEW
    def add_birthday(self, birthday):
        birth_date = Birthday(birthday)
        if birth_date.value > datetime.today():
            raise ValueError("Birthday date cannot be in the future")
        self.birthday = birth_date


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if self.data.get(name) is not None:
            self.data.pop(name)
        else:
            raise ValueError(f"Contact {name} not found")

    def is_empty(self):
        return True if self.data == {} else False

    # NEW
    # returns list of dict of users that should be congratulated with bd within upcoming week
    def get_upcoming_birthdays(self):

        today = datetime.today()
        bd_date = None
        days = 7

        user_birth_date = None
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
            user_birth_date = record.birthday.value.date()

            if (
                user_birth_date.month == 2
                and user_birth_date.day == 29
                and not calendar.isleap(today.year)
            ):
                #  user_birth_date.day = 28
                user_birth_date = user_birth_date.replace(day=28)

            # get possible dates of birthdays for the week to then check if it matches the bd date of the user
            for i in range(days):
                bd_date = today + timedelta(days=i)
                if (
                    bd_date.month == user_birth_date.month
                    and bd_date.day == user_birth_date.day
                ):
                    congratulation_date = AddressBook.shift_from_weekend(bd_date)
                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": congratulation_date.strftime(
                                "%Y.%m.%d"
                            ),
                        }
                    )

        return upcoming_birthdays

    # shifts congratulation day to Monday if it is on Saturday or Sunday
    @staticmethod
    def shift_from_weekend(day):
        if day.weekday() == 5:
            return day + timedelta(days=2)
        if day.weekday() == 6:
            return day + timedelta(days=1)
        return day