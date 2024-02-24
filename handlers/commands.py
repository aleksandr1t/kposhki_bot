from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from utils import states

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Здрасте, {message.from_user.first_name}!\n")
    await message.answer(f"Для доступа к серверу необходимо заполнить небольшую анкету.")

    await state.set_state(states.FormState.about_player)
    await message.answer(f"Расскажите о себе. Какие социальные навыки Вы в себе видите?\n"
                         f"\n"
                         f"<i>Вы можете отправить голосовое сообщение или текст</i>")