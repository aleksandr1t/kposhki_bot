import os
from model_db import *
from config import TOKEN_epta
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from handlers import quetionaire
from handlers import commands
import asyncio
import logging
import sys
from pathlib import Path
from aiogram.types import File

TOKEN = TOKEN_epta
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main():
    dp = Dispatcher()
    dp.include_routers(quetionaire.router,
                       commands.router)
    await dp.start_polling(bot)


async def handle_file(file_id: str, author_id: int):
    path = 'voices'
    author_id = str(author_id)
    if not os.path.exists(f'{path}/{author_id}'):
        os.mkdir(f'{path}/{author_id}')

    file = await bot.get_file(file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{author_id}/{file_id}.ogg")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
