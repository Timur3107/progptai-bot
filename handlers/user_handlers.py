from aiogram import Dispatcher, types
from handlers.start import cmd_start
from handlers.text import text_handler
from handlers.delete_dialog import cmd_delete_dialog
from handlers.models_gpt import change_models


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(lambda msg: change_models(msg, "gpt3"), commands=["gpt3"])
    dp.register_message_handler(lambda msg: change_models(msg, "gpt4"), commands=["gpt4"])
    dp.register_message_handler(lambda msg: change_models(msg, "yandexgpt"), commands=["yandexgpt"])
    # dp.register_message_handler(cmd_delete_dialog, commands=["delete_dialog"])
    dp.register_message_handler(text_handler, content_types=types.ContentType.TEXT)
