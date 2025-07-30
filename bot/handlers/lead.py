from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.user_states import LeadForm
from bot.keyboards.reply import get_confirm_keyboard, get_main_keyboard
from bot.utils.validators import validate_phone, validate_name
from bot.utils.anti_spam import is_spam, get_remaining_requests
from bot.utils.logger import get_logger
from data.database import save_lead
from bot.config import ADMIN_IDS

router = Router()
logger = get_logger(__name__)

# Константы
MAX_NAME_LENGTH = 50
MAX_PHONE_LENGTH = 20
MAX_MESSAGE_LENGTH = 500

def clean_text(text: str) -> str:
    """Очистка текста от непечатаемых символов"""
    if not text:
        return ""
    return ''.join(char for char in text if char.isprintable()).strip()

@router.message(F.text == "Оставить заявку")
async def start_lead(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Проверка на спам
    if is_spam(user_id):
        remaining = get_remaining_requests(user_id)
        await message.answer(
            f"⚠️ Вы отправили слишком много заявок. Попробуйте через час.\n"
            f"Осталось запросов: {remaining}"
        )
        logger.warning(f"Спам-запрос от пользователя {user_id}")
        return

    # Проверка, не находится ли пользователь уже в процессе
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("⚠️ Вы уже оставляете заявку. Дождитесь завершения процесса или введите /cancel для отмены.")
        return
    
    await state.set_state(LeadForm.name)
    await message.answer("Введите ваше имя:", reply_markup=None)
    logger.info(f"Пользователь {user_id} начал заполнение заявки")

@router.message(F.text == "/cancel")
async def cancel_form(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Нет активной формы для отмены.")
        return
    await state.clear()
    await message.answer("❌ Форма отменена.", reply_markup=get_main_keyboard())
    logger.info(f"Пользователь {message.from_user.id} отменил форму")

@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext):
    # Защита от медиа
    if not message.text:
        await message.answer("⚠️ Пожалуйста, введите текстовое имя.")
        return
    
    # Очистка текста
    cleaned_text = clean_text(message.text)
    if not cleaned_text:
        await message.answer("⚠️ Введённый текст содержит только специальные символы.")
        return
    
    # Проверка длины
    if len(cleaned_text) > MAX_NAME_LENGTH:
        await message.answer(f"⚠️ Имя слишком длинное. Максимум {MAX_NAME_LENGTH} символов.")
        return
    
    if not validate_name(cleaned_text):
        await message.answer("⚠️ Имя должно содержать хотя бы 2 буквы и не состоять только из цифр.")
        return
    
    await state.update_data(name=cleaned_text)
    await state.set_state(LeadForm.phone)
    await message.answer("Введите ваш номер телефона:")

@router.message(LeadForm.phone)
async def process_phone(message: Message, state: FSMContext):
    # Защита от медиа
    if not message.text:
        await message.answer("⚠️ Пожалуйста, введите текстовый номер телефона.")
        return
        
    # Очистка текста
    cleaned_text = clean_text(message.text)
    if not cleaned_text:
        await message.answer("⚠️ Введённый текст содержит только специальные символы.")
        return
    
    # Проверка длины
    if len(cleaned_text) > MAX_PHONE_LENGTH:
        await message.answer(f"⚠️ Номер телефона слишком длинный. Максимум {MAX_PHONE_LENGTH} символов.")
        return
        
    if not validate_phone(cleaned_text):
        await message.answer("⚠️ Неверный формат телефона. Введите в формате: +7XXXXXXXXXX или 8XXXXXXXXXX")
        return
    await state.update_data(phone=cleaned_text)
    await state.set_state(LeadForm.message)
    await message.answer("Введите ваш вопрос или сообщение:")

@router.message(LeadForm.message)
async def process_message(message: Message, state: FSMContext):
    # Защита от медиа
    if not message.text:
        await message.answer("⚠️ Пожалуйста, введите текстовое сообщение.")
        return
        
    # Очистка текста
    cleaned_text = clean_text(message.text)
    if not cleaned_text:
        await message.answer("⚠️ Введённый текст содержит только специальные символы.")
        return
    
    # Проверка длины
    if len(cleaned_text) > MAX_MESSAGE_LENGTH:
        await message.answer(f"⚠️ Сообщение слишком длинное. Максимум {MAX_MESSAGE_LENGTH} символов.")
        return
        
    if len(cleaned_text) < 5:
        await message.answer("⚠️ Сообщение должно содержать хотя бы 5 символов.")
        return
    await state.update_data(message=cleaned_text)
    data = await state.get_data()
    summary = f"Проверьте данные заявки:\n\nИмя: {data['name']}\nТелефон: {data['phone']}\nСообщение: {data['message']}"
    await message.answer(summary, reply_markup=get_confirm_keyboard())
    await state.set_state(LeadForm.confirm)
    # Добавляем флаг, что заявка ещё не отправлена
    await state.update_data(submitted=False)

@router.callback_query(LeadForm.confirm)
async def handle_confirmation(callback: CallbackQuery, state: FSMContext):
    # Проверка, что callback.data существует
    if not callback.data:
        await callback.answer("⚠️ Ошибка обработки кнопки.")
        return
        
    # Проверка актуальности callback'а
    if callback.message is None:
        await callback.answer("⚠️ Сообщение устарело.")
        return

    # Проверка безопасности - только тот же пользователь
    if callback.from_user.id != callback.message.chat.id:
        await callback.answer("⚠️ Это не ваша форма.")
        return

    # Получаем данные состояния
    data = await state.get_data()
    user_id = callback.from_user.id
    
    if callback.data == "confirm":
        # Проверка, не была ли уже отправлена
        if data.get('submitted', False):
            await callback.answer("⚠️ Заявка уже отправлена.")
            return
            
        # Устанавливаем флаг отправки
        await state.update_data(submitted=True)
            
        success = save_lead(data['name'], data['phone'], data['message'])
        if success:
            try:
                await callback.message.edit_text("✅ Заявка успешно отправлена! Спасибо за обращение.")
                # Уведомление админам с обработкой ошибок
                notification = f"📬 Новая заявка!\n\nИмя: {data['name']}\nТелефон: {data['phone']}\nСообщение: {data['message']}"
                for admin_id in ADMIN_IDS:
                    try:
                        await callback.bot.send_message(admin_id, notification)
                    except Exception as e:
                        logger.error(f"Ошибка отправки уведомления админу {admin_id}: {e}")
                logger.info(f"Заявка от пользователя {user_id} успешно сохранена")
            except Exception as e:
                logger.error(f"Ошибка редактирования сообщения: {e}")
                try:
                    await callback.message.answer("✅ Заявка отправлена, но возникли проблемы с интерфейсом.")
                except:
                    pass
        else:
            try:
                await callback.message.edit_text("❌ Произошла ошибка при сохранении заявки. Попробуйте позже.")
            except:
                await callback.message.answer("❌ Произошла ошибка при сохранении заявки. Попробуйте позже.")
            logger.error(f"Ошибка сохранения заявки от пользователя {user_id}")
        await state.clear()
        
    elif callback.data == "cancel":
        await state.clear()
        try:
            await callback.message.edit_text("❌ Отправка отменена.", reply_markup=get_main_keyboard())
        except:
            await callback.message.answer("❌ Отправка отменена.", reply_markup=get_main_keyboard())
        logger.info(f"Пользователь {user_id} отменил заявку")
    
    # Отвечаем на callback, чтобы убрать "крутящийся" индикатор
    try:
        await callback.answer()
    except:
        pass