from aiogram import Router, F
from utils.states import *
from keyboards.keyboards import *
from telegram_bot import handle_file
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

router = Router()


@router.message(FormState.about_player)
async def form_state_about_player(message: Message, state: FSMContext):
    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        await state.update_data(about_player=file_id)
    elif not message.text:
        await message.answer(f"Нада отправить текст. Или голосовуху. Шаришь?\n"
                             f"Итак...")
        await message.answer(f"Расскажите о себе. Какие социальные навыки Вы в себе видите?\n"
                             f"\n"
                             f"<i>Вы можете отправить голосовое сообщение или текст</i>")
        return
    elif len(message.text) < 10:
        await message.answer(f"Маловато как-то. Напиши побольше о себе ну пж🙏")
        return
    else:
        await state.update_data(about_player=message.text)
    await state.set_state(FormState.what_to_do)
    await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                         f"<i>Вам необходимо дать развернутый ответ. \n"
                         f"\n"
                         f"Вы можете отправить голосовое сообщение или текст</i>")


@router.message(FormState.what_to_do)
async def form_state_what_to_do(message: Message, state: FSMContext):
    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        await state.update_data(what_to_do=file_id)
    elif not message.text and not message.voice:
        await message.answer(f"Текст. Голосовое сообщение. Ага?\n"
                             f"Пум-пум-пум...")
        await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>")
        return
    else:
        await state.update_data(what_to_do=message.text)
    await state.set_state(FormState.game_experience)
    await message.answer(f"Какой Ваш опыт игры в Minecraft? На протяжении какого времени вы в него играете?\n"
                         f"<i>Вам необходимо дать развернутый ответ. \n"
                         f"\n"
                         f"Вы можете отправить голосовое сообщение или текст</i>")


@router.message(FormState.game_experience)
async def form_state_game_experience(message: Message, state: FSMContext):
    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        await state.update_data(game_experience=file_id)
    elif not message.text and not message.voice:
        await message.answer(f"Ты знаешь, как текст писать? А как голосовые сообщения записывать?\n"
                             f"Во дела. Понабирают всяких...")
        await message.answer(f"Какой Ваш опыт игры в Minecraft? На протяжении какого времени вы в него играете?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>")
        return

    else:
        await state.update_data(game_experience=message.text)
    await state.set_state(FormState.nick)
    await message.answer(f"Введите Ваш ник в майнкрафте \n"
                         f"\n"
                         f"<i>Если Вы ещё не придумали ник, нажмите на кнопку</i> <b>Пропустить вопрос</b>",
                         reply_markup=pass_question_keyboard)


@router.message(FormState.nick)
async def form_state_game_experience(message: Message, state: FSMContext):
    msg = message.text
    if not message.text:
        if message.voice:
            await message.answer(f"МНЕ ЗАЧЕМ ТВОЁ ГС? СМЕШНО ТИПА?")
        if message.photo:
            await message.answer(f"По фотке что-ли я должен ник прочитать? Не умею, простите(")
        if message.video:
            await message.answer(f"В видео я как ник увижу? Просто напиши ник, не знаешь, пропускай вопрос")
        else:
            await message.answer(f"Просто ник текстом скинь пожалуйст прошу тебя")
        await message.answer(f"Введите Ваш ник в майнкрафте \n"
                             f"\n"
                             f"<i>Если Вы ещё не придумали ник, нажмите на кнопку</i> <b>Пропустить вопрос</b>")
        return

    if msg == 'Пропустить вопрос':
        await state.update_data(nick='Вопрос пропущен')
    else:
        await state.update_data(nick=msg)
    await state.set_state(FormState.garik_relationship)
    await message.answer(f"И, пожалуй, самый главный вопрос.")
    await message.answer(f"Умеете ли вы играть на камнях?", reply_markup=garik_keyboard)


@router.message(FormState.garik_relationship)
async def form_state_game_experience(message: Message, state: FSMContext):
    msg = message.text

    if msg in ['Меня зовут Гарик', 'Нет', 'Что?']:
        if msg == 'Что?':
            await message.answer(f"Ты еще про табуретки не слышал...")
        await state.update_data(garik_relationship=msg)
    else:
        await message.answer(f"На кнопку нажми уже любую")
        return

    await message.answer(f"Ваша заявка <b>не</b> зарегистрирована, потому что я еще даже для этих заявок БД не настроил.\n"
                         f"Зато можете полюбоваться записью в FSM, которая уже стёрта:")
    data = await state.get_data()
    await state.clear()

    formatted_text = []
    [
        formatted_text.append(f"{key}: {value}")
        for key, value in data.items()
    ]
    await message.answer("\n".join(formatted_text), reply_markup=ReplyKeyboardRemove())

