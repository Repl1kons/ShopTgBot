from photo_handler import start_send_photo
from aiogram import types
from keyboards.Inline import Inline_keyboard

async def handle_catalog_button(bot, chat_id):
    global messageid
    messageid = (await bot.send_message(chat_id, "Выберите категорию товаров", reply_markup = Inline_keyboard.show_catalogs)).message_id



async def show_category_products(bot, chat_id, category):
    global messageid
    # await bot.delete_message(chat_id = chat_id, message_id = messageid)
    if category == "📔 Ежедневники":
        await bot.send_message(chat_id, "Выберите конкретный ежедневник:")
        path = "planers/categor"
        await start_send_photo(bot, chat_id, path)
    if category == "🖼 Обложки":
        await bot.send_message(chat_id, "Выберите конкретную обложку:")
        path = "covers/categor"
        await start_send_photo(bot, chat_id, path)
    if category == "💳 Кард-холдеры":
        await bot.send_message(chat_id, "Выберите конкретный кард-холдер:")
        path = "cardholder/categor"
        await start_send_photo(bot, chat_id, path)
