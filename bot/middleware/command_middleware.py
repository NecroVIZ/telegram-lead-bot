from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

class CommandInStateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.text and event.text.startswith('/'):
            # Разрешаем только /cancel в состоянии
            if event.text == '/cancel':
                return await handler(event, data)
            else:
                # Игнорируем другие команды в состоянии
                state = data['state']
                current_state = await state.get_state()
                if current_state is not None:
                    await event.answer("⚠️ Пожалуйста, завершите текущую операцию или введите /cancel для отмены.")
                    return
        
        return await handler(event, data)