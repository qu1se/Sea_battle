from aiogram.dispatcher.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    ships_placing = State()
    ask_ready = State()
    battle = State()