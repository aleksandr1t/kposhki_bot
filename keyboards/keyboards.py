from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

pass_question_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пропустить вопрос")
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

