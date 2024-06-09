import gspread
from aiogram import types
import photo_handler
from keyboards.Inline import Inline_keyboard
from aiocache import cached
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import time


@cached()
async def init_image_caption(worksheet, product_name):
    image_captions = []

    gc = gspread.service_account(filename= 'data/json/shoptg-97da5d92bfcd.json')
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
                image_captions.append([category, subcategories])
                continue

    return image_captions


async def create_product_image(callback_query, product_name, article, quantity, price, current_var, choose_product_url, output_path, ava):
    # Запускаем счетчик времени
    start_time = time.time()

    product_image = Image.open("data/img/object.jpg")
    # product_image.

    choose_product_response = requests.get(choose_product_url)
    choose_product_image = Image.open(io.BytesIO(choose_product_response.content))

    width = 100
    height = 100
    card = Image.new("RGB",(width,height),"#EEC3EE")

    # Получаем изображение аватара пользователя
    ava_image = Image.open(ava)
    ava_width = 50  # Выберите подходящую ширину
    ava_height = 50  # Выберите подходящую высоту
    ava_resized = ava_image.resize((ava_width,ava_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_1 = Image.new("L",ava_resized.size,0)
    draw = ImageDraw.Draw(mask_1)
    draw.ellipse((0,0,ava_width,ava_height),fill = 255)
    position = (690,90)

    """ПОКАЗ УСПЕШНОЙ ОПЛАТЫ"""
    success_image = Image.open("data/img/object.jpg")
    success_width = 350  # Выберите подходящую ширину
    success_height = 60  # Выберите подходящую высоту
    success_resized = success_image.resize((success_width,success_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_success = Image.new("L",success_resized.size,0)
    draw_success = ImageDraw.Draw(mask_success)
    radius = min(ava_width,ava_height) // 2  # Радиус закругления, равный половине минимальной стороны изображения
    draw_success.rounded_rectangle((0, 0, success_width, success_height), radius, fill=255)
    position_success = (365, 520)


    """БЛОКИ ДЛЯ ХАР-ИК ТОВАРОВ"""
    block_image = Image.open("data/img/object.jpg")
    block_width = 150  # Выберите подходящую длину
    block_height = 70  # Выберите подходящую шир
    block_resized = block_image.resize((block_width,block_height),Image.LANCZOS)

    # Создаем маску для круглой формы
    mask_block = Image.new("L",block_resized.size,0)
    draw_block = ImageDraw.Draw(mask_block)
    radius = min(block_width,block_height) // 2  # Радиус закругления, равный половине минимальной стороны изображения
    draw_block.rounded_rectangle((0,0,block_width,block_height),radius,fill = 255)
    position_block_amount = (365,420)
    position_block_price = (565,420)



    image = product_image.copy()
    draw = ImageDraw.Draw(image)
    font_size = 22
    font = ImageFont.truetype("data/font/sfns-display-bold.ttf", font_size)


    """ БЕЛАЯ КАРТОЧКА"""
    new_width = 450
    new_height = 530
    card_resized = card.resize((new_width, new_height), Image.LANCZOS)

    mask_card = Image.new("L",card_resized.size,0)
    draw_mask = ImageDraw.Draw(mask_card)
    radius = 20
    draw_mask.rounded_rectangle((0,0,new_width,new_height),radius,fill = 255)

    # Вставляем изображение товара на основное изображение с закругленными углами
    image.paste(card_resized,(315,product_image.height-600),mask = mask_card)


    """ ФОТО ЕЖЕДНЕВНИКА """
    new_width = 200
    new_height = 200
    choose_product_resized = choose_product_image.resize((new_width, new_height), Image.LANCZOS)

    # Создаем маску для скругления углов
    mask = Image.new("L", choose_product_resized.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    radius = 20
    draw_mask.rounded_rectangle((0, 0, new_width, new_height), radius, fill=255)

    # Вставляем изображение товара на основное изображение с закругленными углами
    image.paste(choose_product_resized, (440, card_resized.height - 400), mask=mask)

    image.paste(ava_resized,position,mask = mask_1)
    image.paste(success_resized,position_success,mask = mask_success)



    text_name = f"{product_name}\n"
    text_position_name = (435, card_resized.height - 190)
    draw.text(text_position_name,text_name,fill = "#6A6A6A",font = font)



    text_success = "Успешно добавлено в корзину"
    text_position_success = (375, 535)
    draw.text(text_position_success,text_success,fill = "#6D6C64",font = font)



    image.paste(block_resized, position_block_amount,mask = mask_block)
    text_block_amount = f"Кол-во: {quantity}"
    text_position_block_amount = (390,440)
    draw.text(text_position_block_amount,text_block_amount,fill = "#4B4B4B",font = font)




    image.paste(block_resized,position_block_price,mask = mask_block)
    text_block_price = f"Цена: {price}"
    text_position_block_price = (590,440)
    draw.text(text_position_block_price,text_block_price,fill = "#4B4B4B",font = font)



    image.save(output_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"sdsadsads {execution_time}")
    caption = f"Товар {product_name}:\n\nАртикул: {article}\nВыбранный вариант: {current_var}\nКоличество: {quantity}\nЦена: {price}\n\nБыл успешно добавлен в корзину 💵‍"
        #                        reply_markup = Inline_keyboard.show_basket_add)
    await callback_query.message.edit_media(media = types.InputMediaPhoto(types.InputFile(output_path), caption=caption),
                                            reply_markup = Inline_keyboard.show_basket_add)


async def send_photo(bot,callback_query,product, db):
    cur_img_ind = 0
    cur_img_cap = 1
    amount = 1
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    product_name = user_state['notebook']['product_name']
    print(f"Product: {product}, pr_name: {product_name}")
    image_captions = await init_image_caption(product,product_name)
    await db.State.update_one(dict(
        _id = callback_query.from_user.id),
        {
            "$set": {'notebook.amount': amount}
        }
    )
    amount = user_state['notebook']['amount']

    caption = (f"{image_captions[cur_img_ind][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_ind][1][0][2]}\n"
               f"Кол-во: {amount}\n"
               f"Общее Кол-во: {image_captions[cur_img_ind][1][0][4]}\n\n"
               f"Вариант: {cur_img_cap}/{len(image_captions)}")

    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_ind,cur_img_cap)
    media = image_captions[cur_img_ind][1][0][3]
    # await callback_query.message.edit_media(
    #                      photo = ,
    #                      caption = caption,
    #                      reply_markup = keyboard)

    await callback_query.message.edit_media(media = types.InputMediaPhoto(media,caption = caption),
                                            reply_markup = keyboard)


async def process_callback(bot,callback_query,cur_img_indx,cur_img_caption,db):
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})

    path_name = user_state['notebook']['path_name']

    product_name = user_state['notebook']['product_name']

    amount = user_state['notebook']['amount']

    image_captions = await init_image_caption(path_name,product_name)

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

    if callback_query.data.startswith('back-to-choose'):
        path_name = user_state['notebook']['path_name']
        path_name_2 = "category" + path_name.capitalize()
        #
        # await bot.delete_message(chat_id = callback_query.message.chat.id,
        #                          message_id = callback_query.message.message_id)
        await photo_handler.send_photo(bot, callback_query, path_name_2)
        await callback_query.answer()

        return


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
        else:
            return

        await callback_query.answer()

    if callback_query.data.startswith('amount-sum'):
        amount = user_state['notebook']['amount']
        max_amount = image_captions[cur_img_indx][1][0][4]
        if amount < int(max_amount):
            amount += 1
            await db.State.update_one(dict(
                _id = callback_query.from_user.id),
                {
                    "$set": {'notebook.amount': int(amount)}
                }
            )
        else:
            return

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
        else:
            return

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

        gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
        sh = gc.open("ShopTgTable")
        worksheet = sh.worksheet(product)

        cell = worksheet.find(articul)
        print(cell.row,cell.col)
        worksheet.update_cell(cell.row,5,all_amount)

        all_price = 0

        last_order = await db.Corsina.find_one({'_id': callback_query.from_user.id},{'data': {'$slice': -1}})

        # Получаем последний ID заказа
        last_order_id = last_order['data'][0]['id'] if last_order and 'data' in last_order and last_order['data'] else 0

        # Увеличиваем ID на 1 для нового заказа
        new_order_id = last_order_id + 1

        await db.Corsina.update_one(
            {'_id': callback_query.from_user.id},
            {
                '$push': {
                    'data': {
                        'id': new_order_id,
                        'product_name': product_name,
                        'articul': articul,
                        'selected_variant': cur_img_indx + 1,
                        'quantity': amount,
                        'price': price,
                        'selected_category': category_numb,
                        'max_amount': all_amount,
                        'worksheet': product,
                    }
                }
            }
        )

        all_price += price * amount
        user_profile_photos = await bot.get_user_profile_photos(user_id = callback_query.from_user.id,limit = 1)

        # Проверяем, есть ли у пользователя фотографии профиля
        if user_profile_photos.total_count > 0:
            # Получаем информацию о последней фотографии профиля пользователя
            photo = user_profile_photos.photos[0][-1]
            # Получаем файл фотографии
            photo_file = await bot.get_file(photo.file_id)
            # Возвращаем URL файла фотографии
            await photo_file.download("data/img/ava.png")

        await create_product_image(callback_query,product_name,articul,amount,price,cur_img_indx + 1,image_captions[cur_img_indx][1][0][3],
                                   "data/img/output_image.jpg","data/img/ava.png")
        # await bot.send_message(callback_query.message.chat.id,
        #                        f"Товар {product_name}:\n\nАртикул: {articul}\nВыбранный вариант: {cur_img_indx + 1}\nКоличество: {amount}\nЦена: {all_price}\n\nБыл успешно добавлен в корзину 💵‍",
        #                        reply_markup = Inline_keyboard.show_basket_add)
        return
    # amount = user_state['notebook']['amount']
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    amount = user_state['notebook']['amount']

    caption = (f"{image_captions[cur_img_indx][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_indx][1][0][2]}\n"
               f"Кол-во: {amount}\n"
               f"Общее Кол-во: {image_captions[cur_img_indx][1][0][4]}\n\n"
               f"Вариант: {cur_img_caption}/{len(image_captions)}")
    media = image_captions[cur_img_indx][1][0][3]

    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_indx,cur_img_caption)

    # await bot.edit_message_media(
    #     media = types.InputMediaPhoto(media,caption = caption),
    #     chat_id = callback_query.message.chat.id,
    #     message_id = callback_query.message.message_id,
    #     reply_markup = keyboard)

    await callback_query.message.edit_media(media = types.InputMediaPhoto(media,caption = caption),
                                            reply_markup = keyboard)
