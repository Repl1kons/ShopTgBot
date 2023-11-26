import os
import re

from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

shopping_cart = {}
grouped_prices = {
    r"100\d{3}": 490,
    r"2001\d{2}": 320,
    r"2002\d{2}": 250,
    r"2003\d{2}": 200,
    r"3001\d{2}": 120


}





inline_kb = InlineKeyboardMarkup(row_width=2)
btn_back = InlineKeyboardButton(text='⬅', callback_data='back-enter')
btn_forward = InlineKeyboardButton(text='➡', callback_data='forward-enter')
amount_sum = InlineKeyboardButton(text='➕', callback_data='amount_sum')
amount_min = InlineKeyboardButton(text='➖', callback_data='amount_min')
btn_enter = InlineKeyboardButton(text='Добавить в корзину', callback_data='choose_enter')
inline_kb.add(btn_back, btn_forward, amount_min, amount_sum, btn_enter)

# async def update_photo(bot, chat_id, message_id, photo_path, caption):
#     # Используем edit_message_media для обновления фото и подписи
#     await bot.edit_message_media(
#         media=types.InputMediaPhoto(InputFile(photo_path), caption=caption),
#         chat_id=chat_id,
#         message_id=message_id,
#         reply_markup=inline_kb
#     )

async def send_photo(bot, chat_id, path_dir, category_name):
    global amount
    amount = 1
    global current_image_index
    current_image_index = 0
    global cat_name
    cat_name = category_name

    print(cat_name)
    global image_direct
    image_direct = path_dir

    images = [f for f in os.listdir(image_direct) if os.path.isfile(os.path.join(image_direct, f))]
    photo_path = os.path.join(image_direct, images[current_image_index])
    caption_text = f"\n{current_image_index + 1}/{len(images)}\nКол-во: {amount}"
    await bot.send_photo(chat_id,InputFile(photo_path),caption = caption_text,reply_markup = inline_kb)




async def process_callback(bot, callback_query):
    global amount
    global current_image_index
    global cat_name

    path_dir = os.path.join(image_direct)
    images = [f for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]

    if callback_query.data == 'back-enter':
        if current_image_index > 0:
            current_image_index = (current_image_index - 1) % len(images)
            amount = 1
            print(current_image_index)
    elif callback_query.data == 'forward-enter':
        if current_image_index < len(images) - 1:
            current_image_index = (current_image_index + 1) % len(images)
            amount = 1
            print(current_image_index)
    elif callback_query.data == 'amount_sum':
        amount += 1
    elif callback_query.data == 'amount_min':
        if amount > 1:
            amount -= 1
    elif callback_query.data == 'choose_enter':
        products_to_choose = images[current_image_index].split('_')[1]
        category = images[current_image_index].split('_')[2]
        products_number = images[current_image_index].split('.')[0].split('_')[3]
        articul = f"{products_to_choose}00{category}00{products_number}"

        for pattern,price in grouped_prices.items():
            if re.match(pattern,articul):
                key = f"{cat_name}_{articul}"
                if key in shopping_cart:
                    shopping_cart[key][2] += amount
                    shopping_cart[key][3] += price  # Обновление общей цены
                else:
                    # Добавление нового товара в корзину
                    shopping_cart[key] = [current_image_index,articul,amount,price]

                await bot.send_message(callback_query.message.chat.id,
                                       f"Вы выбрали {images[current_image_index]} ||| Название: {cat_name} ||| Выбранный вариант: {current_image_index + 1} ||| Артикул: {articul} ||| Количество: {amount} ||| Цена: {price * amount}")
                print(shopping_cart[key])
                break
        else:
            await bot.send_message(callback_query.message.chat.id,"Для этого товара нет цены в системе.")

    photo_path = os.path.join(path_dir, images[current_image_index])
    print(photo_path)
    caption_text = f"\n{current_image_index + 1}/{len(images)}\nКол-во: {amount}"

    await bot.edit_message_media(
        media=types.InputMediaPhoto(InputFile(photo_path), caption_text),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=inline_kb
    )