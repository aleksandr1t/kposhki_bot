from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from utils.states import *
from keyboards.keyboards import *
from model_db import *
from telegram_bot import handle_file, send_to_channel, server_ip
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(FormState.about_player)
async def form_state_about_player(message: Message, state: FSMContext):
    data: str
    is_text: bool

    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        data = file_id
        await state.update_data(about_player=file_id)
        is_text = False
    elif not message.text:
        await message.answer(f"Нада отправить текст. Или голосовуху. Шаришь?\n"
                             f"Итак...")
        await message.answer(f"Расскажите о себе. Какие социальные навыки Вы в себе видите?\n"
                             f"\n"
                             f"<i>Вы можете отправить голосовое сообщение или текст</i>")
        return
    elif message.text.lower() in ['/new_form', '/start']:
        await message.answer(f"Для начала заполни оставшуюся форму")
        return
    elif len(message.text) < 10:
        await message.answer(f"Маловато как-то. Напиши побольше о себе ну пж🙏")
        return
    else:
        is_text = True
        data = message.text

    await message.answer(f"Интересно... Так и запишем...")
    await state.update_data(about_player=data)

    state_data = await state.get_data()
    FSMForm.update(
        about_player=data,
        is_about_player_text=is_text).where(FSMForm.id == state_data['id_form']).execute()
    await state.set_state(FormState.what_to_do)
    await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                         f"<i>Вам необходимо дать развернутый ответ. \n"
                         f"\n"
                         f"Вы можете отправить голосовое сообщение или текст</i>\n"
                         f"<b>Вопрос 2/4</b>")


@router.message(FormState.what_to_do)
async def form_state_what_to_do(message: Message, state: FSMContext):
    data: str
    is_text: bool

    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        data = file_id
        is_text = False
    elif not message.text and not message.voice:
        await message.answer(f"Текст. Голосовое сообщение. Ага?\n"
                             f"Пум-пум-пум...")
        await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>")
        return
    else:
        data = message.text
        is_text = True
    await message.answer(f"Угу. Идем дальше.")
    await state.update_data(what_to_do=data)
    state_data = await state.get_data()

    FSMForm.update(
        what_to_do=data,
        is_what_to_do_text=is_text).where(FSMForm.id == state_data['id_form']).execute()
    await state.set_state(FormState.game_experience)
    await message.answer(f"Какой Ваш опыт игры в Minecraft? На протяжении какого времени вы в него играете?\n"
                         f"<i>Вам необходимо дать развернутый ответ. \n"
                         f"\n"
                         f"Вы можете отправить голосовое сообщение или текст</i>\n"
                         f"<b>Вопрос 3/4</b>")


@router.message(FormState.game_experience)
async def form_state_game_experience(message: Message, state: FSMContext):
    data: str
    is_text: bool

    if message.voice:
        file_id = message.voice.file_id

        await handle_file(file_id=file_id, author_id=message.from_user.id)
        data = file_id
        is_text = False
    elif not message.text and not message.voice:
        await message.answer(f"Ты знаешь, как текст писать? А как голосовые сообщения записывать?\n"
                             f"Во дела. Понабирают всяких...")
        await message.answer(f"Какой Ваш опыт игры в Minecraft? На протяжении какого времени вы в него играете?\n"
                             f"<i>Вам необходимо дать развернутый ответ. \n"
                             f"\n"
                             f"Вы можете отправить голосовое сообщение или текст</i>")
        return

    else:
        data = message.text
        is_text = True
    await state.update_data(game_experience=data)
    state_data = await state.get_data()

    FSMForm.update(
        game_experience=data,
        is_game_experience_text=is_text).where(FSMForm.id == state_data['id_form']).execute()
    '''await state.set_state(FormState.nick)
    await message.answer(f"Введите Ваш ник в майнкрафте \n"
                         f"\n"
                         f"<i>Если Вы ещё не придумали ник, нажмите на кнопку</i> <b>Пропустить вопрос</b>\n"
                         f"<b>Вопрос 4/5</b>",
                         reply_markup=pass_question_keyboard)'''
    await state.set_state(FormState.garik_relationship)
    await message.answer(f"Окей, и пожалуй, самый главный вопрос.")
    await message.answer(f"Умеете ли вы играть на камнях?\n"
                         f"<b>Вопрос 4/4</b>",
                         reply_markup=garik_keyboard)


@router.message(NickConfirm.confirm)
async def form_state_nick_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Да':
        (FSMForm.update(
            nick=data['nick']).where(FSMForm.telegram_id == message.from_user.id)
         .where(FSMForm.verdict == True).execute())

        await message.answer(f"Отлично!\n\n"
                             f""
                             f"Присоединиться к серверу Вы сможете по IP {server_ip}\n"
                             f"Учтите, что добавление Вашего ника в вайтлист может занять до 3 часов.\n"
                             f"Спасибо, что Вы с нами!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif message.text == 'Нет, изменить ник':
        await message.answer(f"Введите Ваш ник в Minecraft \n"
                             f"\n"
                             f"<i>Позже изменить его Вы сможете только через админов, "
                             f"поэтому подумайте, прежде чем писать</i>", reply_markup=ReplyKeyboardRemove())
        await state.set_state(NickConfirm.nick)
    else:
        await message.answer(f"Выберите кнопку под поле ввода текста")


@router.message(NickConfirm.nick)
async def form_state_nick_nick(message: Message, state: FSMContext):
    data: str
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
        await message.answer(f"Введите Ваш ник в Minecraft \n"
                             f"\n"
                             f"<i>Позже изменить его Вы сможете только через админов, "
                             f"поэтому подумайте, прежде чем писать</i>")
        return

    if FSMForm.select().where(FSMForm.nick == msg).count():
        await message.answer(f"К сожалению, этот ник занят. \n"
                             f"Попробуйте другой((")
        return

    await state.update_data(nick=msg)

    await message.answer(f"Вы уверены?\n"
                         f"<i>Изменить ник возможно только через администрацию, поэтому подумайте, "
                         f"нужен ли Вам такой ник</i>", reply_markup=nick_keyboard)
    await state.set_state(NickConfirm.confirm)


@router.message(FormState.garik_relationship)
async def form_state_garik_relationship(message: Message, state: FSMContext):
    msg = message.text

    if msg in ['Меня зовут Гарик', 'Нет', 'Что?']:
        if msg == 'Что?':
            await message.answer(f"Ты еще про табуретки не слышал...")
        await state.update_data(garik_relationship=msg)
    else:
        await message.answer(f"На кнопку нажми уже любую")
        return

    data = await state.get_data()
    await state.clear()
    FSMForm.update(
        garik_relationship=msg,
        is_filled=True
    ).where(FSMForm.id == data['id_form']).execute()
    await message.answer(f"Спасибо! Мы рассмотрим заявку и ответим Вам здесь, в боте.",
                         reply_markup=ReplyKeyboardRemove()
                         )

    await send_to_channel(data=data, user_id=message.from_user.id)
