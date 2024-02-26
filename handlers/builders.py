from aiogram.utils.keyboard import InlineKeyboardBuilder


def form_rate_keyboard(form_id):
    builder_keyboard = InlineKeyboardBuilder()

    builder_keyboard.button(text='✅ Одобрено', callback_data=f'{form_id},1')
    builder_keyboard.button(text='❌ Отказано', callback_data=f'{form_id},0')

    builder_keyboard.adjust(2)
    return builder_keyboard.as_markup()
