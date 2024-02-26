from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from utils import states
from datetime import datetime
from model_db import *

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if FSMForm.select().where(FSMForm.telegram_id == message.from_user.id).count() == 0:
        await message.answer(f"Здрасте, {message.from_user.first_name}!\n")
        await message.answer(f"Для доступа к серверу необходимо заполнить небольшую анкету из 4 вопросов, "
                             f"3 вопроса из них требуют развернутого ответа.\n"
                             f"\n"
                             f"Поехали!")

        await command_new_form(message, state)
    else:
        await message.answer(f"Если Вы допустили ошибку и хотите заполнить анкету ещё раз, введите команду /new_form")


@router.message(Command('new_form'))
async def command_new_form(message: Message, state: FSMContext) -> None:
    # if await continue_form.continue_form(message, state): return
    if message.chat.id < 0:
        await message.answer(f"Нахуй иди")
        return
    for note in FSMForm.select().where(FSMForm.telegram_id == message.from_user.id):
        if note.verdict:
            await message.answer(f"Вам уже пришёл положительный ответ по заявке! Подавать её ещё раз нет смысла!")
            return

    await state.set_state(states.FormState.about_player)
    fsm_form = FSMForm.create(
        time_of_creation=datetime.now(),
        telegram_id=message.from_user.id,
        is_filled=False)

    await state.update_data(id_form=fsm_form.id)
    await message.answer(f"Расскажите о себе. Какие социальные навыки Вы в себе видите?\n"
                         f"\n"
                         f"<i>Вы можете отправить голосовое сообщение или текст</i>\n"
                         f"<b>Вопрос 1/4</b>")
