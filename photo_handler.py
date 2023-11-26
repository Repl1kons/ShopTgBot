import os
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

import photo_hendler_two

image_captions = [
    ["planers/categor",
        [
            ["0", "Ежедневник 'ToDo'", "planers/planers_1"],
            ["1", "Ежедневник (без рисунков)", "planers/planers_2"],
            ["2", "Ежедневник (с рисунками)", "planers/planers_3"],
            ["3", "Ежедневник '365'", "planers/planers_4"]
        ]
    ],
    ["covers/categor",
        [
            ["0", "Обложка на документы", "covers/covers_1"],
            ["1", "Обложка на зачетную книжку", "covers/covers_2"],
            ["2", "Обложка на студенческий", "covers/covers_3"]
        ]
    ],
    ["cardholder/categor",

        [
            ["0","Кард-холдер","cardholder/cardholder_1"],
        ]
    ]

]

async def start_send_photo(bot, chat_id, image_dir):
    global image_direct
    image_direct = image_dir
    global categories_1
    for category, subcategories in image_captions:
        print(category)
        print(image_direct)
        if image_direct == category:
            categories_1 = [subcategory[1] for subcategory in subcategories]
            print(categories_1)
    global current_category_index
    current_category_index = 0
    await send_photo(bot, chat_id, current_category_index)

inline_kb = InlineKeyboardMarkup(row_width=2)
btn_back = InlineKeyboardButton(text='⬅', callback_data='back')
btn_forward = InlineKeyboardButton(text='➡', callback_data='forward')
details = InlineKeyboardButton(text='Подробнее', callback_data='details')
btn_enter = InlineKeyboardButton(text='Подтвердить выбор', callback_data='choose_enter_categorical')
inline_kb.add(btn_back, btn_forward, btn_enter)


async def send_photo(bot, chat_id, current_category_index):
    for category, subcategories in image_captions:
        if image_direct == category:
            category_info = subcategories[current_category_index]
            global category_path_suffix
            category_name, category_path_suffix = category_info[1], category_info[2]
            print(f"category_info {category_info} Category_name {category_name}")
            category_path = os.path.join(image_direct)
            images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
            global current_image_index
            current_image_index = 0
            global current_photo_path
            current_photo_path = os.path.join(category_path, images[current_image_index])
            caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
            global current_message_id
            current_message_id = (await bot.send_photo(chat_id, InputFile(current_photo_path), caption=caption_text, reply_markup=inline_kb)).message_id

async def update_photo_caption(bot, chat_id, message_id, caption):
    await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, reply_markup=inline_kb)

async def update_photo(bot, chat_id, photo_path, caption, message_id):
    await bot.edit_message_media(
        media=types.InputMediaPhoto(InputFile(photo_path), caption=caption),
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=inline_kb
    )




async def send_photo_to_categorical(bot, chat_id, current_category_index):
    for category, subcategories in image_captions:
        if image_direct == category:
            category_info = subcategories[current_category_index]
            category_name, category_path_suffix = category_info[1], category_info[2]
            global current_image_index
            current_image_index = 0
            await photo_hendler_two.send_photo(bot,chat_id,category_path_suffix,category_name)


async def process_callback(bot, callback_query):
    global current_category_index
    if callback_query.data == 'back':
        if current_category_index > 0:
            current_category_index = (current_category_index - 1) % len(categories_1)
    elif callback_query.data == 'forward':
        if current_category_index < len(categories_1) - 1:
            current_category_index = (current_category_index + 1) % len(categories_1)
    elif callback_query.data == 'choose_enter_categorical':
        category_name, category_path_suffix = categories_1[current_category_index], \
                                             image_captions[0][1][current_category_index][2]
        await bot.send_message(callback_query.message.chat.id, f"Вы выбрали категорию: {category_name}")
        await send_photo_to_categorical(bot, callback_query.message.chat.id, current_category_index)
    for category, subcategories in image_captions:
        if image_direct == category:
            category_info = subcategories[current_category_index]
            print(f"Callback category info {category_info}")
            category_name, category_path_suffix = category_info[1], category_info[2]
            category_path = os.path.join(image_direct)
            images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
            global current_image_index
            if callback_query.data == 'back':
                if current_image_index > 0:
                    current_image_index = (current_image_index - 1) % len(images)
            elif callback_query.data == 'forward':
                if current_image_index < len(images) - 1:
                    current_image_index = (current_image_index + 1) % len(images)

            global current_photo_path
            current_photo_path = os.path.join(category_path, images[current_image_index])
            caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
            await update_photo(bot, callback_query.message.chat.id, current_photo_path, caption_text, callback_query.message.message_id)
