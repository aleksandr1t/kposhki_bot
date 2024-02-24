from aiogram.filters.state import StatesGroup, State


class FormState(StatesGroup):
    about_player = State()
    what_to_do = State()
    game_experience = State()
    nick = State()
    garik_relationship = State()
    discord_id = State()

