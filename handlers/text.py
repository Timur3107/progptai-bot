from aiogram import types
import os
from dotenv import load_dotenv
import openai
import configparser
import g4f
import requests

config = configparser.ConfigParser()

load_dotenv('.env')

token = os.getenv('OPENAI_TOKEN')
openai.api_key = token
max_token_count = 4096

count_tokens_gpt4 = 0
count_tokens_yandexgpt = 0

context_chatgpt3 = []
context_chatgpt4 = []
context_yandexgpt = []


def update(context, role, content, yandex=False):
    if yandex:
        context.append({"role": role, "text": content})
    else:
        context.append({"role": role, "content": content})


def delete_contex():
    global count_tokens_gpt4, count_tokens_yandexgpt
    context_chatgpt3.clear()
    context_chatgpt4.clear()
    context_yandexgpt.clear()
    count_tokens_gpt4 = 0
    count_tokens_yandexgpt = 0


async def chatgpt3_message_handler(msg):
    update(context_chatgpt3, 'user', msg.text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context_chatgpt3,
        temperature=0.5,
        max_tokens=100,
        timeout=20
    )

    answer_chatgpt = response['choices'][0]['message']['content']
    update(context_chatgpt3, 'assistant', answer_chatgpt)

    if response['usage']['total_tokens'] >= max_token_count:
        await msg.answer(
            f'Сейчас вы использовали максимум токенов: ваш диалог сброшен. Продолжайте работу')
        delete_contex()
    await msg.answer(answer_chatgpt)


async def chatgpt4_message_handler(msg):
    global count_tokens_gpt4
    update(context_chatgpt4, 'user', msg.text)
    count_tokens_gpt4 += len(msg.text)

    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_4_32k_0613,
        messages=context_chatgpt4,
        # provider=g4f.Provider.Bing,
    )
    update(context_chatgpt4, 'assistant', response)

    count_tokens_gpt4 += len(response)

    if count_tokens_gpt4 >= max_token_count:
        await msg.answer(
            f'Сейчас вы использовали максимум токенов: ваш диалог сброшен. Продолжайте работу')
        delete_contex()
    await msg.answer(response)


async def yandexgpt_message_handler(msg):
    global count_tokens_yandexgpt
    update(context_yandexgpt, 'user', msg.text, yandex=True)
    count_tokens_yandexgpt += len(msg.text)

    prompt = {
        "modelUri": str(os.getenv('MODEL_URI')),
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000"
        },
        "messages": context_yandexgpt
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f'Api-Key {str(os.getenv("YANDEX_GPT_TOKEN"))}'
    }
    response = requests.post(url, json=prompt, headers=headers).json()
    yandex_gpt_answer = response["result"]["alternatives"][0]["message"]["text"]

    update(context_yandexgpt, 'assistant', yandex_gpt_answer, yandex=True)
    count_tokens_yandexgpt += len(yandex_gpt_answer)

    if count_tokens_yandexgpt >= max_token_count:
        await msg.answer(
            f'Сейчас вы использовали максимум токенов: ваш диалог сброшен. Продолжайте работу')
        delete_contex()

    await msg.answer(yandex_gpt_answer)


async def text_handler(msg: types.Message):
    config.read('config.ini')
    user_id = str(msg.from_user.id)
    if user_id != os.getenv('ALLOWED_CHAT_ID'):
        print(f"Отказано в доступе для пользователя с ID {user_id}")
        return

    loading_message = None
    try:
        loading_message = await msg.answer("Loading...")
        if config['State']['MODEL_GPT'] == "gpt3":
            await chatgpt3_message_handler(msg)
        elif config['State']['MODEL_GPT'] == "gpt4":
            await chatgpt4_message_handler(msg)
        else:
            await yandexgpt_message_handler(msg)
    except Exception as _ex:
        await msg.answer(
            text=f"Error: {_ex}"
        )

    await loading_message.delete()
