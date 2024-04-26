import asyncio
import os
from dotenv import load_dotenv
import logging
import g4f

load_dotenv('.env')
from aiogram import Bot, Dispatcher
from handlers.user_handlers import register_user_handlers

from database.engine import create_db


# подключение всех хандлеров
def register_handlers(dp: Dispatcher):
    register_user_handlers(dp)


async def main():
    await create_db()
    logging.basicConfig(level=logging.INFO)
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)
    dp = Dispatcher(bot)

    register_handlers(dp)

    try:
        await dp.start_polling()
    except Exception as _ex:
        print(f"Error: {_ex}")


if __name__ == '__main__':
    asyncio.run(main())
