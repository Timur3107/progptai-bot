from aiogram import types
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


async def gpt3_handler(msg: types.Message):
    try:
        config.set('State', 'MODEL_GPT', 'gpt3')
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        await msg.answer(text="chatgpt-3-turbo")
    except Exception as _ex:
        await msg.answer(text="Не удалось(")
        print(_ex)

