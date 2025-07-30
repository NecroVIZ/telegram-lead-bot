from aiogram import Router, F
from aiogram.types import Message
from bot.utils.logger import get_logger
from data.database import get_stats
from bot.config import ADMIN_IDS

router = Router()
logger = get_logger(__name__)

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(F.text == "/stats")
async def stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    try:
        stats_data = get_stats()
        response = f"📊 Статистика бота:\n\n"
        response += f"Всего заявок: {stats_data['total_leads']}\n"
        response += f"Сегодня: {stats_data['today_leads']}\n"
        response += f"За последние 7 дней: {stats_data['week_leads']}\n"
        await message.answer(response)
        logger.info(f"Админ {message.from_user.id} запросил статистику")
    except Exception as e:
        await message.answer("❌ Ошибка получения статистики")
        logger.error(f"Ошибка получения статистики: {e}")

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    
    response = "🔧 Панель администратора:\n\n"
    response += "/stats - статистика по заявкам\n"
    response += "/export - экспорт данных (в разработке)\n"
    response += "/help - помощь\n"
    await message.answer(response)