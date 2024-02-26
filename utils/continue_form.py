from model_db import *
from utils import states
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def continue_form(message: Message, state: FSMContext):
    request = FSMForm.select().where(FSMForm.telegram_id == message.from_user.id).where(FSMForm.is_filled == False)
    if len(request) == 0:
        return False

    await message.answer(f"Мы нашли недозаполненную анкету!")

    for note in request:
        note_id = note.id
        about_player = note.about_player
        what_to_do = note.what_to_do
        game_experience = note.game_experience
        nick = note.nick
        garik_relationship = note.garik_relationship

    if about_player is None:
        await state.update_data(id_form=note_id)
        await state.set_state(states.FormState.about_player)
        await message.answer(f"Расскажите о себе. Какие социальные навыки Вы в себе видите?\n"
                             f"\n"
                             f"<i>Вы можете отправить голосовое сообщение или текст</i>\n"
                             f"<b>Вопрос 1/5</b>")
    elif what_to_do is None:
        await state.update_data(id_form=note_id)
        await state.set_state(states.FormState.what_to_do)
        await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>\n"
                             f"<b>Вопрос 2/5</b>")
    elif game_experience is None:
        await state.update_data(id_form=note_id)
        await state.set_state(states.FormState.game_experience)
        await message.answer(f"Какой Ваш опыт игры в Minecraft? На протяжении какого времени вы в него играете?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>\n"
                             f"<b>Вопрос 3/5</b>")
    elif nick is None:
        await state.update_data(id_form=note_id)
        await state.set_state(states.FormState.nick)
        await message.answer(f"Введите Ваш ник в майнкрафте \n"
                             f"\n"
                             f"<i>Если Вы ещё не придумали ник, нажмите на кнопку</i> <b>Пропустить вопрос</b>\n"
                             f"<b>Вопрос 4/5</b>")
    elif garik_relationship is None:
        await state.update_data(id_form=note_id)
        await state.set_state(states.FormState.garik_relationship)
        await message.answer(f"Умеете ли вы играть на камнях?\n"
                             f"<b>Вопрос 5/5</b>",)
    else:
        await message.answer('Невозможно найти сохраненку!')
    return True
