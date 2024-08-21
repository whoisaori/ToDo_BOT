import os
import sys
import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

from app.user import user
from app.admin import admin
from app.handlers import router
from app.database.models import async_main

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


async def main():
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(user, admin, router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


async def on_startup():
    await async_main()
    print('Бот запущен')


async def on_shutdown():
    print('Бот остановлен')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
