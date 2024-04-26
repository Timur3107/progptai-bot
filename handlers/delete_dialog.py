from aiogram import types
from database.requests import delete_dialogue

# в разработке
async def cmd_delete_dialog(msg: types.Message):
    await delete_dialogue(msg.chat.id)
    await msg.reply("Диалог успешно очищен!")

