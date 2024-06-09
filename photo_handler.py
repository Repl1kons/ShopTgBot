import gspread
from aiogram import types
import more_category
import photo_hendler_two
from keyboards.Inline import Inline_keyboard
from aiocache import cached


@cached()
async def init_image_caption(worksheet):
    image_captions = []
    gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
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


async def send_photo(bot, callback_query: types.CallbackQuery, product):
    cur_img_ind = 0
    cur_img_cap = 1

    keyboard = Inline_keyboard.create_category_keyboard(cur_img_ind, cur_img_cap, product)

    image_captions = await init_image_caption(product)
    print(image_captions[cur_img_ind][1][0][0])

    caption = f"{image_captions[cur_img_ind][1][0][1]}\nЦена: {image_captions[cur_img_ind][1][0][4]}\nВариант: {cur_img_cap} из {len(image_captions)}"
    media = image_captions[cur_img_ind][1][0][0]

    await callback_query.message.edit_media(media = types.InputMediaPhoto(media,caption = caption),
                                            reply_markup = keyboard)

async def process_callback(bot, callback_query, cur_img_indx, cur_img_caption, product, db):
    image_captions = await init_image_caption(product)
    #
    # if callback_query.data.startswith('back_to_choose'):
    #
    #     await callback_query.answer()

    if callback_query.data.startswith('categoryBack'):
        if cur_img_indx > 0:
            cur_img_indx -= 1
            cur_img_caption -= 1
        else:
            return
        await callback_query.answer()
    elif callback_query.data.startswith('categoryForward'):
        if cur_img_caption < len(image_captions):
            cur_img_indx += 1
            cur_img_caption += 1

        else:
            return
        await callback_query.answer()


    elif callback_query.data.startswith('choose-enter-categorical'):
        product_object = product.replace("category", '').lower()

        product_name = image_captions[cur_img_indx][1][0][1]
        path_name = f"{product_object}"
        await db.State.update_one(dict(
            _id = callback_query.from_user.id),
            {
                "$set": {'notebook.path_name': path_name,
                         'notebook.product_name': product_name,
                         'notebook.amount': 1}
            }
        )
        await photo_hendler_two.send_photo(bot, callback_query, product_object, db)
        await callback_query.answer()
        return


    elif callback_query.data.startswith('categoryMore'):
        product_object = product.replace("category",'').lower()
        path_more = image_captions[cur_img_indx][1][0][2]
        current_price = int(image_captions[cur_img_indx][1][0][4])
        product_name = image_captions[cur_img_indx][1][0][1]
        path_name = f"{product_object}"
        more_text = image_captions[cur_img_indx][1][0][3]
        await db.State.update_one(dict(
            _id = callback_query.from_user.id),
            {
                "$set": {'notebook.path_name': path_name,
                         'notebook.more.cur_img_ind': cur_img_indx,
                         'notebook.product_name': product_name,
                         'notebook.price': current_price,
                         'notebook.path_more': path_more}
            }
        )
        await more_category.start_send_photo_more(bot, callback_query,
                                                  more_text, db)
        await callback_query.answer()
        return

    media = image_captions[cur_img_indx][1][0][0]
    caption = f"{image_captions[cur_img_indx][1][0][1]}\nЦена: {image_captions[cur_img_indx][1][0][4]}\nВариант: {cur_img_caption} из {len(image_captions)}"
    keyboard = Inline_keyboard.create_category_keyboard(cur_img_indx, cur_img_caption, product)

    await callback_query.message.edit_media(media=types.InputMediaPhoto(media, caption=caption),
                                            reply_markup = keyboard)

    # await callback_query.message.edit_message_media(
    #     media = types.InputMediaPhoto(media,caption = caption),
    #     chat_id = callback_query.message.chat.id,
    #     message_id = callback_query.message.message_id,
    #     reply_markup = keyboard)