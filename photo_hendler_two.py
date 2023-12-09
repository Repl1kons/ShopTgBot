import os
import re
from aiogram.types import InputFile
from aiogram import types
from keyboards.Inline import Inline_keyboard
import corsina
import photo_handler

grouped_prices = {
    r"100\d{3}": 490,
    r"2001\d{2}": 320,
    r"2002\d{2}": 250,
    r"2003\d{2}": 200,
    r"3001\d{2}": 120}

async def send_photo(bot, chat_id, path_dir, category_name, message_id):
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

    await bot.edit_message_media(media = types.InputMediaPhoto(InputFile(photo_path), caption = caption_text),
                                 chat_id = chat_id,
                                 message_id = message_id,
                                 reply_markup = Inline_keyboard.product_show)


async def process_callback(bot, callback_query):
    global amount
    global current_image_index
    global cat_name
    global message_id

    path_dir = os.path.join(image_direct) # path
    images = [f for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]

    if callback_query.data == "back_to_choose":
        await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
        await photo_handler.send_photo(bot,callback_query.message.chat.id, current_image_index)

    if callback_query.data == 'back-enter':
        if current_image_index > 0:
            current_image_index = (current_image_index - 1) % len(images)
            amount = 1
            print(current_image_index)
    elif callback_query.data == 'forward-enter':
        # if current_image_index < len(images) - 1: # что бы списки не прокручивались после того как закончились
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
        category_numb = category
        products_number = images[current_image_index].split('.')[0].split('_')[3]
        articul = f"{products_to_choose}00{category}00{products_number}"
        print(products_to_choose)
        print(category)
        print(articul)

        for pattern, price in grouped_prices.items():
            if re.match(pattern,articul):
                await corsina.add_to_cart(callback_query.message.chat.id,cat_name,articul,current_image_index + 1,amount,price, category_numb)


                await bot.send_message(callback_query.message.chat.id,
                                       f"Товар {cat_name}:\n\nАртикул: {articul}\nВыбранный вариант: {current_image_index + 1}\nКоличество: {amount}\nЦена: {price * amount}\n\nБыл успешно добавлен в корзину 💵‍",
                                       reply_markup = Inline_keyboard.show_basket_add)

    photo_path = os.path.join(path_dir, images[current_image_index])
    print(photo_path)
    caption_text = f"\n{current_image_index + 1}/{len(images)}\nКол-во: {amount}"

    await bot.edit_message_media(
        media=types.InputMediaPhoto(InputFile(photo_path), caption_text),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=Inline_keyboard.product_show
    )