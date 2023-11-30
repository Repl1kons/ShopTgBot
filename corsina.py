from aiogram import types
import config
import photo_hendler_two
from aiogram.types import LabeledPrice
from keyboards.Inline import Inline_keyboard

price_all = {
    "total_price": 0
}

price_a = {
    'total_price': 0
}


import sqlite3

async def add_to_cart(user_id, item_name, articul, selected_variant, quantity, price):
    conn = sqlite3.connect('data/bot_database.db')  # Подключение к базе данных
    cursor = conn.cursor()

    # SQL-команда для добавления товара в корзину
    cursor.execute("""
        INSERT INTO cart_items (user_id, item_name, articul, selected_variant, quantity, price) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, item_name, articul, selected_variant, quantity, price))

    conn.commit()
    conn.close()


async def show_cart(bot, message: types.Message):
    # cart_contents = ""
    # price_a["total_price"] = 0
    # for key,details in photo_hendler_two.shopping_cart.items():
    #     item_name,articul = key.split('_')
    #     selected_variant = details[0]
    #     quantity = details[2]
    #     price = details[3]
    #     item_total_price = quantity * price
    #     print(item_name)
    #     print(articul)
    #     print(quantity)
    #     print(price)
    #     price_a['total_price'] += item_total_price
    #
    #     cart_contents += f"{item_name}\nАртикул: {articul}\n Вариант: {selected_variant}\n Количество: {quantity}\n Цена за единицу: {price}\n В сумме: {item_total_price}\n\n"
    user_id = message.from_user.id
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query,(user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    # Форматирование данных корзины для пользователя
    cart_contents = ""
    total_price = 0
    amount_price = 0
    for item in cart_items:
        print(cart_items)
        amount_price = item[3] * item[4]
        total_price += item[4] * item[3]
        print(total_price)
        cart_contents += f"*Товар:* {item[0]}\nАртикул: {item[1]}\nВариант: {item[2]}\nКоличество: {item[3]}\nЦена за единицу: {item[4]}\nЦена: {amount_price}\n\n"

    if cart_contents:
        # await clear_user_cart(user_id)
        cart_contents += f"Общая цена: {total_price} рублей"
        await bot.send_message(user_id, f"*🛒 Ваша Корзина*\n\n{cart_contents}", reply_markup = Inline_keyboard.keyboard_basket, parse_mode='Markdown')
    else:
        await bot.send_message(user_id,"корзина пуста")





    # if cart_contents:
    #     cart_contents += f"\n\nОбщая цена: {price_a['total_price']} рублей"  # Добавляем общую цену
    #     await message.answer(f"*🛒 Ваша Корзина*\n\n{cart_contents}", reply_markup=Inline_keyboard.keyboard_basket, parse_mode='Markdown')
    # else:
    #     await message.answer("Корзина пуста.")

async def clear_user_cart(user_id):
    """ Функция для очистки корзины пользователя в базе данных """
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


async def process_callback(bot, callback_query):
    # print(f'price_a: {price_a["total_price"]}')
    if callback_query.data == 'clear_cart':
        await clear_user_cart(callback_query.message.chat.id)
        await bot.send_message(callback_query.message.chat.id, "Корзина очищена.")
        price_a.clear()
        print(price_a)
