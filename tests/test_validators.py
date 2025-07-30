import pytest
from bot.utils.validators import validate_phone, validate_name

class TestPhoneValidation:
    def test_valid_phones(self):
        """Тестирование валидных номеров"""
        valid_phones = [
            "+79991234567",
            "89991234567",
            "79991234567",
        ]
        for phone in valid_phones:
            assert validate_phone(phone) == True, f"Телефон {phone} должен быть валидным"

    def test_invalid_phones(self):
        """Тестирование невалидных номеров"""
        invalid_phones = [
            "1234567890",  # Нет кода страны
            "+7999123456",  # Мало цифр
            "+799912345678",  # Много цифр
            "abc123",  # Буквы
            "",  # Пустая строка
            " ",  # Пробелы
            None,  # None
        ]
        for phone in invalid_phones:
            assert validate_phone(phone) == False, f"Телефон {phone} должен быть невалидным"

class TestNameValidation:
    def test_valid_names(self):
        """Тестирование валидных имён"""
        valid_names = [
            "Иван",
            "John",
            "Иван Петров",
            "Анна-Мария",
            "О'Коннор",
        ]
        for name in valid_names:
            assert validate_name(name) == True, f"Имя '{name}' должно быть валидным"

    def test_invalid_names(self):
        """Тестирование невалидных имён"""
        invalid_names = [
            "",  # Пустая строка
            " ",  # Пробелы
            "123",  # Только цифры
            "1",  # Одна буква
            "12",  # Две цифры
            None,  # None
        ]
        for name in invalid_names:
            assert validate_name(name) == False, f"Имя '{name}' должно быть невалидным"