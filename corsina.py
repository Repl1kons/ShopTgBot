from aiogram import types

import config
import photo_hendler_two
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice






async def show_cart(message: types.Message):
    global total_price
    cart_contents = ""
    total_price = 0

    for key, details in photo_hendler_two.shopping_cart.items():
        item_name, articul = key.split('_')
        selected_variant = details[0]
        quantity = int(details[2])
        price = int(details[3]) * quantity  # Цена за количество товара

        total_price += price

        # Форматирование информации о товаре
        item_info = f"*{item_name}*\nАртикул: {articul}\nВариант: {selected_variant + 1}\nКоличество: {quantity}\nЦена за единицу: {int(details[3])} рублей"

        # Добавляем информацию о товаре в корзину
        cart_contents += f"\n\n{item_info}" if cart_contents else item_info

    clear_button = InlineKeyboardButton(text='Очистить', callback_data='clear_cart')
    payment_button = InlineKeyboardButton(text='Оплатить', callback_data='payment')
    keyboard = InlineKeyboardMarkup().add(clear_button, payment_button)

    if cart_contents:
        cart_contents += f"\n\nОбщая цена: {total_price} рублей"  # Добавляем общую цену
        await message.answer(f"*🛒 Ваша Корзина*\n\n{cart_contents}", reply_markup=keyboard, parse_mode='Markdown')
    else:
        await message.answer("Корзина пуста.")


async def process_callback(bot, callback_query):
    global total_price
    if callback_query.data == 'clear_cart':
        photo_hendler_two.shopping_cart.clear()
        await bot.send_message(callback_query.message.chat.id, "Корзина очищена.")
    if callback_query.data == 'payment':
        print(f"total_price {total_price}")
        await bot.send_message(callback_query.message.chat.id, "Данные тестовой карты:\nНомер: 1111 1111 1111 1026\nСрок действия: 12/22\nCVC: 000")
        PRICE = types.LabeledPrice(label = "Оплата корзины", amount = total_price*100)
        await bot.send_invoice(callback_query.message.chat.id,
            title = "Оплата корзины",
            description = "sdsdsd",
            provider_token = config.PAYMENT_TOKEN,
            currency = 'rub',
            prices = [PRICE],
            start_parameter = 'pay',
            payload = 'test-invoice-payload')