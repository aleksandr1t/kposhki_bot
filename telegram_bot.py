import os
import redis.asyncio as redis
from model_db import *
from utils import states
from config import TOKEN_epta, rediska
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from handlers import quetionaire, builders
from aiogram.fsm.storage.base import StorageKey, BaseStorage
from handlers import commands
from handlers import callback
import asyncio
import logging
import sys
from aiogram.types import FSInputFile
from aiogram.fsm.storage.redis import RedisStorage


server_ip = '147.185.221.18:35666'

TOKEN = TOKEN_epta
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

storage = RedisStorage(redis.Redis(host="172.31.99.45", port=6379, username="kposhnik", password=f'{rediska}'))

dp = Dispatcher(storage=storage)
dp.callback_query.register(callback.select_verdict)


async def inform_user_about_positive_verdict(form_user_id: int, form_id: int):
    FSMForm.update(verdict=True).where(FSMForm.id == form_id).execute()

    await bot.send_message(form_user_id, f'Поздравляем!\n'
                                         f'Наши администраторы проверили заявку и допустили Вас на сервер!\n\n'
                                         f''
                                         f'Осталось только написать ник, чтобы добавить Вас в вайтлист')

    state_with: FSMContext = FSMContext(storage=dp.storage, key=StorageKey(
        chat_id=form_user_id, user_id=form_user_id, bot_id=bot.id))

    await state_with.set_state(states.NickConfirm.nick)
    await bot.send_message(form_user_id, f"Введите Ваш ник в Minecraft \n"
                                         f"\n"
                                         f"<i>Позже изменить его Вы сможете только через админов, "
                                         f"поэтому подумайте, прежде чем писать</i>")


async def inform_user_about_negative_verdict(form_user_id: int, form_id: int):
    FSMForm.update(verdict=False).where(FSMForm.id == form_id).execute()

    await bot.send_message(form_user_id,
                           f'Возможно, Вы заполнили что-то не так, но Ваша анкета сочлась неубедительной.\n'
                           f'В следующий раз Вы можете попытать удачу и заполнить анкету ещё раз, '
                           f'написав команду /new_form\n\n'
                           f'Спасибо за обращение!')


async def announce_nick_admin(nick: str, nick_telegram_id: int):
    await bot.send_message(1027005788,
                           f'Приветики...\n'
                           f'нужно добавить в вайтлист <a href>челика под ником <code>{nick}</code>.\n\n'
                           f''
                           f'Надеюсь, ты сделаешь это как можно скорее!')


async def main():
    dp.include_routers(quetionaire.router, commands.router)
    await dp.start_polling(bot)


async def handle_file(file_id: str, author_id: int):
    path = 'voices'
    author_id = str(author_id)
    if not os.path.exists(f'{path}/{author_id}'):
        os.mkdir(f'{path}/{author_id}')

    file = await bot.get_file(file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{author_id}/{file_id}.ogg")


async def send_to_channel(data: dict, user_id: int):
    form_id = data['id_form']
    channel_id = -4165034341
    buffer = ''
    for note in FSMForm.select().where(FSMForm.id == form_id):
        is_about_player_text = note.is_about_player_text
        is_what_to_do_text = note.is_what_to_do_text
        is_game_experience_text = note.is_game_experience_text

    if is_about_player_text:
        buffer += (f'Заявка <b>№{form_id}</b> от <a href="tg://user?id={user_id}">этого пользователя</a>\n\n'
                   f''
                   f'<i>Рассмотрите её как можно скорее, но объективно.\n'
                   f'Если Вы столкнулись с трудностями, '
                   f'не забудьте проконсультироваться с другими администраторами.</i>\n\n\n'
                   f''
                   f''
                   f'<b>Вопрос №1</b> Расскажите о себе\n\n'
                   f'{data['about_player']}\n\n')
    else:
        await bot.send_message(channel_id, f'Заявка <b>№{form_id}</b> от '
                                           f'<a href="tg://user?id={user_id}">этого пользователя</a>\n\n'
                                           f'<i>Рассмотрите её как можно скорее, но объективно.\n'
                                           f'Если Вы столкнулись с трудностями, '
                                           f'не забудьте проконсультироваться с другими администраторами.</i>\n\n\n'
                                           f''
                                           f''
                                           f'<b>Вопрос №1</b> Расскажите о себе')
        await bot.send_voice(channel_id, FSInputFile(f"voices/{user_id}/{data['about_player']}.ogg"))

    if is_what_to_do_text:
        buffer += (f'<b>Вопрос №2</b> Цель, чем заниматься\n\n'
                   f'{data['what_to_do']}\n\n')
    else:
        if is_about_player_text:
            await bot.send_message(channel_id, f'{buffer}\n'
                                               f'<b>Вопрос №2</b> Цель, чем заниматься')
        else:
            await bot.send_message(channel_id, f'<b>Вопрос №2</b> Цель, чем заниматься')
        await bot.send_voice(channel_id, FSInputFile(f"voices/{user_id}/{data['what_to_do']}.ogg"))

    if is_game_experience_text:
        if is_what_to_do_text:
            buffer += (f'<b>Вопрос №3</b> Опыт игры\n\n'
                       f'{data['game_experience']}\n\n')
        else:
            buffer = (f'<b>Вопрос №3</b> Опыт игры\n\n'
                      f'{data['game_experience']}\n\n')
        await bot.send_message(channel_id, buffer)
    else:
        if is_what_to_do_text:
            await bot.send_message(channel_id, f'{buffer}\n\n'
                                               f'<b>Вопрос №3</b> Опыт игры')
        else:
            await bot.send_message(channel_id, f'<b>Вопрос №3</b> Опыт игры')
        await bot.send_voice(channel_id, FSInputFile(f"voices/{user_id}/{data['game_experience']}.ogg"))

    await bot.send_message(channel_id, f'<b>Вопрос №4</b> Умеет ли человек играть на камнях\n\n'
                                       f''
                                       f'{data['garik_relationship']}\n\n\n'
                                       f''
                                       f'Руководствуясь общими правилами рассмотрения заявок, '
                                       f'Вы, как уполномоченное лицо по рассмотрению заявок, '
                                       f'утверждаете, что в рассмотрении завяки вы выносите вердикт:\n\n'
                                       f''
                                       f'В заявке <b>№{form_id}</b>:',
                           reply_markup=builders.form_rate_keyboard(form_id))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
