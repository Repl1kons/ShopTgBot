import sqlite3
from data.db import database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import config
import corsina
from catalog import handle_catalog_button, show_category_products  # Импортируем новый обработчик
import photo_handler
import photo_hendler_two
from aiogram.types import ContentTypes,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.Markup import Markup_keyboards
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.Inline import Inline_keyboard


class PaymentState(StatesGroup):
    ASK_NAME = State()
    ASK_REGION = State()
    ASK_CITY = State()
    ASK_STREET = State()
    ASK_HOUSE = State()
    CONFIRMATION = State()

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage = storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_message = f'Привет, {message.from_user.first_name}!\nУ меня ты сможешь купить некоторые товары!\nКонтакт моего разработчика: https://t.me/Garnlzerx'
    await bot.send_message(message.chat.id, welcome_message, reply_markup=Markup_keyboards.main_menu)

@dp.message_handler(lambda message: message.text in ['🆘 Помощь', '/help'])
async def handle_help(message: types.Message):
    await bot.send_message(message.chat.id, "Команда Помощь")


@dp.message_handler(lambda message: message.text == "👨Профиль")
async def profil_user(message: types.Message):
    user_id = message.from_user.id
    user_data = database.get_user_data(user_id)
    if user_data:
        await bot.send_message(
            message.from_user.id,
            text = f"*Ваши текущие данные:*\n\n*Имя:*\n{user_data[0]}\n\n*Адрес:*\n{user_data[2]} обл, г.{user_data[1]}, ул.{user_data[3]},{user_data[4]}",
            reply_markup = Inline_keyboard.profil_data,
            parse_mode = 'Markdown'
        )
    else:
        await bot.send_message(user_id, f"Здравствуйте {message.from_user.username} 👋, зарегистрируйтесь пожалуйста в боте для работы магазина")
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(message.from_user.id,"Введите ваше имя в формате ФИО:")).message_id


@dp.message_handler(lambda message: message.text == '🛍 Каталог')
async def handle_catalog(message: types.Message):
    await handle_catalog_button(bot, message.chat.id)


@dp.message_handler(lambda message: message.text == '🛒 Корзина')
async def handle_corsina(message: types.Message):
    await corsina.show_cart(bot, message)

@dp.callback_query_handler(lambda c: c.data in ['clear_cart', "pay_cont"])
async def callback_handler(callback_query: types.CallbackQuery):
    await corsina.process_callback(bot, callback_query)

@dp.callback_query_handler(lambda c: c.data == 'payment')
async def start_payment_process(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = database.get_user_data(user_id)
    if user_data:
        await bot.send_message(
            callback_query.from_user.id,
            text = f"*Ваши текущие данные:*\n\n*Имя:*\n{user_data[0]}\n\n*Адрес:*\n{user_data[2]} обл., г.{user_data[1]}, ул.{user_data[3]},{user_data[4]}",
            reply_markup = Inline_keyboard.confirmation_keyboard
        )

    else:
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО: ")).message_id

@dp.callback_query_handler(lambda c: c.data == 'change_data', state='*')
async def change_data(callback_query: types.CallbackQuery, state: FSMContext):
    print("Обработчик change_data вызван")  # Для отладки
    try:
        database.delete_user(callback_query.from_user.id)
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id,"Введите ваше имя в формате ФИО: ")).message_id
    except Exception as e:
        print(f"Ошибка: {e}")

@dp.callback_query_handler(lambda c: c.data == 'confirm_data', state='*')
async def confirm_data(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = callback_query.from_user.id
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query,(user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    # Форматирование данных корзины для пользователя
    total_price = 0
    for item in cart_items:
        total_price += int(item[3] * item[4] - 800) # Главное не забыть убрать -800
    total_price = total_price
    print(f"total price {int(total_price)}")
    await bot.send_invoice(callback_query.from_user.id,
                           title = "Оплата корзины",
                           description = "Описание вашей корзины",
                           provider_token = config.PAYMENT_TOKEN,
                           currency = 'rub',
                           prices = [types.LabeledPrice(label = "Оплата корзины",amount = int(total_price*100))],
                           start_parameter = 'pay',
                           payload = 'test-invoice-payload')



@dp.message_handler(state=PaymentState.ASK_NAME)
async def process_name(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['name'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = "Теперь введите область:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.message_handler(state=PaymentState.ASK_REGION)
async def process_city(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['region'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = "Введите пожалуйста город в котором вы живете:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.message_handler(state=PaymentState.ASK_CITY)
async def process_city(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['city'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = "Отлично, осталось совсем чуть-чуть, теперь введите название вашей улицы:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


# Обработчик для состояния ASK_STREET
@dp.message_handler(state=PaymentState.ASK_STREET)
async def process_street(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['street'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = "И наконец, введите номер вашего дома:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)



# Обработчик для состояния ASK_HOUSE
@dp.message_handler(state=PaymentState.ASK_HOUSE)
async def process_house(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['house'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = f"Пожалуйста, подтвердите введенные данные."
                                                                                                f"\n\nИмя: {data['name']}\nОбласть: {data['region']}\nГород: {data['city']}\nУлица: {data['street']}\nДом: {data['house']}",
                                                                                                reply_markup = Inline_keyboard.user_data)
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'data-enter', state=PaymentState.CONFIRMATION)
async def process_data_enter(callback_query: types.CallbackQuery, state: FSMContext):
    global message_id

    async with state.proxy() as data:
        database.add_user(
            user_id = callback_query.from_user.id,
            name = data['name'],
            city = data['city'],
            region = data['region'],
            street = data['street'],
            number_house = data['house']
        )


    await bot.edit_message_text(chat_id = callback_query.message.chat.id,message_id = message_id,
                                text = "Отлично теперь нажмите на кнопку оплаты: ")
    await bot.delete_message(chat_id = callback_query.message.chat.id,message_id = callback_query.message.message_id)

    await state.finish()

    user_id = callback_query.from_user.id
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query,(user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    total_price = 0
    for item in cart_items:
        total_price += int(item[3] * item[4] - 800)  # Главное не забыть убрать -800
    total_price = total_price
    print(f"total price {int(total_price)}")
    await bot.send_invoice(callback_query.from_user.id,
                           title = "Оплата корзины",
                           description = "Описание вашей корзины",
                           provider_token = config.PAYMENT_TOKEN,
                           currency = 'rub',
                           prices = [types.LabeledPrice(label = "Оплата корзины",amount = int(total_price * 100))],
                           start_parameter = 'pay',
                           payload = 'test-invoice-payload')

@dp.callback_query_handler(lambda c: c.data == 'data-edit', state=PaymentState.CONFIRMATION)
async def process_data_edit(callback_query: types.CallbackQuery, state: FSMContext):
    await PaymentState.ASK_NAME.set()
    message_id = (await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id, text = "Опрос начинается заново. Введите ваше имя в формате ФИО: ")).message_id


@dp.callback_query_handler(lambda c: c.data in ['back', 'forward', 'choose_enter_categorical', 'back_return'])
async def callback_handler(callback_query: types.CallbackQuery):
    await photo_handler.process_callback(bot, callback_query)

@dp.callback_query_handler(lambda c: c.data in ['back-enter', 'forward-enter', 'choose_enter', 'amount_sum', 'amount_min'])
async def callback_handler(callback_query: types.CallbackQuery):
    await photo_hendler_two.process_callback(bot, callback_query)

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
    except Exception as e:
        print(f"Pay erorr: {e}")


@dp.message_handler(content_types = ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    user_id = message.from_user.id
    payment_info = message.successful_payment.to_python()
    for k,v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")

    # Извлечение данных пользователя
    user_data = database.get_user_data(user_id)
    if user_data:
        user_info = f"*Данные пользователя:*\nИмя: {user_data[0]}\nОбласть: {user_data[2]}\nГород: {user_data[1]}\nУлица: {user_data[3]}\nДом: {user_data[4]}"
    else:
        user_info = "Информация о пользователе не найдена."

    # Извлечение данных о заказе
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?",(user_id,))
    orders = cursor.fetchall()
    conn.close()

    order_info = "*Детали заказа:*\n"
    for item in orders:
        amount_price_1 = item[3] * item[4]
        order_info += f"*Товар:* {item[0]}\nАртикул: {item[1]}\nВариант: {item[2]}\nКоличество: {item[3]}\nОбщая стоимость заказа: {amount_price_1}\n\n"

    # Отправка информации пользователю
    await bot.send_message(1066300592,f"{user_info}\n\n{order_info}",parse_mode = 'Markdown')

    # Очистка корзины пользователя
    await corsina.clear_user_cart(user_id)


# @dp.message_handler(lambda message: message.text)
# async def process_user_input(message: types.Message):
#     user_input = message.text
#     for key in user:
#         if user[key] == '':
#             user[key] = user_input
#             break
#
#     await message.answer(f"Вы ввели: {user_input}")


@dp.callback_query_handler(lambda c: c.data.startswith('category'))
async def handle_category_choice(callback_query: types.CallbackQuery):
    category = callback_query.data.split('_')[1]
    await show_category_products(bot, callback_query.message.chat.id, category)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)