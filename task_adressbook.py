from collections import UserDict
import re

# Базові класи 

class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class Name(Field):
    """Поле для імені контакту."""
    pass


class Phone(Field):
    """Поле для номера телефону з валідацією формату (10 цифр)."""

    def __init__(self, value):
        validated = self._validate(value)
        super().__init__(validated)

    @staticmethod
    def _validate(phone_number: str):
        if not re.fullmatch(r"^\d{10}$", phone_number):
            raise ValueError("Номер телефону повинен містити рівно 10 цифр.")
        return phone_number

    def set_phone(self, new_value):
        self._value = self._validate(new_value)


# Клас Record 

class Record:
    """Запис контакту: імʼя та список телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        """Додає телефон з валідацією."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def find_phone(self, phone_number: str):
        """Пошук телефону за значенням."""
        return next((p for p in self.phones if p.value == phone_number), None)

    def edit_phone(self, old_phone: str, new_phone: str):
        """Редагування існуючого номера."""
        phone = self.find_phone(old_phone)
        if phone is None:
            raise ValueError(f"Телефон '{old_phone}' не знайдено.")
        phone.set_phone(new_phone)

    def remove_phone(self, phone_number: str):
        """Видалення телефону."""
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError(f"Телефон '{phone_number}' не знайдено.")
        self.phones.remove(phone)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        return f"Contact name: {self.name.value}, phones: {phones}"


# Клас AddressBook 

class AddressBook(UserDict):
    """Колекція записів, що працює як словник."""

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name not in self.data:
            raise KeyError(f"Запис для '{name}' не знайдено.")
        del self.data[name]


# Реалізація 

if __name__ == '__main__':
    # Створення книги
    book = AddressBook()

    # Запис John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Демонстрація помилки
    try:
        john_record.add_phone("123")  # Невалідний номер
    except ValueError as e:
        print(f"Помилка додавання: {e}")

    book.add_record(john_record)

    # Запис Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Вивід усіх записів
    for record in book.data.values():
        print(record)

    # Редагування номера John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    # Пошук телефону
    found = john.find_phone("5555555555")
    print(f"{john.name.value}: {found.value}")

    # Видалення запису
    book.delete("Jane")