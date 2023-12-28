import os
from aiogram.types import InputFile
import more_category
import photo_hendler_two
import utils
from keyboards.Inline import Inline_keyboard


import sys

# Установите кодировку консоли на UTF-8

# Установите кодировку консоли на UTF-8

image_captions = [
    ["planers/categor",
        [
            ["0", "Ежедневник 'ToDo'", "planers/planers_1", "📓 *Формат:* А5\n📄 *104 листа*\n🕒 *Без привязки к году/месяцам*\n🔖 *Твердый переплет*", "more/planners_1"],
            ["1", "Ежедневник (без рисунков)", "planers/planers_2", "📘 *Формат:* B6\n📄 *104 листа с различной разлиновкой* (на месяц, каждый день)\n🗓️ *Рассчитан на 13 месяцев по 31 дню*\n🕒 *Без привязки к году/месяцам*\n✍️ *К каждому месяцу есть:* \n -трекер привычек\n -лист с задачами\n🔖 *Твердый переплет: Ляссе*", "more/planners_2"],
            ["2", "Ежедневник (с рисунками)", "planers/planers_3", "📘 *Формат:* B6\n📄 *104 листа с различной разлиновкой* (на месяц, каждый день)\n🗓️ *Рассчитан на 13 месяцев по 31 дню*\n🕒 *Без привязки к году/месяцам*\n✍️ *К каждому месяцу есть: трекер привычек, лист с задачами*\n🔖 *Твердый переплет: Ляссе*", "more/planners_3"],
            ["3", "Ежедневник '365'", "planers/planers_4", "📒 *Формат:* B6\n📄 *104 листа с различной разлиновкой:*\n    - в точку\n    - в линейку\n    - в клетку\n    - с рисунками\n🕒 *Без привязки к году/месяцам*\n🔖 *Твердый переплет: Ляссе*", "more/planners_4"]
        ]
    ],
    ["covers/categor",
        [
            ["0", "Обложка на документы", "covers/covers_1", "📁 *Компактная обложка* вмещает техпаспорт, страховку, права и другие документы.\n🎫 *Внутри вкладыш с 6 кармашками разного размера* (1шт. размера 10х7; 4шт. - 12,5х9; 1шт. - 22,5х15,5 складывается 2 раза).\n🔁 *Вкладыш можно достать и использовать как обложку для паспорта*.", "more/covers_1"],
            ["1", "Обложка на зачетную книжку", "covers/covers_2", "📘 *Удобный чехол* на зачетную книжку", "more/covers_2"],
            ["2", "Обложка на студенческий", "covers/covers_3", "📘 *Удобный чехол* на студенческий", "more/covers_3"]
        ]
    ],
    ["cardholder/categor",

        [
            ["0","Кард-холдер","cardholder/cardholder_1", "💳 *Удобный чехол* под магнитную карту", "more/cardholder_1"],
        ]
    ]
]


async def start_send_photo(bot, chat_id, image_dir):
    global current_category_index
    current_category_index = 0
    global image_direct
    image_direct = image_dir
    global categories_1
    for category, subcategories in image_captions:
        print(f"sdsds {category}")
        print(f"subsdsds {subcategories}")
        print(image_direct)
        if image_direct == category:
            categories_1 = [subcategory[1] for subcategory in subcategories]
            print(categories_1)

    await send_photo(bot, chat_id, current_category_index)



async def send_photo(bot, chat_id, current_cat_ind):
    global current_message_id
    global current_image_index
    global current_photo_path
    global current_category_index
    current_category_index = current_cat_ind
    current_message_id = None
    for category, subcategories in image_captions:
        if image_direct == category:
            if 0 <= current_category_index < len(subcategories):
                category_info = subcategories[current_category_index]
            # category_info = subcategories[current_category_index]
                category_name, category_path_suffix = category_info[1], category_info[2]
                print(f"category_info {category_info} Category_name {category_name}")
                category_path = os.path.join(image_direct)
                images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]

                current_image_index = 0

                current_photo_path = os.path.join(category_path, images[current_image_index])
                caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
                current_message_id = (await bot.send_photo(chat_id, InputFile(current_photo_path), caption=caption_text, reply_markup=Inline_keyboard.category_product)).message_id
                print("send photo in ph")
                print(current_message_id)



async def send_photo_to_categorical(bot, chat_id, current_category_index, message_id):
    print("send_to_categorical in ph")
    for category, subcategories in image_captions:
        if image_direct == category:
            category_info = subcategories[current_category_index]
            category_name, category_path_suffix = category_info[1], category_info[2]
            global current_image_index
            current_image_index = 0
            await photo_hendler_two.send_photo(bot,chat_id,category_path_suffix,category_name, message_id, current_category_index)


async def process_callback(bot, callback_query):
    global current_category_index
    global current_photo_path
    global current_image_index

    print(current_category_index)
    if callback_query.data == 'back':
        # if current_category_index > 0:
            current_category_index = (current_category_index - 1) % len(categories_1)
    elif callback_query.data == 'forward':
        # if current_category_index < len(categories_1):
            current_category_index = (current_category_index + 1) % len(categories_1)

    elif callback_query.data == 'choose_enter_categorical':
        print("Callback ph")
        print(callback_query.message.message_id)
        # category_name, category_path_suffix = categories_1[current_category_index], \
        #                                      image_captions[0][1][current_category_index][2]
        # await bot.send_message(callback_query.message.chat.id, f"Вы выбрали категорию: {category_name}")
        await send_photo_to_categorical(bot, callback_query.message.chat.id, current_category_index, callback_query.message.message_id)


    for category, subcategories in image_captions:
        if image_direct == category:
            category_info = subcategories[current_category_index]
            print(f"Callback category info {category_info}")
            category_name, category_path_suffix = category_info[1], category_info[2]
            category_path = os.path.join(image_direct)
            images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
            if callback_query.data == 'back':
                # if current_image_index > 0:
                current_image_index = (current_image_index - 1) % len(images)
                current_photo_path = os.path.join(category_path,images[current_image_index])
                print(f"images {images[current_image_index]}")
                caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
                await utils.update_photo(bot,callback_query.message.chat.id,current_photo_path,caption_text,
                                         callback_query.message.message_id,inline_kb = Inline_keyboard.category_product)
            elif callback_query.data == 'forward':
                # if current_image_index < len(images) - 1:
                current_image_index = (current_image_index + 1) % len(images)
                current_photo_path = os.path.join(category_path,images[current_image_index])
                print(f"images2 {images[current_image_index]}")
                caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
                await utils.update_photo(bot,callback_query.message.chat.id,current_photo_path,caption_text,
                                         callback_query.message.message_id,inline_kb = Inline_keyboard.category_product)
            elif callback_query.data == "more":
                if image_direct == category:
                    category_info = subcategories[current_category_index]
                    more_text = category_info[3]
                    more_path = category_info[4]
                    await bot.delete_message(callback_query.message.chat.id, message_id = callback_query.message.message_id)
                    await more_category.start_send_photo_more(bot,callback_query.message.chat.id,current_photo_path, image_direct, more_path, more_text)

            elif callback_query.data == "back_to_choose":
                await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
                current_category_index = 0
                await send_photo(bot,callback_query.from_user.id, current_category_index)
                # return
            # elif callback_query.data == 'back_return':
            #     # async def back_return(callback_query: types.CallbackQuery):
            #     await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            #     # await bot.send_message(callback_query.message.chat.id, "")
            #     await main.return_handle_catalog(bot, callback_query.message.chat.id)

            await utils.update_photo(bot = bot, chat_id = callback_query.message.chat.id, photo_path = current_photo_path, caption = caption_text, message_id = callback_query.message.message_id, inline_kb = Inline_keyboard.category_product)