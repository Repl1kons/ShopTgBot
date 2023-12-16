from aiogram import types, Dispatcher

import data.db.database
from keyboards.Inline import Inline_keyboard
import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def add_to_cart(user_id, item_name, articul, selected_variant, quantity, price, selected_category):
    conn = sqlite3.connect('data/bot_database.db')  # Подключение к базе данных
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
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    cart_contents = ""
    total_price = 0
    item_number = 1

    for item in cart_items:
        amount_price = item[3] * item[4]
        total_price += amount_price
        cart_contents += f"{item_number}. *Товар:* {item[0]}\nАртикул: {item[1]}\nВариант: {item[2]}\nКоличество: {item[3]}\nЦена за единицу: {item[4]}\nОбщая цена: {amount_price}\n\n"
        item_number += 1  # Увеличиваем счетчик для следующего товара
    global message_id
    if cart_contents:
        cart_contents += f"Доставка: 300 руб\n*Всего к оплате: {total_price + 300} руб.*"
        message_id = (await bot.send_message(user_id, f"*🛒 Ваша Корзина*\n\n{cart_contents}", reply_markup=Inline_keyboard.keyboard_basket, parse_mode='Markdown')).message_id
    else:
        message_id = (await bot.send_message(user_id, "👻 Ваша корзина пуста 😢")).message_id



class CartEditState(StatesGroup):
    awaiting_item_number = State()


async def item_number_received(bot, message: types.Message,state: FSMContext):
    user_id = message.from_user.id
    item_number = message.text.strip()

    if not item_number.isdigit():
        await message.answer("Пожалуйста, введите числовой номер товара.")
        return

    item_number = int(item_number) - 1  # Переводим в индекс массива (начинается с 0)

    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    # Получение товара по номеру
    cursor.execute("SELECT id FROM cart_items WHERE user_id = ? ORDER BY id",(user_id,))
    rows = cursor.fetchall()

    if item_number < 0 or item_number >= len(rows):
        await message.answer("Товар с таким номером не найден.")
    else:
        item_id = rows[item_number][0]
        cursor.execute("DELETE FROM cart_items WHERE id = ?",(item_id,))
        conn.commit()
        await bot.delete_message(message.chat.id, message.message_id)
        await show_cart(bot, message)

    conn.close()
    await state.finish()


async def clear_user_cart(user_id):
    """ Функция для очистки корзины пользователя в базе данных """
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

#
# async def process_callback(bot, callback_query):
#     global message_id
#     if callback_query.data == 'clear_cart':
#         await clear_user_cart(callback_query.message.chat.id)
#         await bot.edit_message_text(chat_id = callback_query.message.chat.id,message_id = message_id, text = "👻 Пока что тут пусто 😢")
    # if callback_query.data == "edit_cart":

async def process_callback(bot, callback_query: types.CallbackQuery, state):
    user_id = callback_query.from_user.id

    if callback_query.data == 'edit_cart':
        await CartEditState.awaiting_item_number.set()
        await bot.delete_message(user_id, callback_query.message.message_id)
        await bot.send_message(user_id, "Введите номер товара для удаления:\n\nИли нажмите на кнопку что бы вернуться назад", reply_markup = Inline_keyboard.show_basket_add)

    elif callback_query.data == 'clear_cart':
        await clear_user_cart(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id, text="👻 Ваша корзина теперь пуста 😢")

    elif callback_query.data == 'show_basket':
        await state.finish()
        await show_cart(bot, callback_query)

# def register_handlers():
#     dp.register_callback_query_handler(process_callback, lambda c: c.data in ['edit_cart', 'clear_cart'], state='*')
#     dp.register_message_handler(item_number_received, state=CartEditState.awaiting_item_number)

