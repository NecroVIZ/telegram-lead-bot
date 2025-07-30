from aiogram import Dispatcher
from bot.handlers import start, lead, admin

def setup_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(lead.router)
    dp.include_router(admin.router)