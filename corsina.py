from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

import data.db.database
from data.db import database
from keyboards.Inline import Inline_keyboard
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

def create_cart_keyboard(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, quantity, articul FROM cart_items WHERE user_id = ?", (user_id,))
    cart_items = cursor.fetchall()
    conn.close()
    if cart_items:
        keyboard = InlineKeyboardMarkup(row_width=3)
        all_amount = database.get_all_amount(cart_items[0][3])
        print(f"Всего: {all_amount}")
        for item_id, item_name, quantity, articul in cart_items:

            keyboard.insert(InlineKeyboardButton(text=f"{item_name} | {articul} | {quantity} шт.", callback_data=f'corzina_{item_id}'))

            keyboard.add(
                InlineKeyboardButton(text="- 1", callback_data=f"corzinaEditMin_{item_id}"),
                InlineKeyboardButton(text="Удалить", callback_data=f"corzinaEditDel_{item_id}"),
                InlineKeyboardButton(text = "+ 1",callback_data = f"corzinaEditSum_{item_id}"))
        keyboard.add(InlineKeyboardButton(text = "Назад", callback_data = "show_basket"))
        return keyboard

def create_cart_edit_message(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    welcome_message = '● Товары:'
    total_price = 0
    item_number = 1

    query = "SELECT id, item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?"
    cursor.execute(query,(user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    if cart_items:
        for item in cart_items:
            amount_price = item[4] * item[5]
            total_price += amount_price
            welcome_message += f"\n\n*{item[1]}*\n ┄ Артикул: {item[2]}\n ┄ Вариант: {item[3]}\n{item[4]} шт. x {int(item[5])} ₽ = {int(amount_price)} ₽\n———"
            item_number += 1

        # welcome_message += "● Итого: "

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



async def show_cart(bot, message: types.Message):

    user_id = message.from_user.id
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    cart_contents = '● Товары:\n'
    total_price = 0
    item_number = 1
    all_order_price = 0
    all_quantity = 0

    for item in cart_items:
        amount_price = item[3] * item[4]
        total_price += amount_price
        cart_contents += f"\n*{item[0]}*\n _┄ Артикул:_ {item[1]}\n ┄ _Вариант:_ {item[2]}\n" \
                         f"{item[3]} шт. x {int(item[4])} ₽ = {int(amount_price)}" \
                         f" ₽\n———\n"
        item_number += 1
        all_quantity += item[3]
    all_order_price += total_price
    cart_contents += f'\n● Итого:\n ┄ {all_quantity} шт. товаров на {int(all_order_price)} ₽\n ┄ Доставка: 300 ₽\n\n'
    print(all_order_price)
    global message_id
    if cart_items:
        cart_contents += f"*Всего к оплате: {int(total_price + 300)} руб.*"
        message_id = (await bot.send_message(user_id, f"{cart_contents}", reply_markup=Inline_keyboard.keyboard_basket, parse_mode='Markdown')).message_id
    else:
        message_id = (await bot.send_message(user_id, "👻 Ваша корзина пуста 😢")).message_id



async def edit_cart(bot, message: types.Message):
    keyboard = create_cart_keyboard(message.from_user.id)
    current_order_number = None
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    query = "SELECT id, item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?"
    cursor.execute(query,(message.from_user.id,))
    cart_items = cursor.fetchall()
    conn.close()

    if cart_items:
        welcome_message = create_cart_edit_message(message.from_user.id)

        global message_id
        message_id = (await bot.send_message(message.from_user.id, welcome_message, reply_markup=keyboard, parse_mode='Markdown')).message_id
    else:
        await bot.send_message(message.from_user.id, "Ваша корзина пуста")

async def edit_cart_Delete(bot, callback_query: types.CallbackQuery, corzinaEdit):
    global message_id


    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    # Получение товара по номеру
    cursor.execute("SELECT quantity, articul, item_name, selected_variant, price FROM cart_items WHERE id = ?",(corzinaEdit,))
    rows = cursor.fetchall()

    show_catalogs = InlineKeyboardMarkup(row_width=3)
    if rows:

        now_all_amount = database.get_all_amount(rows[0][1])
        new_all_amount = now_all_amount[0] + rows[0][0]
        print(new_all_amount)
        database.update_all_amount(rows[0][1], new_all_amount)
        database.delete_order_corsina(corzinaEdit)
        new_keyboard = create_cart_keyboard(callback_query.from_user.id)
        welcome_message = create_cart_edit_message(callback_query.from_user.id)

        # welcome_message += '———\n'
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, text=welcome_message, message_id=message_id, reply_markup=new_keyboard, parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, text="К сожалению вы еще не сделали покупки", message_id=message_id, reply_markup=show_catalogs, parse_mode='Markdown')

async def edit_cart_amount_Sum(bot, callback_query: types.CallbackQuery, corzinaEdit):
    global message_id

    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    # Получение товара по номеру
    cursor.execute("SELECT quantity, articul, item_name, selected_variant, price FROM cart_items WHERE id = ?", (corzinaEdit,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    if rows:
        for item in rows:

            now_amount = item[0]
            new_amount = now_amount + 1
            database.update_all_amount_corzina(corzinaEdit, new_amount)
        welcome_message = create_cart_edit_message(callback_query.from_user.id)
        # welcome_message += '———\n'
        new_keyboard = create_cart_keyboard(callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    text=welcome_message, message_id=message_id,
                                    reply_markup=new_keyboard, parse_mode='Markdown')


async def edit_cart_amount_Min(bot, callback_query: types.CallbackQuery, corzinaEdit):
    welcome_message = '● Товары:'
    total_price = 0
    item_number = 1
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    # Получение товара по номеру
    cursor.execute("SELECT quantity, articul, item_name, selected_variant, price FROM cart_items WHERE id = ?", (corzinaEdit,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    if rows and rows[0][0] > 1:
        for item in rows:
            now_amount = item[0]
            new_amount = now_amount - 1
        database.update_all_amount_corzina(corzinaEdit, new_amount)
        welcome_message = create_cart_edit_message(callback_query.from_user.id)
        # welcome_message += '———\n'
        new_keyboard = create_cart_keyboard(callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    text=welcome_message, message_id=message_id,
                                    reply_markup=new_keyboard, parse_mode='Markdown')



async def clear_user_cart(user_id):
    """ Функция для очистки корзины пользователя в базе данных """
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


async def process_callback(bot, callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if callback_query.data == 'edit_cart':
        # await bot.delete_message(user_id, callback_query.message.message_id) # удаление сообщения с содержимым корзины
        await edit_cart(bot, callback_query)

    elif callback_query.data == 'show_basket':
        await show_cart(bot, callback_query)

    elif callback_query.data == 'clear_cart':
        conn = sqlite3.connect('data/user_corsina.db')
        cursor = conn.cursor()

        query = "SELECT item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?"
        cursor.execute(query,(user_id,))
        cart_items = cursor.fetchall()
        conn.close()

        for item in cart_items:
            articul = item[1]
            amount = item[3]
            now_amount = data.db.database.get_all_amount(articul)
            new_amount = amount + now_amount[0]
            data.db.database.update_all_amount(articul,new_amount)

        await clear_user_cart(user_id)
        await bot.edit_message_text(chat_id = user_id,message_id = callback_query.message.message_id,
                                    text = "👻 Ваша корзина теперь пуста 😢")

