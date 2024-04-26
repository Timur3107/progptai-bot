from aiogram import types
import os
from dotenv import load_dotenv
import openai
import configparser
import g4f
import requests
from database.requests import get_user
from database.requests import add_dialogue

config = configparser.ConfigParser()

load_dotenv('.env')

token = os.getenv('OPENAI_TOKEN')
openai.api_key = token


async def conversion_requests(chat_id, role, content, old_dialog, yandex=False):
    if yandex:
        d = {"role": role, "text": content}
    else:
        d = {"role": role, "content": content}
    await add_dialogue(chat_id, d, old_dialog, yandex)


async def chatgpt3_message_handler(msg, history):
    await conversion_requests(msg.chat.id, 'user', msg.text, history)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        temperature=0.5,
        max_tokens=100,
        timeout=20
    )

    answer_chatgpt = response['choices'][0]['message']['content']
    await conversion_requests(msg.chat.id, 'assistant', answer_chatgpt, history)
    await msg.answer(answer_chatgpt)


async def chatgpt4_message_handler(msg, history):
    await conversion_requests(msg.chat.id, 'user', msg.text, history)
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_4_32k_0613,
        messages=history,
        # provider=g4f.Provider.Bing,
    )
    await conversion_requests(msg.chat.id, 'assistant', response, history)
    await msg.answer(response)


async def yandexgpt_message_handler(msg, history_yandex):
    await conversion_requests(msg.chat.id, 'user', msg.text, history_yandex, yandex=True)

    prompt = {
        "modelUri": str(os.getenv('MODEL_URI')),
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000"
        },
        "messages": history_yandex
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f'Api-Key {str(os.getenv("YANDEX_GPT_TOKEN"))}'
    }
    response = requests.post(url, json=prompt, headers=headers).json()
    yandex_gpt_answer = response["result"]["alternatives"][0]["message"]["text"]

    await conversion_requests(msg.chat.id, 'assistant', yandex_gpt_answer, history_yandex, yandex=True)

    await msg.answer(yandex_gpt_answer)


async def text_handler(msg: types.Message):
    # config.read('config.ini')
    # user_id = str(msg.from_user.id)
    # if user_id != os.getenv('ALLOWED_CHAT_ID'):
    #     print(f"Отказано в доступе для пользователя с ID {user_id}")
    #     return

    user = await get_user(msg.chat.id)
    if not user:
        await msg.answer(text=f"Пожалуйста, зарегистрируйтесь: /start")
        return

    loading_message = None
    try:
        loading_message = await msg.answer("Loading...")
        if user.model_gpt == "gpt3":
            await chatgpt3_message_handler(msg, user.chatgpt_dialogue_history)
        elif user.model_gpt == "gpt4":
            await chatgpt4_message_handler(msg, user.chatgpt_dialogue_history)
        else:
            await yandexgpt_message_handler(msg, user.yandexgpt_dialogue_history)
    except Exception as _ex:
        await msg.answer(
            text=f"Error: {_ex}"
        )

    await loading_message.delete()
