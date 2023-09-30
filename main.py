from collections import UserDict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate()

        self._value = new_value

    def validate(self):
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
    def __init__(self, value=None):
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
        phone = Phone(str(phone))
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
        if self.birthday:
            # birthday_str = str(self.birthday._value) if self.birthday else "N/A"
            return (f"Contact name: {self.name._value}, "
                    f"phones: {'; '.join(phone_number._value for phone_number in self.phones)}, "
                    f"birthday: {self.birthday._value}, "
                    f"birthday in {self.days_to_birthday()} days")
        else:
            return (f"Contact name: {self.name._value}, "
                    f"phones: {'; '.join(phone_number._value for phone_number in self.phones)}")

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

    def search(self, keyword):
        results = set()
        for record in self.data.values():
            if keyword.lower() in record.name.value.lower():
                results.add(record)
            for phone_number in record.phones:
                if keyword in phone_number.value:
                    results.add(record)
                    break
        return results


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


class FileManager:
    @staticmethod
    def save_to_json(address_book, filename):
        records = []
        for record in address_book.data.values():
            record_data = {
                "name": record.name._value,
                "birthday": record.birthday._value if record.birthday else None,
                "phones": [phone._value for phone in record.phones]
            }
            records.append(record_data)

        with open(filename, 'w') as file:
            json.dump(records, file)

    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            address_book = AddressBook()
            for record_data in data:
                record = Record(
                    record_data['name'],
                    record_data['birthday'])
                for phone in record_data['phones']:
                    record.add_phone(int(phone))
                address_book.add_record(record)
            return address_book
