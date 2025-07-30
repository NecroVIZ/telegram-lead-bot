import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.state import State, StatesGroup
from bot.handlers.lead import start_lead
from bot.states.user_states import LeadForm

class TestLeadHandlers:
    @pytest.mark.asyncio
    async def test_start_lead_success(self, mock_message, mock_state):
        """Тест успешного начала заполнения заявки"""
        mock_state.get_state = AsyncMock(return_value=None)
        
        with patch('bot.handlers.lead.is_spam', return_value=False):
            await start_lead(mock_message, mock_state)
            
        mock_state.set_state.assert_called_once_with(LeadForm.name)
        mock_message.answer.assert_called_once_with("Введите ваше имя:", reply_markup=None)

    @pytest.mark.asyncio
    async def test_start_lead_already_in_progress(self, mock_message, mock_state):
        """Тест повторного начала заполнения заявки"""
        mock_state.get_state = AsyncMock(return_value=LeadForm.name)
        
        with patch('bot.handlers.lead.is_spam', return_value=False):
            await start_lead(mock_message, mock_state)
            
        mock_message.answer.assert_called_once_with(
            "⚠️ Вы уже оставляете заявку. Дождитесь завершения процесса или введите /cancel для отмены."
        )
        mock_state.set_state.assert_not_called()

    @pytest.mark.asyncio
    async def test_start_lead_spam_protection(self, mock_message, mock_state):
        """Тест защиты от спама"""
        mock_state.get_state = AsyncMock(return_value=None)
        
        with patch('bot.handlers.lead.is_spam', return_value=True):
            with patch('bot.handlers.lead.get_remaining_requests', return_value=2):
                await start_lead(mock_message, mock_state)
                
        mock_message.answer.assert_called_once()
        assert "слишком много заявок" in mock_message.answer.call_args[0][0]
        mock_state.set_state.assert_not_called()