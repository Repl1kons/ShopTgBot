import io
from aiogram.types import InputFile
from aiogram import types
from googleapiclient.http import MediaIoBaseDownload

import photo_handler
import photo_hendler_two
from keyboards.Inline import Inline_keyboard
import hashlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import pprint


async def start_send_photo_more(bot, callback_query, more_text, db):
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    more_dir = user_state['notebook']['path_more']
    path_name = user_state['notebook']['path_name']
    product_name = user_state['notebook']['product_name']

    download_path = f"data/photo/{product_name}/{path_name}"
    if not os.path.exists(download_path):
        await install_image(bot, callback_query, more_dir, path_name, product_name, more_text, db)
    else:
        await send_photo(bot,callback_query,download_path,more_text,db)



def calculate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

async def install_image(bot, callback_query, folder_id, path_name, product_name, path_text, db):

    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'data/json/disk_autorization.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)


    download_path = f"data/photo/{product_name}/{path_name}"
    if not os.path.exists(download_path):
        os.makedirs(download_path)


    file_list = service.files().list(q=f"'{folder_id}' in parents and trashed=false").execute()
    pprint.pprint(file_list)
    for file in file_list.get('files', []):
        local_file_path = os.path.join(download_path, file['name'])

        if os.path.exists(local_file_path):
            local_file_hash = calculate_file_hash(local_file_path)
            drive_file_hash = file.get('md5Checksum')  # используем get, чтобы избежать KeyError

            if drive_file_hash is not None and local_file_hash != drive_file_hash:
                # Файлы отличаются, скачиваем новый
                request = service.files().get_media(fileId = file['id'])
                fh = io.FileIO(local_file_path, mode = 'w')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                print(f'Файл "{file["name"]}" успешно обновлен.')
            else:
                print(f'Файл "{file["name"]}" уже синхронизирован.')
        else:
            request = service.files().get_media(fileId = file['id'])
            fh = io.FileIO(local_file_path, mode = 'w')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            print(f'Файл "{file["name"]}" успешно скачан.')

    local_files = os.listdir(download_path)
    for local_file in local_files:
        local_file_path = os.path.join(download_path, local_file)
        drive_file_names = [file['name'] for file in file_list.get('files', [])]
        if local_file not in drive_file_names:
            os.remove(local_file_path)
            print(f'Локальный файл "{local_file}" удален, так как его нет на Google Диске.')
    await send_photo(bot, callback_query, download_path, path_text, db)



async def send_photo(bot, callback_query, more_path, more_text, db):
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    price = user_state['notebook']['price']

    path = os.path.join(more_path)
    await db.State.update_one(dict(
        _id = callback_query.from_user.id),
        {
            "$set": {'notebook.path': path,
                     'notebook.text': more_text}

        }
    )
    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    list_img_ind = 0
    current_photo_path = os.path.join(path, images[list_img_ind])

    keyboard = Inline_keyboard.create_more_cat(list_img_ind)
    len_photo = f"*{list_img_ind + 1}/{len(images)}*\nЦена: {price}"
    # await callback_query.message.edit_media(media = InputFile(current_photo_path),
    #                                          caption = f"{len_photo}\n{more_text}",
    #                                          reply_markup=keyboard,
    #                                          parse_mode = 'Markdown')

    await callback_query.message.edit_media(media = types.InputMediaPhoto(InputFile(current_photo_path),
                                            caption = f"{len_photo}\n{more_text}",
                                            parse_mode = 'Markdown'),
                                            reply_markup = keyboard)

async def process_callback(bot, callback_query, current_image_index, db):
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    # current_image_index = 0
    path = user_state['notebook']['path']


    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    text = user_state['notebook']['text']
    price = int(user_state['notebook']['price'])

    if callback_query.data.startswith('more_back_return'):
        path_name = user_state['notebook']['path_name']
        path_name_2 = "category" + path_name.capitalize()

        # await bot.delete_message(chat_id = callback_query.message.chat.id,message_id = callback_query.message.message_id)
        await photo_handler.send_photo(bot,callback_query, path_name_2)
        return
    if callback_query.data.startswith('move_more_forward'):
        current_image_index = (current_image_index + 1) % len(images)
        print(current_image_index)
        await callback_query.answer()

    if callback_query.data.startswith('move_more_back'):
        current_image_index = (current_image_index - 1) % len(images)
        print(current_image_index)
        await callback_query.answer()

    if callback_query.data.startswith('choose_enter_categorical'):
        worksheet = user_state['notebook']['path_name']
        # await bot.delete_message(chat_id = callback_query.message.chat.id,message_id = callback_query.message.message_id)
        await photo_hendler_two.send_photo(bot, callback_query, worksheet, db)
        return
    photo_path = os.path.join(path,images[current_image_index])
    keyboard = Inline_keyboard.create_more_cat(current_image_index)
    len_photo = f"*{current_image_index + 1}/{len(images)}*\n" \
                f"Цена: {price}"

    # await bot.edit_message_media(
    #     media = types.InputMediaPhoto(InputFile(photo_path),caption = f"{len_photo}\n{text}",parse_mode = 'Markdown'),
    #     chat_id = callback_query.message.chat.id,
    #     message_id = callback_query.message.message_id,
    #     reply_markup = keyboard)

    await callback_query.message.edit_media(media = types.InputMediaPhoto(InputFile(photo_path),
                                            caption = f"{len_photo}\n{text}",
                                            parse_mode = 'Markdown'),
                                            reply_markup = keyboard)
