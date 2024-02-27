import gspread
from aiogram import types
import photo_handler
from keyboards.Inline import Inline_keyboard


async def init_image_caption(worksheet,product_name):
    image_captions = []

    gc = gspread.service_account(filename = 'shoptg-97da5d92bfcd.json')
    sh = gc.open("ShopTgTable")
    worksheet = sh.worksheet(worksheet)
    for index,row in enumerate(worksheet.get_all_values()):
        if index == 0:
            continue  # Пропускаем 1 строку
        if row:
            category = row[0]
            subcategories = []
            for i in range(0,len(row),5):
                subcategory = [row[i],row[i + 1],row[i + 2],row[i + 3],row[i + 4]]
                if subcategory[1] == product_name:
                    if int(subcategory[4]) > 0:
                        subcategories.append(subcategory)
            if subcategories:  # Проверяем, что subcategories не пустой
                image_captions.append([category,subcategories])
                continue

    return image_captions


async def send_photo(bot,callback_query,product,db):
    cur_img_ind = 0
    cur_img_cap = 1
    user_state = await db.State.find_one({'_id': callback_query.from_user.id})
    product_name = user_state['notebook']['product_name']
    print(f"Product: {product}, pr_name: {product_name}")
    image_captions = await init_image_caption(product,product_name)
    await db.State.update_one(dict(
        _id = callback_query.from_user.id),
        {
            "$set": {'notebook.amount': 1}
        }
    )
    amount = user_state['notebook']['amount']

    caption = (f"{image_captions[cur_img_ind][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_ind][1][0][2]}\n"
               f"Кол-во: {amount}\n"
               f"Общее Кол-во: {image_captions[cur_img_ind][1][0][4]}\n\n"
               f"Вариант: {cur_img_cap}/{len(image_captions)}")

    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_ind,cur_img_cap)

    await bot.send_photo(callback_query.message.chat.id,
                         photo = image_captions[cur_img_ind][1][0][3],
                         caption = caption,
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

        await bot.delete_message(chat_id = callback_query.message.chat.id,
                                 message_id = callback_query.message.message_id)
        await photo_handler.send_photo(bot,callback_query.from_user.id,path_name_2)

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

        await bot.send_message(callback_query.message.chat.id,
                               f"Товар {product_name}:\n\nАртикул: {articul}\nВыбранный вариант: {cur_img_indx + 1}\nКоличество: {amount}\nЦена: {all_price}\n\nБыл успешно добавлен в корзину 💵‍",
                               reply_markup = Inline_keyboard.show_basket_add)
    # amount = user_state['notebook']['amount']

    caption = (f"{image_captions[cur_img_indx][1][0][1]}\n"
               f"Цена: {image_captions[cur_img_indx][1][0][2]}\n"
               f"Кол-во: {amount}\n"
               f"Общее Кол-во: {image_captions[cur_img_indx][1][0][4]}\n\n"
               f"Вариант: {cur_img_caption}/{len(image_captions)}")
    media = image_captions[cur_img_indx][1][0][3]

    keyboard = Inline_keyboard.create_category_product_keyboard(cur_img_indx,cur_img_caption)

    await bot.edit_message_media(
        media = types.InputMediaPhoto(media,caption = caption),
        chat_id = callback_query.message.chat.id,
        message_id = callback_query.message.message_id,
        reply_markup = keyboard)
