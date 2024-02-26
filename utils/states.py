from aiogram.filters.state import StatesGroup, State


class FormState(StatesGroup):
    id_form = State()
    about_player = State()
    what_to_do = State()
    game_experience = State()
    garik_relationship = State()


class NickConfirm(StatesGroup):
    id_form = State()
    nick = State()
    confirm = State()
