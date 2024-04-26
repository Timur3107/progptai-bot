from aiogram import types
from database.requests import change_model_gpt

async def change_models(msg: types.Message, new_model_gpt):
    try:
        await change_model_gpt(msg.chat.id, new_model_gpt)
        await msg.answer(text="successful")
    except Exception as e:
        await msg.answer(text=f"Error: {e}")


