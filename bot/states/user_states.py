from aiogram.fsm.state import State, StatesGroup

class LeadForm(StatesGroup):
    name = State()
    phone = State()
    message = State()
    confirm = State()