from database.models import User
from database.engine import async_session
from sqlalchemy import select


async def get_user(chat_id):
    async with async_session() as session:
        user = await session.scalars(select(User).where(User.telegram_id == chat_id))
        return user.first()


async def add_user(chat_id):
    async with async_session() as session:
        user = User(telegram_id=chat_id, model_gpt="gpt3", chatgpt_dialogue_history=[], yandexgpt_dialogue_history=[])
        session.add(user)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()


async def add_dialogue(chat_id, new_dialog, old_dialog, yandex=False):
    async with async_session() as session:
        user = await session.scalars(select(User).where(User.telegram_id == chat_id))
        if yandex:
            old_dialog.append(new_dialog)
            user.first().yandexgpt_dialogue_history = old_dialog
        else:
            old_dialog.append(new_dialog)
            user.first().chatgpt_dialogue_history = old_dialog

        try:
            await session.commit()
        except Exception as e:
            session.rollback()


async def change_model_gpt(chat_id, new_model_gpt):
    async with async_session() as session:
        user = await session.scalars(select(User).where(User.telegram_id == chat_id))
        user.first().model_gpt = new_model_gpt
        try:
            await session.commit()
        except Exception as e:
            session.rollback()


async def delete_dialogue(chat_id):
    async with async_session() as session:
        user = await session.scalars(select(User).where(User.telegram_id == chat_id))

        user.first().yandexgpt_dialogue_history = []
        user.first().chatgpt_dialogue_history = []

        try:
            await session.commit()
        except Exception as e:
            session.rollback()
