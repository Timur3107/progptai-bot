from aiogram import types
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


async def yagpt_handler(msg: types.Message):
    try:
        config.set('State', 'MODEL_GPT', 'yandexgpt')
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        await msg.answer(text="yandex-gpt-lite")
    except Exception as _ex:
        await msg.answer(text="Не удалось(")
