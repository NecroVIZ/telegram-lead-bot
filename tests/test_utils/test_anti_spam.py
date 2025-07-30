import pytest
from bot.utils.anti_spam import is_spam, get_remaining_requests

class TestAntiSpam:
    def test_first_request_not_spam(self):
        """Первый запрос не должен быть спамом"""
        user_id = 12345
        assert is_spam(user_id) == False

    def test_multiple_requests_within_limit(self):
        """Несколько запросов в пределах лимита"""
        user_id = 12346
        # 3 запроса в пределах лимита
        assert is_spam(user_id) == False
        assert is_spam(user_id) == False
        assert is_spam(user_id) == False
        # 4-й запрос должен быть спамом
        assert is_spam(user_id) == True

    def test_remaining_requests(self):
        """Проверка оставшихся запросов"""
        user_id = 12347
        # Используем 1 запрос
        is_spam(user_id)
        remaining = get_remaining_requests(user_id)
        assert remaining == 2  # Осталось 2 из 3