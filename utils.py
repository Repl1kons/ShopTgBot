from aiogram.types import InputFile
from aiogram import types

async def update_photo(bot, chat_id, photo_path, caption, message_id, inline_kb):
    await bot.edit_message_media(
        media=types.InputMediaPhoto(InputFile(photo_path), caption=caption),
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=inline_kb
    )

