from aiogram.types import CallbackQuery
from model_db import *


async def select_verdict(call: CallbackQuery):
    from telegram_bot import inform_user_about_positive_verdict, inform_user_about_negative_verdict
    form_id = int(call.data.split(',')[0])
    verdict = int(call.data.split(',')[1])
    for note in FSMForm.select().where(FSMForm.id == form_id):
        form_user_id = note.telegram_id
        verdict_note = note.verdict

    if verdict_note is not None:
        if not verdict_note:
            info = 'вьебал ему отказ уже я'
        else:
            info = 'поздравил его уже блять я с зачислением на сервер'
        await call.message.answer(text=f'Хуль <a href="tg://user?id={call.from_user.id}">ты</a> '
                                       f'блять жмаешь на эту кнопку, все уже, поезд уехал, {info}')
        await call.answer()
        return

    if verdict:
        await inform_user_about_positive_verdict(form_user_id, form_id)
        answer = (f'{call.message.text[:-1]} ✅ Одобрено '
                  f'(решение принял <a href="tg://user?id={call.from_user.id}">этот админ</a>)')
        await call.message.edit_text(text=answer)
        # await call.message.answer(text=f'<a href="tg://user?id={call.from_user.id}">Вы</a> '
        #                                f'утвердили добавление игрока на сервер.\n'
        #                                f'Информация передана пользователю!')
    else:
        await inform_user_about_negative_verdict(form_user_id, form_id)
        answer = (f'{call.message.text[:-1]} ❌ Отказано '
                  f'(решение принял <a href="tg://user?id={call.from_user.id}">этот админ</a>)')
        await call.message.edit_text(text=answer)
        # await call.message.answer(text=f'<a href="tg://user?id={call.from_user.id}">Вы</a> '
        #                                f'отказали к допуску игроку по заявке.')
    await call.answer()


