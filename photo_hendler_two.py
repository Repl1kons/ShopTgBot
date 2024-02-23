# import os
# import re
# from aiogram.types import InputFile
# from aiogram import types
#
# import data.db.database
# from keyboards.Inline import Inline_keyboard
# import corsina
# import photo_handler
#
# grouped_prices = {
#     r"100\d{3}": 490,
#     r"2001\d{2}": 320,
#     r"2002\d{2}": 250,
#     r"2003\d{2}": 200,
#     r"3001\d{2}": 120}
#
# async def send_photo(bot, message, path_dir, category_name, category_index):
#     amount = 1
#     global current_image_index
#     current_image_index = 0
#     global cat_name
#     cat_name = category_name
#     global category_numb
#     category_numb = category_index
#
#     print(cat_name)
#     global image_direct
#     image_direct = path_dir
#     # global all_amount
#     images = [f for f in os.listdir(image_direct) if os.path.isfile(os.path.join(image_direct, f))]
#     photo_path = os.path.join(image_direct, images[current_image_index])
#     products_to_choose = images[current_image_index].split('_')[1]
#     category = images[current_image_index].split('_')[2]
#     category_numb = category
#     products_number = images[current_image_index].split('.')[0].split('_')[3]
#     articul = f"{products_to_choose}00{category}00{products_number}"
#
#     all_amount = data.db.database.get_all_amount(articul)
#     if all_amount[0] > 0:
#         caption_text = f"\n{current_image_index + 1}/{len(images)}\nАртикул: {articul}\nОсталось: {all_amount[0]}\nКол-во: {amount}"
#
#
#         await bot.edit_message_media(media = types.InputMediaPhoto(InputFile(photo_path), caption = caption_text),
#                                      chat_id = message.from_user.id,
#                                      message_id = message.message_id ,
#                                      reply_markup = Inline_keyboard.product_show)
#     else:
#         caption_text = f"\n{current_image_index + 1}/{len(images)}\nАртикул: {articul}\nК сожалению данный товар закончился"
#
#         await bot.edit_message_media(media = types.InputMediaPhoto(InputFile(photo_path),caption = caption_text),
#                                      chat_id = message.from_user.id,
#                                      message_id = message_id,
#                                      reply_markup = Inline_keyboard.product_show_nol)
#
#
# async def process_callback(bot, callback_query):
#     global amount
#     global current_image_index
#     global cat_name
#     global message_id
#     global all_amount_prod
#     global category_numb
#     global image_direct
#
#     all_amount_prod = 0
#     # global articul
#     # articul = 0
#
#     path_dir = os.path.join(image_direct) # path
#     images = [f for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]
#
#
#
#     if callback_query.data == 'back-enter':
#         # if current_image_index > 0:
#         current_image_index = (current_image_index - 1) % len(images)
#         amount = 1
#         print(current_image_index)
#
#     elif callback_query.data == 'forward-enter':
#         # if current_image_index < len(images) - 1: # что бы списки не прокручивались после того как закончились
#         current_image_index = (current_image_index + 1) % len(images)
#         amount = 1
#         print(current_image_index)
#
#     elif callback_query.data == 'amount_min':
#         if amount > 1:
#             amount -= 1
#
#
#     photo_path = os.path.join(path_dir,images[current_image_index])
#     products_to_choose = images[current_image_index].split('_')[1]
#     category = images[current_image_index].split('_')[2]
#     print(f"Category: {category}")
#     category_numb = category
#     products_number = images[current_image_index].split('.')[0].split('_')[3]
#     articul = f"{products_to_choose}00{category}00{products_number}"
#     if callback_query.data == 'amount_sum':
#         max_amount = data.db.database.get_all_amount(articul)
#         if amount < max_amount[0]:
#             amount += 1
#     if callback_query.data == 'choose_enter':
#         all_amount_prod = data.db.database.get_all_amount(articul)
#         all_amount = all_amount_prod[0]
#         amount_def = all_amount
#         all_amount -= amount
#         data.db.database.update_all_amount(articul,all_amount)
#
#         price = data.db.database.get_price(articul)
#         all_price = 0
#         if amount_def > 0:
#             for pattern, price in grouped_prices.items():
#                 if re.match(pattern,articul):
#                         await corsina.add_to_cart(callback_query.message.chat.id,cat_name,articul,current_image_index + 1,amount,price, category_numb)
#                         all_price += price * amount
#
#             await bot.send_message(callback_query.message.chat.id,
#                                    f"Товар {cat_name}:\n\nАртикул: {articul}\nВыбранный вариант: {current_image_index + 1}\nКоличество: {amount}\nЦена: {all_price}\n\nБыл успешно добавлен в корзину 💵‍",
#                                    reply_markup = Inline_keyboard.show_basket_add)
#
#
#
#     all_amount_prod = data.db.database.get_all_amount(articul)
#     if all_amount_prod[0] > 0:
#         caption_text = f"\n{current_image_index + 1}/{len(images)}\nАртикул: {articul}\nОсталось: {all_amount_prod[0]}\nКол-во: {amount}"
#         await bot.edit_message_media(
#             media=types.InputMediaPhoto(InputFile(photo_path), caption_text),
#             chat_id=callback_query.message.chat.id,
#             message_id=callback_query.message.message_id,
#             reply_markup=Inline_keyboard.product_show)
#     else:
#         caption_text = f"\n{current_image_index + 1}/{len(images)}\nАртикул: {articul}\nК сожалению данный товар закончился😢"
#         await bot.edit_message_media(
#             media = types.InputMediaPhoto(InputFile(photo_path),caption_text),
#             chat_id = callback_query.message.chat.id,
#             message_id = callback_query.message.message_id,
#             reply_markup = Inline_keyboard.product_show_nol)
import io

import gspread
from aiogram.types import InputFile
from aiogram import types
from googleapiclient.http import MediaIoBaseDownload
# import choose_notebook
import config
import corsina
from keyboards.Inline import Inline_keyboard
import hashlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import pprint

async def init_image_caption(worksheet, product_name):
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
                if subcategory[1] == product_name:
                    if int(subcategory[4]) > 0:
                        subcategories.append(subcategory)
            if subcategories:  # Проверяем, что subcategories не пустой
                image_captions.append([category,subcategories])
                continue

    return image_captions


async def send_photo(bot, callback_query, product, db):
    cur_img_ind = 0
    cur_img_cap = 1
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    product_name = user_state['notebook']['product_name']
    # keyboard = Inline_keyboard.create_category_keyboard(cur_img_ind, cur_img_cap, product)

    image_captions = await init_image_caption(product, product_name)

    caption = (f"{image_captions[cur_img_ind][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_ind][1][0][2]}\n"
               f"Кол-во: 1\n"
               f"Общее Кол-во: {image_captions[cur_img_ind][1][0][4]}\n\n"
               f"Вариант: {cur_img_cap}/{len(image_captions)}")

    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_ind, cur_img_cap)

    await bot.send_photo(callback_query.message.chat.id,
                         photo = image_captions[cur_img_ind][1][0][3],
                         caption = caption,
                         reply_markup = keyboard)


#     await install_image(bot, chat_id, more_dir, path_name, more_text, db)
#
#
#
# def calculate_file_hash(file_path):
#     hasher = hashlib.md5()
#     with open(file_path, 'rb') as file:
#         while chunk := file.read(8192):
#             hasher.update(chunk)
#     return hasher.hexdigest()
#
# async def install_image(bot, chat_id, folder_id, path_name, path_text, db):
#
#     SCOPES = ['https://www.googleapis.com/auth/drive']
#     SERVICE_ACCOUNT_FILE = 'disk_autorization.json'
#
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     service = build('drive', 'v3', credentials=credentials)
#
#
#     download_path = f"photo_{path_name}"
#     if not os.path.exists(download_path):
#         os.makedirs(download_path)
#
#     file_list = service.files().list(q=f"'{folder_id}' in parents and trashed=false").execute()
#     pprint.pprint(file_list)
#     for file in file_list.get('files', []):
#         local_file_path = os.path.join(download_path, file['name'])
#
#         if os.path.exists(local_file_path):
#             local_file_hash = calculate_file_hash(local_file_path)
#             drive_file_hash = file.get('md5Checksum')  # используем get, чтобы избежать KeyError
#
#             if drive_file_hash is not None and local_file_hash != drive_file_hash:
#                 # Файлы отличаются, скачиваем новый
#                 request = service.files().get_media(fileId = file['id'])
#                 fh = io.FileIO(local_file_path, mode = 'w')
#                 downloader = MediaIoBaseDownload(fh, request)
#                 done = False
#                 while not done:
#                     _, done = downloader.next_chunk()
#                 print(f'Файл "{file["name"]}" успешно обновлен.')
#             else:
#                 print(f'Файл "{file["name"]}" уже синхронизирован.')
#         else:
#             request = service.files().get_media(fileId = file['id'])
#             fh = io.FileIO(local_file_path, mode = 'w')
#             downloader = MediaIoBaseDownload(fh, request)
#             done = False
#             while not done:
#                 _, done = downloader.next_chunk()
#             print(f'Файл "{file["name"]}" успешно скачан.')
#
#     local_files = os.listdir(download_path)
#     for local_file in local_files:
#         local_file_path = os.path.join(download_path, local_file)
#         drive_file_names = [file['name'] for file in file_list.get('files', [])]
#         if local_file not in drive_file_names:
#             os.remove(local_file_path)
#             print(f'Локальный файл "{local_file}" удален, так как его нет на Google Диске.')
#     await send_photo(bot, chat_id, download_path, path_text, db)
#
#
#
# async def send_photo(bot, chat_id, more_path, more_text, db):
#
#     user_state = await db.State.find_one({'_id': chat_id})
#     price = user_state['notebook']['price']
#
#     path = os.path.join(more_path)
#     await db.State.update_one(dict(
#         _id = chat_id),
#         {
#             "$set": {'notebook.path': path,
#                      'notebook.text': more_text}
#
#         }
#     )
#     images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#     current_image_index = int(user_state['notebook']['more']['cur_img_ind'])
#     current_photo_path = os.path.join(path, images[current_image_index])
#
#     keyboard = Inline_keyboard.create_category_product_ceyboard(current_image_index)
#     len_photo = f"*{current_image_index + 1}/{len(images)}*\nЦена: {price}"
#     await bot.send_photo(chat_id,
#                          InputFile(current_photo_path),
#                          caption = f"{len_photo}\n{more_text}",
#                          reply_markup = keyboard,
#                          parse_mode = 'Markdown')
#
# async def pay_notebook_more(bot, message, db):
#     user_state = await db.State.find_one({'_id': message.from_user.id})
#     cur_img_indx = int(user_state['notebook']['more']['cur_img_ind'])
#     image_captions = await choose_notebook.init_image_caption()
#     current_img = image_captions[cur_img_indx][1][0][0]
#     current_caption = image_captions[cur_img_indx][1][0][1]
#     current_price = image_captions[cur_img_indx][1][0][4]
#     current_link = image_captions[cur_img_indx][1][0][5]
#     caption = f"Вы приобрели {current_caption}\nЗа {current_price}\nвот ваша ссылка: {current_link}"
#     await bot.send_photo(message.from_user.id,
#                          photo = str(current_img),
#                          caption = caption)

async def process_callback(bot, callback_query, cur_img_indx, cur_img_caption, db):
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})

    path_name = user_state['notebook']['path_name']
    # images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # amount = 1
    product_name = user_state['notebook']['product_name']

    image_captions = await init_image_caption(path_name, product_name)


    if callback_query.data.startswith('forward-enter'):
        if cur_img_caption < len(image_captions):  # что бы списки не прокручивались после того как закончились
            cur_img_indx += 1
            cur_img_caption += 1
            await db.State.update_one(dict(
                _id = callback_query.from_user.id),
                {
                    "$set": {'notebook.amount': 1}
                }
            )
        await callback_query.answer()

    if callback_query.data.startswith('back-enter'):
        if cur_img_indx > 0:
            cur_img_indx -= 1
            cur_img_caption -= 1
            await db.State.update_one(dict(
                _id = callback_query.from_user.id),
                {
                    "$set": {'notebook.amount': 1}
                }
            )
        await callback_query.answer()

    if callback_query.data.startswith('amount-sum'):
        max_amount = image_captions[cur_img_indx][1][0][4]
        amount = user_state['notebook']['amount']

        if amount < int(max_amount):
            print(max_amount)
            amount += 1
            await db.State.update_one(dict(
                _id = callback_query.from_user.id),
                {
                    "$set": {'notebook.amount': int(amount)}
                }
            )
        await callback_query.answer()

    if callback_query.data.startswith('amount-min'):
        amount = user_state['notebook']['amount']
        if amount > 1:
            amount -= 1
            await db.State.update_one(dict(
                        _id = callback_query.from_user.id),
                        {
                            "$set": {'notebook.amount': int(amount)}
                        }
                    )
        await callback_query.answer()

    if callback_query.data.startswith('product-choose-enter'):
        amount = int(user_state['notebook']['amount'])
        all_amount = int(image_captions[cur_img_indx][1][0][4])
        all_amount -= amount
        articul = image_captions[cur_img_indx][1][0][0]
        category_numb = int(articul[3:-3])
        price = int(image_captions[cur_img_indx][1][0][2])
        product = user_state['notebook']['path_name']

        image_captions[cur_img_indx][1][0][4] = all_amount

        gc = gspread.service_account(filename = 'shoptg-97da5d92bfcd.json')
        sh = gc.open("ShopTgTable")
        worksheet = sh.worksheet(product)

        cell = worksheet.find(articul)
        print(cell.row, cell.col)
        worksheet.update_cell(cell.row, 5, all_amount)

        all_price = 0

        await corsina.add_to_cart(callback_query.message.chat.id,product_name,articul,cur_img_indx + 1,amount,price, category_numb)
        all_price += price * amount

        await bot.send_message(callback_query.message.chat.id,
                               f"Товар {product_name}:\n\nАртикул: {articul}\nВыбранный вариант: {cur_img_indx + 1}\nКоличество: {amount}\nЦена: {all_price}\n\nБыл успешно добавлен в корзину 💵‍",
                               reply_markup = Inline_keyboard.show_basket_add)




    amount = user_state['notebook']['amount']
    caption = (f"{image_captions[cur_img_indx][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_indx][1][0][2]}\n"
               f"Кол-во: {amount}\n"
               f"Общее Кол-во: {image_captions[cur_img_indx][1][0][4]}\n\n"
               f"Вариант: {cur_img_caption}/{len(image_captions)}")
    media = image_captions[cur_img_indx][1][0][3]
    # photo_path = os.path.join(path, images[list_img_ind])
    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_indx, cur_img_caption)

    await bot.edit_message_media(
        media = types.InputMediaPhoto(media,caption = caption),
        chat_id = callback_query.message.chat.id,
        message_id = callback_query.message.message_id,
        reply_markup = keyboard)