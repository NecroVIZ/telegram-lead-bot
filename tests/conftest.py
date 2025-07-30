# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, Mock
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, Chat, CallbackQuery

@pytest.fixture
def mock_message():
    """Фикстура для мокированного сообщения"""
    message = Mock(spec=Message)
    message.from_user = Mock(spec=User)
    message.from_user.id = 123456789
    message.chat = Mock(spec=Chat)
    message.chat.id = 123456789
    message.text = ""
    message.answer = AsyncMock()
    return message

@pytest.fixture
def mock_callback():
    """Фикстура для мокированного callback'а"""
    callback = Mock(spec=CallbackQuery)
    callback.from_user = Mock(spec=User)
    callback.from_user.id = 123456789
    callback.message = Mock(spec=Message)
    callback.message.chat = Mock(spec=Chat)
    callback.message.chat.id = 123456789
    callback.data = ""
    callback.answer = AsyncMock()
    return callback

@pytest.fixture
def mock_state():
    """Фикстура для мокированного состояния FSM"""
    state = AsyncMock(spec=FSMContext)
    state.get_state = AsyncMock(return_value=None)
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    return state