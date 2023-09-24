from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def get_value(self):
        return self._value

    @get_value.setter
    def set_value(self, new_value):
        self.validate(self)

        self._value = new_value

    def validate(self, new_value):
        pass


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self._value.isdigit() or len(self._value) != 10:
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if self._value:
            components = self._value.split('.')
            if len(components) != 3:
                raise ValueError("Invalid birthday format")
            day, month, year = map(int, components)
            try:
                datetime(year, month, day)
            except ValueError:
                raise ValueError("Invalid birthday date")

    def as_datetime(self):
        if not self._value:
            return None
        components = self._value.split('.')
        if len(components) != 3:
            raise ValueError("Invalid birthday format")
        day, month, year = map(int, components)
        try:
            return datetime(year, month, day)
        except ValueError:
            raise ValueError("Invalid birthday date")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone = Phone(phone)
        phone.validate()
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [phone_number for phone_number in self.phones if phone_number._value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone_number in self.phones:
            if phone_number._value == old_phone:
                phone_number._value = new_phone
                found = True
                break

        if not found:
            raise ValueError("Phone not found")

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number._value == phone:
                return phone_number

        return None

    def __str__(self):
        return f"Contact name: {self.name._value}, phones: {'; '.join(phone_number._value for phone_number in self.phones)}"

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.today()
        next_birthday = self.birthday.as_datetime().replace(year=today.year)

        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name._value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

class AddressBookPaginator:
    def __init__(self, address_book, page_size=10):
        self.address_book = address_book
        self.page_size = page_size
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        all_records = list(self.address_book.data.values())

        if start >= len(all_records):
            raise StopIteration

        page_content = all_records[start:end]

        self.current_page += 1
        return page_content

