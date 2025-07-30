import pytest
from unittest.mock import patch, MagicMock
from data.database import save_lead, get_stats

class TestDatabase:
    @patch('data.database.get_sheet')
    def test_save_lead_success(self, mock_get_sheet):
        """Тест успешного сохранения заявки"""
        # Мокаем sheet
        mock_sheet = MagicMock()
        mock_sheet.get_all_values.return_value = [["Имя", "Телефон", "Сообщение", "Дата"]]
        mock_get_sheet.return_value = mock_sheet
        
        result = save_lead("Иван", "+79991234567", "Тестовое сообщение")
        assert result == True
        mock_sheet.append_row.assert_called_once()

    @patch('data.database.get_sheet')
    def test_save_lead_failure(self, mock_get_sheet):
        """Тест неудачного сохранения заявки"""
        mock_get_sheet.return_value = None
        result = save_lead("Иван", "+79991234567", "Тестовое сообщение")
        assert result == False

    @patch('data.database.get_sheet')
    def test_get_stats_success(self, mock_get_sheet):
        """Тест успешного получения статистики"""
        # Мокаем sheet
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {"Имя": "Иван", "Телефон": "+79991234567", "Сообщение": "Тест", "Дата": "2025-07-30 12:00:00"},
            {"Имя": "Петр", "Телефон": "+79991234568", "Сообщение": "Тест2", "Дата": "2025-07-30 13:00:00"},
        ]
        mock_get_sheet.return_value = mock_sheet
        
        stats = get_stats()
        assert isinstance(stats, dict)
        assert "total_leads" in stats
        assert stats["total_leads"] >= 0

    @patch('data.database.get_sheet')
    def test_get_stats_failure(self, mock_get_sheet):
        """Тест неудачного получения статистики"""
        mock_get_sheet.return_value = None
        stats = get_stats()
        assert stats == {"total_leads": 0, "today_leads": 0, "week_leads": 0}