from aiogram.fsm.state import StatesGroup, State


class AddWordState(StatesGroup):
    english = State()
    translation = State()
    image = State()
