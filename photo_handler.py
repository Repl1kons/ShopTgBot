from aiogram import types
import photo_hendler_two
from keyboards.Inline import Inline_keyboard
import gspread


async def init_image_caption(worksheet):
    image_captions = []

    gc = gspread.service_account(filename = 'shoptg-97da5d92bfcd.json')
    sh = gc.open("ShopTgTable")
    worksheet = sh.worksheet(worksheet)
    for index, row in enumerate(worksheet.get_all_values()):
        if index == 0:
            continue  # Пропускаем 1 строку
        if row:
            category = row[0]
            subcategories = []
            for i in range(0, len(row), 5):
                subcategory = [row[i], row[i + 1], row[i + 2], row[i + 3], row[i + 4]]
                subcategories.append(subcategory)
            image_captions.append([category, subcategories])
    return image_captions


async def send_photo(bot, chat_id, product):

    cur_img_ind = 0
    cur_img_cap = 1

    keyboard = Inline_keyboard.create_category_keyboard(cur_img_ind, cur_img_cap, product)

    image_captions = await init_image_caption(product)
    print(image_captions[cur_img_ind][1][0][0])

    caption = f"{cur_img_cap}/{len(image_captions)}\n{image_captions[cur_img_ind][1][0][1]}\nЦена: {image_captions[cur_img_ind][1][0][4]}"

    await bot.send_photo(chat_id,
                         photo = image_captions[cur_img_ind][1][0][0],
                         caption = caption,
                         reply_markup = keyboard)

#
#
#
# async def send_photo_to_categorical(bot, chat_id, current_category_index, message_id):
#     print("send_to_categorical in ph")
#     for category, subcategories in image_captions:
#         if image_direct == category:
#             category_info = subcategories[current_category_index]
#             category_name, category_path_suffix = category_info[1], category_info[2]
#             global current_image_index
#             current_image_index = 0
#             await photo_hendler_two.send_photo(bot,chat_id,category_path_suffix,category_name, message_id, current_category_index)
#
#
async def process_callback(bot, callback_query, cur_img_indx, cur_img_caption, product, db):
    image_captions = await init_image_caption(product)

    if callback_query.data.startswith('categoryBack'):
        if cur_img_indx > 0:
            cur_img_indx -= 1
            cur_img_caption -= 1
        await callback_query.answer()
    elif callback_query.data.startswith('categoryForward'):
        if cur_img_caption < len(image_captions):  # что бы списки не прокручивались после того как закончились
            cur_img_indx += 1
            cur_img_caption += 1
        await callback_query.answer()


    elif callback_query.data.startswith('choose-enter-categorical'):
        product_object = product.replace("category", '').lower()
        path_more = image_captions[cur_img_indx][1][0][2]
        current_price = int(image_captions[cur_img_indx][1][0][4])
        product_name = image_captions[cur_img_indx][1][0][1]
        path_name = f"{product_object}"
        # category_name, category_path_suffix = categories_1[current_category_index], \
        #                                      image_captions[0][1][current_category_index][2]
        # await bot.send_message(callback_query.message.chat.id, f"Вы выбрали категорию: {category_name}")
        await db.State.update_one(dict(
            _id = callback_query.from_user.id),
            {
                "$set": {'notebook.path_more': path_more,
                         'notebook.path_name': path_name,
                         'notebook.more.cur_img_ind': cur_img_indx,
                         'notebook.product_name': product_name}
            }
        )
        await photo_hendler_two.send_photo(bot, callback_query, product_object, db)
#
#     for category, subcategories in image_captions:
#         if image_direct == category:
#             category_info = subcategories[current_category_index]
#             print(f"Callback category info {category_info}")
#             category_name, category_path_suffix = category_info[1], category_info[2]
#             category_path = os.path.join(image_direct)
#             images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
#             if callback_query.data == 'back':
#                 # if current_image_index > 0:
#                 current_image_index = (current_image_index - 1) % len(images)
#                 current_photo_path = os.path.join(category_path,images[current_image_index])
#                 print(f"images {images[current_image_index]}")
#                 caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
#                 await utils.update_photo(bot,callback_query.message.chat.id,current_photo_path,caption_text,
#                                          callback_query.message.message_id,inline_kb = Inline_keyboard.category_product)
#             elif callback_query.data == 'forward':
#                 # if current_image_index < len(images) - 1:
#                 current_image_index = (current_image_index + 1) % len(images)
#                 current_photo_path = os.path.join(category_path,images[current_image_index])
#                 print(f"images2 {images[current_image_index]}")
#                 caption_text = f"{category_name}\n{current_image_index + 1}/{len(images)}"
#                 await utils.update_photo(bot,callback_query.message.chat.id,current_photo_path,caption_text,
#                                          callback_query.message.message_id,inline_kb = Inline_keyboard.category_product)
#             elif callback_query.data == "more":
#                 if image_direct == category:
#                     category_info = subcategories[current_category_index]
#                     more_text = category_info[3]
#                     more_path = category_info[4]
#                     await bot.delete_message(callback_query.message.chat.id, message_id = callback_query.message.message_id)
#                     await more_category.start_send_photo_more(bot,callback_query.message.chat.id,current_photo_path, image_direct, more_path, more_text)
#
#             elif callback_query.data == "back_to_choose":
#                 await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
#                 current_category_index = 0
#                 await send_photo(bot,callback_query.from_user.id, current_category_index)
#                 # return
#             elif callback_query.data == 'back_return':
#                 # async def back_return(callback_query: types.CallbackQuery):
#                 await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
#                 # await bot.send_message(callback_query.message.chat.id, "")
#                 await main.return_handle_catalog(bot, callback_query.message.chat.id)
    media = image_captions[cur_img_indx][1][0][0]
    caption = f"{cur_img_caption}/{len(image_captions)}\n{image_captions[cur_img_indx][1][0][1]}\nЦена: {image_captions[cur_img_indx][1][0][4]}"
    keyboard = Inline_keyboard.create_category_keyboard(cur_img_indx, cur_img_caption, product)

    await bot.edit_message_media(
        media = types.InputMediaPhoto(media,caption = caption),
        chat_id = callback_query.message.chat.id,
        message_id = callback_query.message.message_id,
        reply_markup = keyboard)