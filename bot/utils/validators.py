import re

def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    if not phone:
        return False
    # Поддерживаем форматы: +7XXXXXXXXXX, 8XXXXXXXXXX, 7XXXXXXXXXX
    pattern = r'^(\+7|8|7)[0-9]{10}$'
    phone_clean = re.sub(r'[^0-9+]', '', phone)
    return bool(re.match(pattern, phone_clean))

def validate_name(name: str) -> bool:
    """Валидация имени"""
    if not name or len(name.strip()) < 2:
        return False
    # Считаем буквы
    letters = sum(1 for c in name if c.isalpha())
    # Проверяем, что не только цифры
    not_only_digits = not name.strip().isdigit()
    return letters >= 2 and not_only_digits