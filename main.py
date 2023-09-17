from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Invalid phone number format")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone = Phone(phone)
        phone.validate_phone()
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [phone_number for phone_number in self.phones if phone_number.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone_number in self.phones:
            if phone_number.value == old_phone:
                phone_number.value = new_phone
                found = True
                break

        if not found:
            raise ValueError("Phone not found")

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                return phone_number

        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone_number.value for phone_number in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

