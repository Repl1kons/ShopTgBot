from photo_handler import start_send_photo
from aiogram import types

product_categories = ['📔 Ежедневники', '💳 Кард-холдеры', '🖼 Обложки']

async def handle_catalog_button(bot, chat_id):
    markup = types.InlineKeyboardMarkup(row_width = 1)  # Создаем Inline клавиатуру
    for category in product_categories:
        button = types.InlineKeyboardButton(text = category,callback_data = f'category_{category}')
        markup.add(button)

    await bot.send_message(chat_id, "Выберите категорию товаров", reply_markup = markup)



async def show_category_products(bot, chat_id, category):
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
