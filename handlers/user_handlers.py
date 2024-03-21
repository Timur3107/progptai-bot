from aiogram import Dispatcher, types
from handlers.start import cmd_start
from handlers.text import text_handler
# from handlers.delete_context import delete_context
from handlers.gpt3 import gpt3_handler
from handlers.gpt4 import gpt4_handler
from handlers.yandexgpt import yagpt_handler

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])

    dp.register_message_handler(gpt3_handler, commands=["gpt3"])
    dp.register_message_handler(gpt4_handler, commands=["gpt4"])
    dp.register_message_handler(yagpt_handler, commands=["yandexgpt"])

    # dp.register_message_handler(delete_context, commands=["deletecontext"])
    dp.register_message_handler(text_handler, content_types=types.ContentType.TEXT)
