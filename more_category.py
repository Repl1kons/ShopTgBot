import os

from aiogram.types import InputMediaPhoto
import photo_handler
from aiogram.types import InputFile

from keyboards.Inline import Inline_keyboard

async def start_send_photo_more(bot, chat_id, path_dir, patha, more_path, more_text):
    global path_a
    path_a = patha
    more_dir = more_path
    text = more_text
    print(f"more path {more_dir}")
    print(f"more text {text}")
    global image_direct
    image_direct = path_dir
    await send_photo(bot, chat_id, more_path, more_text)


async def send_photo(bot, chat_id, more_path, more_text):
    global path
    path = os.path.join(more_path)
    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # print(category_path)
    print(images)
    global current_image_index
    current_image_index = 0
    current_photo_path = os.path.join(path,images[current_image_index])
    global text
    text = more_text
    global current_message_id
    len_photo = f"*{current_image_index + 1}/{len(images)}*"
    current_message_id = (await bot.send_photo(chat_id,InputFile(current_photo_path),caption = f"{len_photo}\n{text}",
                                           reply_markup = Inline_keyboard.category_product_1, parse_mode = 'Markdown')).message_id


async def process_callback(bot, callback_query):
    global message_id
    global path_a
    global image_direct
    global current_image_index
    global path
    global current_message_id
    global text


    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]

    if callback_query.data == 'more_back_return':
        await bot.delete_message(chat_id = callback_query.message.chat.id,message_id = current_message_id)
        await photo_handler.start_send_photo(bot, callback_query.message.chat.id, image_dir = path_a)
    if callback_query.data == 'forward_1':
        current_image_index = (current_image_index + 1) % len(images)
        amount = 1
        print(current_image_index)
    if callback_query.data == 'back_1':
        if current_image_index > 0:
            current_image_index = (current_image_index - 1) % len(images)
            amount = 1
            print(current_image_index)
    len_photo = f"*{current_image_index+1}/{len(images)}*"
    photo_path = os.path.join(path,images[current_image_index])
    await bot.edit_message_media(
        media = InputMediaPhoto(InputFile(photo_path), caption = f"{len_photo}\n{text}", parse_mode = 'Markdown'),
        chat_id = callback_query.message.chat.id,
        message_id = current_message_id,
        reply_markup = Inline_keyboard.category_product_1,
    )