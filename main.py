import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from bot.bot import setup_handlers
from bot.middleware.command_middleware import CommandInStateMiddleware
from bot.config import BOT_TOKEN
from bot.utils.logger import get_logger

logger = get_logger(__name__)

async def shutdown(signal_name, bot, dp):
    """Корректное завершение работы"""
    logger.info(f"Получен сигнал {signal_name}, завершаем работу...")
    await dp.stop_polling()
    await bot.session.close()
    logger.info("Бот остановлен")

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Добавляем middleware
    dp.message.middleware(CommandInStateMiddleware())
    
    # Регистрируем хендлеры
    setup_handlers(dp)
    
    # Обработчики сигналов для graceful shutdown
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda s, f: asyncio.create_task(shutdown(s.name, bot, dp)))
    
    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())