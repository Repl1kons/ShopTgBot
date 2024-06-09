from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import gspread
from keyboards.Inline import Inline_keyboard
import sqlite3

async def create_cart_keyboard(user_id, db):
    user_corsina = await db.Corsina.find_one({'_id': user_id})
    user_corsina_data = user_corsina['data']

    if user_corsina_data:
        keyboard = InlineKeyboardMarkup(row_width=3)
        for order in user_corsina_data:

            all_amount = order['max_amount']
            print(f"Всего: {all_amount}")
            # for item_id, item_name, quantity, articul in cart_items:
            print(order)
            item_id = order['id']
            keyboard.insert(InlineKeyboardButton(text=f"{order['product_name']} | {order['articul']} | {order['quantity']} шт.", callback_data=f'corzina_{item_id}'))

            keyboard.add(
                InlineKeyboardButton(text="- 1", callback_data=f"corzinaEditMin_{item_id}"),
                InlineKeyboardButton(text="Удалить", callback_data=f"corzinaEditDel_{item_id}"),
                InlineKeyboardButton(text = "+ 1",callback_data = f"corzinaEditSum_{item_id}"))
        keyboard.add(InlineKeyboardButton(text = "Назад", callback_data = "show_basket"))
        return keyboard

async def create_cart_edit_message(user_id, db):
    user_corsina = await db.Corsina.find_one({'_id': user_id})
    user_corsina_data = user_corsina['data']

    welcome_message = '● Товары:'
    total_price = 0
    item_number = 1

    if user_corsina_data:
        for order in user_corsina_data:
            amount_price = order['quantity'] * order['price']
            total_price += amount_price
            welcome_message += f"\n\n*{order['product_name']}*\n ┄ Артикул: {order['articul']}\n ┄ Вариант: {order['selected_variant']}\n{order['quantity']} шт. x {int(order['price'])} ₽ = {int(amount_price)} ₽\n———"
            item_number += 1

        # welcome_message += "● Итого: "

        return welcome_message

    else:

        welcome_message = f"Корзина пуста"

        return welcome_message

async def add_to_cart(user_id, item_name, articul, selected_variant, quantity, price, selected_category):
    conn = sqlite3.connect('data/user_corsina.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # SQL-команда для добавления товара в корзину
    cursor.execute("""
        INSERT INTO cart_items (user_id, item_name, articul, selected_variant, quantity, price, selected_category) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, item_name, articul, selected_variant, quantity, price, selected_category))

    conn.commit()
    conn.close()



async def show_cart(bot, message: types.Message, db):
    user_id = message.from_user.id

    user_corsina = await db.Corsina.find_one({'_id': user_id})
    user_corsina_data = user_corsina['data']
    if user_corsina_data:
        # user_corsina_data = user_corsina['data']
        # Здесь остальной код, использующий user_corsina_data

        cart_contents = '● Товары:\n'
        total_price = 0
        item_number = 0
        all_order_price = 0

        total_amount_price = 0

        for order in user_corsina_data:
            order_price = int(order['price'])
            order_quantity = int(order['quantity'])
            order_amount_price = order_price * order_quantity
            total_amount_price += order_amount_price

            total_price += order_amount_price
            cart_contents += (f"\n*{order['product_name']}*\n "
                              f"┄_Артикул:_ {order['articul']}\n "
                              f"┄_Вариант:_ {order['selected_variant']}\n"
                              f"{order['quantity']} шт. x {order['price']} ₽\n"
                              f"Сумма: {order['quantity'] * order['price']} ₽\n"
                              f"----------\n")

            item_number += order['quantity']

        cart_contents += f'\n● Итого:\n ┄ {item_number} шт. товаров на {total_price} ₽\n ┄ Доставка: 300 ₽\n\n'
        print(all_order_price)
        cart_contents += f"*Всего к оплате: {int(total_price + 300)} руб.*"
        await bot.send_message(user_id, f"{cart_contents}", reply_markup=Inline_keyboard.keyboard_basket, parse_mode='Markdown')
    else:
        await bot.send_message(user_id, "👻 Ваша корзина пуста 😢")



async def edit_cart(bot, message: types.Message, db):
    user_corsina = await db.Corsina.find_one({'_id': message.from_user.id})
    user_corsina_data = user_corsina['data']

    keyboard = await create_cart_keyboard(message.from_user.id, db)

    if user_corsina_data:
        welcome_message = await create_cart_edit_message(message.from_user.id, db)

        await bot.send_message(message.from_user.id, welcome_message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        await bot.send_message(message.from_user.id, "Ваша корзина пуста")

async def edit_cart_Delete(bot, callback_query: types.CallbackQuery, corzinaEdit, db):

    user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
    user_corsina_data = user_corsina['data']

    if user_corsina_data:
        for order in user_corsina_data:
            now_amount = int(order['quantity'])
            max_amount = int(order['max_amount'])
            worksheet = order['worksheet']
            articul = order['articul']
            new_all_amount = max_amount + now_amount

            if int(order['id']) == int(corzinaEdit):
                gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
                sh = gc.open("ShopTgTable")
                worksheet = sh.worksheet(worksheet)
                cell = worksheet.find(articul)
                print(cell.row,cell.col)
                worksheet.update_cell(cell.row, 5, new_all_amount)

                await db.Corsina.update_one(
                    {'_id': callback_query.from_user.id},
                    {'$pull': {'data': {'id': int(corzinaEdit)}}}
                )
        new_keyboard = await create_cart_keyboard(callback_query.from_user.id, db)
        welcome_message = await create_cart_edit_message(callback_query.from_user.id, db)

            # welcome_message += '———\n'
        await callback_query.message.edit_text(text=welcome_message, reply_markup=new_keyboard, parse_mode='Markdown')
        if not user_corsina_data:
            welcome_message = "Ваша корзина теперь пуста"
            await callback_query.message.edit_text(text=welcome_message, reply_markup=new_keyboard, parse_mode='Markdown')


    else:
        welcome_message = "Ваша корзина теперь пуста"
        await callback_query.message.edit_text(text=welcome_message, reply_markup=new_keyboard, parse_mode='Markdown')



async def edit_cart_amount_Sum(bot, callback_query: types.CallbackQuery, corzinaEdit, db):
    user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
    user_corsina_data = user_corsina['data']
    if user_corsina_data:
        for order in user_corsina_data:
            now_amount = int(order['quantity'])
            max_amount = int(order['max_amount'])
            worksheet = order['worksheet']
            articul = order['articul']
            if now_amount < max_amount:
                new_amount = now_amount + 1
                tabel_new_amount = max_amount - 1
                if int(order['id']) == int(corzinaEdit):
                    gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
                    sh = gc.open("ShopTgTable")
                    worksheet = sh.worksheet(worksheet)
                    cell = worksheet.find(articul)
                    print(cell.row,cell.col)
                    worksheet.update_cell(cell.row,5, tabel_new_amount)

                    await db.Corsina.update_one(
                        {'_id': callback_query.from_user.id},
                        {'$set': {'data.$[elem].quantity': new_amount,
                                  'data.$[elem].max_amount': tabel_new_amount}},
                        array_filters = [{'elem.id': int(corzinaEdit)}]
                    )


        # После обновления заказа создаем новое сообщение о корзине и обновляем клавиатуру
        welcome_message = await create_cart_edit_message(callback_query.from_user.id,db)
        new_keyboard = await create_cart_keyboard(callback_query.from_user.id,db)
        await callback_query.message.edit_text(text = welcome_message,
                                               reply_markup = new_keyboard,
                                               parse_mode = 'Markdown')


async def edit_cart_amount_Min(bot, callback_query: types.CallbackQuery, corzinaEdit, db):
    user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
    user_corsina_data = user_corsina['data']
    if user_corsina_data:
        for order in user_corsina_data:
            now_amount = int(order['quantity'])
            max_amount = int(order['max_amount'])
            worksheet = order['worksheet']
            articul = order['articul']
            if now_amount < max_amount:
                new_amount = now_amount - 1
                tabel_new_amount = max_amount + 1
                if int(order['id']) == int(corzinaEdit):
                    gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
                    sh = gc.open("ShopTgTable")
                    worksheet = sh.worksheet(worksheet)
                    cell = worksheet.find(articul)
                    print(cell.row,cell.col)
                    worksheet.update_cell(cell.row,5,tabel_new_amount)

                    await db.Corsina.update_one(
                        {'_id': callback_query.from_user.id},
                        {'$set': {'data.$[elem].quantity': new_amount,
                                  'data.$[elem].max_amount': tabel_new_amount}},
                        array_filters = [{'elem.id': int(corzinaEdit)}]
                    )

        welcome_message = await create_cart_edit_message(callback_query.from_user.id,db)
        new_keyboard = await create_cart_keyboard(callback_query.from_user.id,db)
        await callback_query.message.edit_text(text = welcome_message,
                                               reply_markup = new_keyboard,
                                               parse_mode = 'Markdown')

async def process_callback(bot, callback_query: types.CallbackQuery, db):
    user_id = callback_query.from_user.id

    if callback_query.data == 'edit_cart':
        await edit_cart(bot, callback_query, db)

    elif callback_query.data == 'show_basket':
        await show_cart(bot, callback_query, db)

    elif callback_query.data == 'clear_cart':
        user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
        user_corsina_data = user_corsina['data']

        if user_corsina_data:
            for order in user_corsina_data:
                now_amount = int(order['quantity'])
                max_amount = int(order['max_amount'])
                worksheet = order['worksheet']
                articul = order['articul']

                new_amount = now_amount - 1
                tabel_new_amount = max_amount + 1

                gc = gspread.service_account(filename = 'data/json/shoptg-97da5d92bfcd.json')
                sh = gc.open("ShopTgTable")
                worksheet = sh.worksheet(worksheet)
                cell = worksheet.find(articul)
                print(cell.row,cell.col)
                worksheet.update_cell(cell.row,5,tabel_new_amount)

                await db.Corsina.update_one(
                    {'_id': callback_query.from_user.id},
                    {'$set': {'data': []}}
                )
        await callback_query.message.edit_text(text = "👻 Ваша корзина теперь пуста 😢")

