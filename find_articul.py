import os
import sqlite3
from aiogram import types

import catalog
import config
import corsina
from data import db
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.Inline import Inline_keyboard
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SetAmount(StatesGroup):
    new_amount = State()

def get_articul_data(articul):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    cursor.execute('SELECT articul, name_product, variant,price, photo_path, all_amount FROM product WHERE articul = ?', (articul,))
    articul_data = cursor.fetchone()
    conn.commit()
    conn.close()
    return articul_data if articul_data else None




async def start_articul(bot, chat_id, articul_numb):
    # db.database.delete_user(chat_id)
    global caption

    global photo_message_id
    global articul_data
    try:

        articul_data = get_articul_data(articul_numb)

        # start_articul = (await bot.send_message(chat_id, f"Вы ввели артикул: {articul_numb}")).message_id
        if articul_data:
            print(articul_data)
            if articul_data[5] > 0:
                caption = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: 1\nОсталось: {articul_data[5]}"
                if chat_id == config.ID_ADMIN:
                    from keyboards.Inline.Inline_keyboard import product_show_articul_for_admin
                    photo_message_id = (await bot.send_photo(chat_id, photo = InputFile(articul_data[4]), caption = caption, parse_mode = "Markdown", reply_markup = product_show_articul_for_admin)).message_id

                else:
                    caption = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: 1\nОсталось: {articul_data[5]}"
                    from keyboards.Inline.Inline_keyboard import product_show_articul
                    photo_message_id = (await bot.send_photo(chat_id,photo = InputFile(articul_data[4]),caption = caption,parse_mode = "Markdown",
                                             reply_markup = product_show_articul)).message_id
                print(articul_data)
                global amount_to_buy

                amount_to_buy = 1
            else:
                caption = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nК сожалению данный товар закончился😢"
                if chat_id == config.ID_ADMIN:
                    from keyboards.Inline.Inline_keyboard import product_show_articul_nol_for_admin
                    photo_message_id = (await bot.send_photo(chat_id,photo = InputFile(articul_data[4]),caption = caption,
                                                             parse_mode = "Markdown",
                                                             reply_markup = product_show_articul_nol_for_admin)).message_id

                else:
                    from keyboards.Inline.Inline_keyboard import product_show_articul_nol
                    await bot.send_photo(chat_id,photo = InputFile(articul_data[4]),caption = caption,
                                                             parse_mode = "Markdown",
                                                             reply_markup = product_show_articul_nol)
                print(articul_data)
                amount_to_buy = 1
                print(amount_to_buy)
        else:
            await bot.delete_message(chat_id, start_articul)
            await catalog.ArticulForm.articul_numb.set()
            await bot.send_message(chat_id, "Данный артикул некорректен, пожалуйста проверьте и напишите его заново!!\n"
                                            "Если все правильно, то вы можете обратиться к нам за помощью (в команде 🆘 Помощь или /help)\n\n"
                                            "Попробуйте ввести артикул заново")
    except Exception as e:
        logging.error(f"Ошибка при обработке start_articul: {e}",exc_info = True)


async def set_amount_art(bot, message: types.Message, state: FSMContext):
    global articul_data
    user_id = message.from_user.id
    new_amount = message.text.strip()

    if not new_amount.isdigit():
        await message.answer("Пожалуйста, введите число")
        return

    await bot.send_message(user_id, f"Вы указали кол-во {new_amount}")
    db.database.update_all_amount(articul_data[0], new_amount)
    await bot.send_message(user_id, f"Кол-во для {articul_data[0]} было обновлено на {new_amount}")
    await state.finish()

async def process_callback(bot, callback_query, state):
    global amount_to_buy
    # global photo_message_id
    global articul_data
    global caption

    if callback_query.data == 'amount_sum_1':
        max_amount = db.database.get_all_amount(articul_data[0])[0]
        # print(all_amount[0])
        if amount_to_buy < max_amount:
            amount_to_buy += 1
            print(amount_to_buy)
    elif callback_query.data == 'amount_min_1':
        if amount_to_buy > 1:
            amount_to_buy -= 1
            print(amount_to_buy)
    elif callback_query.data == 'set_amount':
        await SetAmount.new_amount.set()
        await bot.send_message(callback_query.message.chat.id, "Введите кол-во для данного товара: ")

    elif callback_query.data == 'choose_enter_1':
        new_amount_1 = db.database.get_all_amount(articul_data[0])
        if new_amount_1[0] > 0:
            category = articul_data[4].split('_')[2]
            await corsina.add_to_cart(callback_query.message.chat.id,articul_data[1],articul_data[0],articul_data[2],amount_to_buy,articul_data[3],category)
            await db.database.add_product(articul_data[0],articul_data[1],articul_data[2],articul_data[3],articul_data[4])
            await bot.send_message(callback_query.message.chat.id,
                                   f"Товар {articul_data[1]}:\n\nАртикул: {articul_data[0]}\nВыбранный вариант: {articul_data[2]}\nКоличество: {amount_to_buy}\nЦена: {articul_data[3] * amount_to_buy}\n\nБыл успешно добавлен в корзину 💵‍",
                                   reply_markup = Inline_keyboard.show_basket_add)


            new_amount = new_amount_1[0] - amount_to_buy
            db.database.update_all_amount(articul_data[0],new_amount)
            caption = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: {amount_to_buy}\nОсталось: {articul_data[5]}"
        else:
            await bot.send_message(callback_query.message.chat.id, "К сожалению товар закончился 😢")


    # caption = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: {amount_to_buy}\nОсталось: {articul_data[5]}"
    all_amount_prod = db.database.get_all_amount(articul_data[0])
    if callback_query.message.chat.id == config.ID_ADMIN:
        if all_amount_prod[0] > 0:
            caption_text = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: {amount_to_buy}\nОсталось: {articul_data[5]}"
            await bot.edit_message_caption(
                chat_id = callback_query.message.chat.id,
                message_id = callback_query.message.message_id,
                caption = caption_text,
                reply_markup = Inline_keyboard.product_show_articul_for_admin,
                parse_mode = 'Markdown')
        else:
            caption_text = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nК сожалению данный товар закончился😢"
            await bot.edit_message_caption(
                chat_id = callback_query.message.chat.id,
                message_id = callback_query.message.message_id,
                caption = caption_text,
                reply_markup = Inline_keyboard.product_show_articul_nol_for_admin,
                parse_mode = 'Markdown')
    else:
        if all_amount_prod[0] > 0:
            caption_text = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nКол-во: {amount_to_buy}\nОсталось: {articul_data[5]}"
            await bot.edit_message_caption(
                chat_id = callback_query.message.chat.id,
                message_id = callback_query.message.message_id,
                caption = caption_text,
                reply_markup = Inline_keyboard.product_show_articul,
                parse_mode = 'Markdown')
        else:
            caption_text = f"*{articul_data[1]}*\n*Вариант товара*: {articul_data[2]}\n*Цена*: {articul_data[3]}\nК сожалению данный товар закончился😢"
            await bot.edit_message_caption(
                chat_id = callback_query.message.chat.id,
                message_id = callback_query.message.message_id,
                caption = caption_text,
                reply_markup = Inline_keyboard.product_show_articul_nol,
                parse_mode = 'Markdown')