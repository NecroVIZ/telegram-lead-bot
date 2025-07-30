from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.reply import get_main_keyboard

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    # Поддержка deep linking
    args = message.text[6:] if len(message.text) > 6 else ""
    welcome_text = "Привет! Я бот для сбора заявок 👋"
    if args:
        welcome_text += f"\n\nВы перешли по ссылке с параметром: {args}"
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@router.message(F.text == "О нас")
async def about(message: Message):
    await message.answer("Я помогаю собирать заявки от клиентов и отправляю их вам в таблицу Google Sheets.")

# Обработка команды /help
@router.message(F.text == "/help")
async def help_command(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/cancel - отменить текущую форму\n"
        "/help - показать помощь\n"
    )
    # Только для админов
    from bot.config import ADMIN_IDS
    if message.from_user.id in ADMIN_IDS:
        help_text += "/admin - панель администратора\n"
        help_text += "/stats - статистика по заявкам\n"
    
    await message.answer(help_text)