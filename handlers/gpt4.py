from aiogram import types
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


async def gpt4_handler(msg: types.Message):
    try:
        config.set('State', 'MODEL_GPT', 'gpt4')
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        await msg.answer(text="chatgpt-4")
        await msg.answer(
            text="Чтобы все могли воспользоваться gpt4, у бота есть ограничения на скорость и он может работать нестабильно. "
                 "Переключиться на стабильную версию: /gpt3"
        )
    except Exception as _ex:
        await msg.answer(text="Не удалось(")
