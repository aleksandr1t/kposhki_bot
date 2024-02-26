from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

nick_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет, изменить ник")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Не придумал Вы можете'
)

garik_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меня зовут Гарик"),
        ],
        [
            KeyboardButton(text="Нет")
        ],
        [
            KeyboardButton(text="Что?")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Играете на камнях?'
)

