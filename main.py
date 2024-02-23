import logging
import random
import sqlite3
from contextlib import suppress

import catalog
import find_articul
import more_category
import profil_register
from data.db import database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import config
import corsina
from catalog import handle_catalog_button, show_category_products
import photo_handler
import photo_hendler_two
from aiogram.types import ContentTypes,InlineKeyboardMarkup,InlineKeyboardButton
from keyboards.Markup import Markup_keyboards
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.Inline import Inline_keyboard
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# logger = logging.getLogger('Shop-bot')
#
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# file_handler = logging.FileHandler("bot_logs.txt")
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)


import gspread

# async def init_image_caption():
#     image_captions = []
#
#     gc = gspread.service_account(filename = 'shoptg-97da5d92bfcd.json')
#     sh = gc.open("ShopTgTable")
#     worksheet = sh.sheet1
#     for index, row in enumerate(worksheet.get_all_values()):
#         if index == 0:
#             continue  # Пропускаем 1 строку
#         if row:
#             category = row[0]
#             subcategories = []
#             for i in range(1, len(row), 6):
#                 subcategory = [row[i], row[i + 1], row[i + 2]]
#                 subcategories.append(subcategory)
#             image_captions.append([category, subcategories])
#     print(image_captions)


class PaymentState(StatesGroup):
    ASK_NAME = State()
    ASK_REGION = State()
    ASK_CITY = State()
    ASK_STREET = State()
    ASK_HOUSE = State()
    ASK_APARTMENT = State()
    ASK_INDECS = State()
    CONFIRMATION = State()


storage = MemoryStorage()
bot = Bot(token = config.BOT_TOKEN)
dp = Dispatcher(bot, storage = storage)
cluster = AsyncIOMotorClient(host = 'localhost:27017')
db = cluster.ShopTgBot



@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    start_param = message.get_args()
    print(start_param)

    user_data = await db.User.find_one({'_id': message.from_user.id})

    if user_data:
        # Если пользователь уже есть, выводим сообщение
        await message.answer("Вы уже зарегистрированы в базе данных.")
    else:
        with suppress(DuplicateKeyError):
            await db.User.insert_one(dict(
                _id = message.from_user.id,
                data = {
                    'name': '',
                    'age': 0,
                    'phone': "",
                    'email': "",
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'username': message.from_user.username,
                    'language': message.from_user.language_code,
                    'is_bot': message.from_user.is_bot,
                    'tg_premium': message.from_user.is_premium

                },
                currency_date = {
                    'name': '',
                    'week': '',
                    'day': '',
                    'eventId': ''
                }
            ))

            await db.State.insert_one(dict(
                _id = message.from_user.id,
                appointment = {
                    'name': '',
                    'age': 0,
                    'requests': '',
                    'day': '',
                    'time': ''
                },
                tarif_marafons = {
                    'name': '',
                    'age': 0,
                    'marathon': '',
                    'tarif': '',
                    'waited': '',
                    'target': '',
                    'link': ''
                },
                notebook = {
                    'cur_img_ind': 0,
                    'path_more': '',
                    'path_name': '',
                    'price': 0,
                    'amount': 1,
                    'path': '',
                    'text': '',
                    'product_name': '',
                    'more': {
                        'cur_img_ind': 0
                    }
                }

            ))

            await message.answer("Вы успешно зарегистрированы в базе данных.")
    # await init_image_caption()

    welcome_message = \
        f"*🎉 Здравствуй, {message.from_user.first_name}!*\n\n" \
        f"Я - *твой личный шопинг-бот* 🛍️.\nВот что я могу предложить:\n\n" \
        f"- ✒️ *Уникальные обложки*\n" \
        f"- 📘 *Стильные ежедневники*\n" \
        f"- 🌟 *И многое другое*\n\n" \
        f"*Создано специально для it's my planner | by A-STUDENT!*"
        # f"Вы передали параметр: {start_param}"

    await bot.send_message(message.chat.id, welcome_message, reply_markup = Markup_keyboards.main_menu,
                               parse_mode = 'Markdown')
    if start_param.isdigit():
        await find_articul.start_articul(bot,message.chat.id,start_param)

@dp.message_handler(lambda message: message.text in ['🆘 Помощь', '/help'])
async def handle_help(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Если у вас есть вопросы по поводу работе бота или другая информация - напишите нам\n https://t.me/Garnlzerx")

@dp.callback_query_handler(lambda c: c.data in ['myOrder', 'return_order'])
async def my_order(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    global show_order_message
    print("MyOrder")
    if callback_query.from_user.id == config.ID_ADMIN:
        user_order = database.get_all_user_order()
    else:
        user_order = database.get_user_order(callback_query.from_user.id)
    if user_order:
        current_order_number = None
        show_order = InlineKeyboardMarkup(row_width = 1)
        for order in user_order:
            if order[0] != current_order_number:
                order_button = InlineKeyboardButton(text = order[0],callback_data = f'order_{order[0]}')
                show_order.add(order_button)
                current_order_number = order[0]
        returnProfilButton = InlineKeyboardButton(text = 'Назад',callback_data = 'returnProfil')
        show_order.add(returnProfilButton)


        # global all_price
        # for order in user_order:
        #     if order[0] != current_order_number:
        #         if current_order_number is not None:
        #             orders_text += f"Статус заказа: Создан\n\n"
        #         current_order_number = order[0]
        #         orders_text += f"*Заказ: {current_order_number}*\n"
        #         item_number = 1
        #         all_price = 0
        #
        #     orders_text += f"{item_number}. Товар: {order[1]}\n" \
        #                    f"Артикул: {order[2]}\n" \
        #                    f"Вариант: {order[3]}\n" \
        #                    f"Кол-во: {order[4]}\n\n"
        #     print(order)
        #
        #     item_number += 1
        #     all_price += order[5]
        #
        # orders_text += f"Статус заказа: Создан\n"
        show_order_message = (await bot.send_message(callback_query.from_user.id,text = f"*Выберите номер заказа для просмотра*\n\n", parse_mode = 'Markdown', reply_markup = show_order)).message_id
    else:
        await bot.send_message(callback_query.message.chat.id, "Похоже вы еще не сделали ни одного заказа🤨", reply_markup = Inline_keyboard.returnProfil)


@dp.message_handler(commands=['status'])
async def status_command(message):
    with open("app.log", "rb") as log_file:
        await bot.send_document(message.chat.id, log_file)

@dp.callback_query_handler(lambda c: c.data.startswith('order'))
async def handle_category_choice(callback_query: types.CallbackQuery):

    global show_order_message
    text_order_info = ''
    global order
    order = callback_query.data.split('_')[1]
    order_info = database.get_user_order_order_id(order)
    text_order_info += f"*Заказ: {order}*\n\n"
    item_number = 1
    show_order = InlineKeyboardMarkup(row_width = 1)


    for order_inf in order_info:
        text_order_info += f"{item_number}. Товар: {order_inf[0]}\n" \
                       f"Артикул: {order_inf[1]}\n" \
                       f"Вариант: {order_inf[2]}\n" \
                       f"Кол-во: {order_inf[3]}\n\n"
        item_number += 1
        status = order_inf[5]
        user_id = order_inf[6]
    user_data = database.get_user_data(user_id)
    if callback_query.from_user.id == config.ID_ADMIN:
        if user_data:
            text_order_info += f"*Данные пользователя:*\nИмя: {user_data[0]}\nОбласть: {user_data[2]}\nГород: {user_data[1]}\nУлица: {user_data[3]}\nДом: {user_data[4]}\nКвартира: {user_data[5]}\nИндекс: {user_data[6]}"
        returnOrderButton = InlineKeyboardButton(text = 'Назад',callback_data = 'return_order')
        order_button = InlineKeyboardButton(text = "Установить статус",callback_data = f'set_status')
        show_order.add(order_button)
        show_order.insert(returnOrderButton)
        await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id = show_order_message, text = text_order_info, parse_mode = 'Markdown', reply_markup = show_order) # Inline_keyboard.returnOrder
    else:
        text_order_info += f"Статус заказа: {status}\n"
        await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id = show_order_message, text = text_order_info, parse_mode = 'Markdown', reply_markup = Inline_keyboard.returnOrder)
    # await show_category_products(bot, callback_query.message.chat.id, category)

@dp.callback_query_handler(lambda c: c.data == 'set_status')
async def callback_handler_4(callback_query: types.CallbackQuery):
    global order
    set_status_keyboard = InlineKeyboardMarkup(row_width = 1)
    returnOrderButton = InlineKeyboardButton(text = 'В пути',callback_data = 'editStatus_Отправлен')
    order_button = InlineKeyboardButton(text = "Доставлен",callback_data = f'editStatus_Доставлен')
    set_status_keyboard.add(order_button)
    set_status_keyboard.insert(returnOrderButton)
    await bot.send_message(callback_query.from_user.id, f"выберите статус для заказа {order}:", reply_markup = set_status_keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("editStatus"))
async def callback_handler_4(callback_query: types.CallbackQuery):
    global order
    status = callback_query.data.split('_')[1]
    # print(status)
    database.update_status_order(order, status)
    await bot.send_message(callback_query.from_user.id, f"Статус заказа был изменен на {status}")



@dp.message_handler(lambda message: message.text == "Админ епт")
async def adminMod(message: types.Message):
    await bot.send_message(message.chat.id, "Ты как общаешься сучка")

@dp.message_handler(lambda message: message.text == "👨Профиль")
async def profil_user(message: types.Message):
    user_id = message.from_user.id
    user_data = database.get_user_data(user_id)
    if user_data:
        full_name = user_data[0].split(' ')
        first_name = full_name[1]
        last_name = full_name[0]
        surname = full_name[2]
        text  = f"🙍 <b>Профиль пользователя:</b>\n" \
                f"🆔 <i>ID:</i> {user_id}\n"\
                f"👤 <i>Никнейм:</i> {message.from_user.username}\n\n"\
                f"👤 <b>Имя пользователя:</b>\n"\
                f"┌ <i>Фамилия:</i> {last_name}\n"\
                f"├ <i>Имя:</i> {first_name}\n"\
                f"└ <i>Отчество:</i> {surname}\n\n"\
                f"🏠 <b>Адрес:</b>\n"\
                f"┌ <i>Область:</i> {user_data[2]}\n"\
                f"├ <i>Город:</i> {user_data[1]}\n"\
                f"├ <i>Улица:</i> {user_data[3]}\n"\
                f"├ <i>Дом:</i> {user_data[4]}\n"\
                f"└ <i>Индекс:</i> {user_data[5]}"

        await bot.send_message(message.from_user.id, text = text, reply_markup = Inline_keyboard.profil_data_1,
        parse_mode = 'HTML')


    else:
        await bot.send_message(user_id,
                               f"Здравствуйте {message.from_user.username} 👋\nВ данный момент вы не зарегистрированы в боте. Вы можете начать регистрироваться сейчас.",
                               reply_markup = Inline_keyboard.not_profil_data)

# @dp.callback_query_handler(lambda c: c.data == 'returnProfil')
# async def callback_handler(callback_query: types.CallbackQuery):
#     await profil_user(callback_query)

@dp.message_handler(state = catalog.ArticulForm.articul_numb)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["articul"] = message.text
        await catalog.get_articul(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'create_data_profil')
async def callback_handler(callback_query: types.CallbackQuery):
    await profil_register.process_callback(bot, callback_query, State)


@dp.callback_query_handler(lambda c: c.data == 'show_basket_1')
async def callback_handler(callback_query: types.CallbackQuery):
    await corsina.show_cart(bot, callback_query)


@dp.message_handler(state = profil_register.ProfilState.GET_NAME)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["name"] = message.text
        await profil_register.get_name(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = profil_register.ProfilState.GET_REGION)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["region"] = message.text
        await profil_register.get_region(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = profil_register.ProfilState.GET_CITY)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["city"] = message.text
        await profil_register.get_city(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = profil_register.ProfilState.GET_STREET)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["street"] = message.text
        await profil_register.get_street(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = profil_register.ProfilState.GET_HOUSE)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["house"] = message.text
        await profil_register.get_house_numb(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.message_handler(state = profil_register.ProfilState.GET_APARTMENT)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["apartment"] = message.text
        await profil_register.get_apartment(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = profil_register.ProfilState.GET_INDECS)
async def start_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["indecs"] = message.text
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)
        await profil_register.get_indecs(bot, message, state)
        await bot.send_message(message.from_user.id,
                               f"Пожалуйста, подтвердите введенные данные.\n\n"
                               f"Имя: {profil_data['name']}\n"
                               f"Область: {profil_data['region']}\n"
                               f"Город: {profil_data['city']}\n"
                               f"Улица: {profil_data['street']}\n"
                               f"Дом: {profil_data['house']}\n"
                               f"Квартира: {profil_data['apartment']}\n"
                               f"Индекс: {profil_data['indecs']}",
                               reply_markup = Inline_keyboard.user_data_1)


@dp.callback_query_handler(lambda c: c.data == 'change_data_1', state = '*')
async def change_data(callback_query: types.CallbackQuery):
    database.delete_user(callback_query.from_user.id)
    await profil_register.process_callback(bot, callback_query, State)


@dp.callback_query_handler(lambda c: c.data == 'return_order')
async def return_on_order(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await my_order(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'returnProfil')
async def return_on_profile(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await profil_user(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'data-enter_1', state = profil_register.ProfilState.CONFIRMATION)
async def process_data_enter(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id = callback_query.from_user.id, message_id = callback_query.message.message_id)
    await profil_register.conf(bot, callback_query, state)


@dp.callback_query_handler(lambda c: c.data == 'data-edit_1', state = profil_register.ProfilState.CONFIRMATION)
async def process_data_edit(callback_query: types.CallbackQuery):
    database.delete_user(callback_query.from_user.id)
    await profil_register.process_callback(bot, callback_query, State)



@dp.callback_query_handler(lambda c: c.data == 'create_data')
async def create_info_user(message: types.Message):
    await PaymentState.ASK_NAME.set()
    global message_id
    message_id = (await bot.send_message(message.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")).message_id


@dp.message_handler(lambda message: message.text == '🛍 Каталог')
async def handle_catalog_1(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await handle_catalog_button(bot, message.chat.id)


@dp.callback_query_handler(lambda c: c.data == 'back_return')
async def back_return(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await handle_catalog_button(bot, callback_query.message.chat.id)


@dp.message_handler(lambda message: message.text == '🛒 Корзина')
async def handle_corsina(message: types.Message):
    await corsina.show_cart(bot, message)

@dp.callback_query_handler(lambda c: c.data in ['clear_cart', "pay_cont", "edit_cart", "show_basket"])
async def callback_handler(callback_query: types.CallbackQuery):
    await corsina.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data == 'payment')
async def start_payment_process(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = database.get_user_data(user_id)
    if user_data:
        await bot.send_message(
            callback_query.from_user.id,
            text = f"*Ваши текущие данные:*\n\n*Имя:*\n{user_data[0]}\n\n*Адрес:*\n{user_data[2]} обл., г.{user_data[1]}, ул.{user_data[3]},{user_data[4]}., {user_data[5]}\nИндекс: {user_data[6]}",
            reply_markup = Inline_keyboard.confirmation_keyboard,
            parse_mode = 'Markdown'
        )

    else:
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату ")).message_id


@dp.callback_query_handler(lambda c: c.data == 'change_data', state = '*')
async def change_data(callback_query: types.CallbackQuery, state: FSMContext):
    print("Обработчик change_data вызван")  # Для отладки
    try:
        database.delete_user(callback_query.from_user.id)
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")).message_id
    except Exception as e:
        print(f"Ошибка: {e}")




@dp.callback_query_handler(lambda c: c.data == 'confirm_data', state = '*')
async def confirm_data(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = callback_query.from_user.id
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    # Форматирование данных корзины для пользователя
    total_price = 0
    for item in cart_items:
        total_price += int(item[3] * item[4])  # Главное не забыть убрать -800
    print(f"total price {int(total_price)}")
    await bot.send_invoice(callback_query.from_user.id,
                           title = "Оплата корзины",
                           description = "Описание вашей корзины",
                           provider_token = config.PAYMENT_TOKEN,
                           currency = 'rub',
                           prices = [
                               types.LabeledPrice(
                                   label = "Оплата корзины",
                                   amount = int(total_price * 100)
                               ),
                               types.LabeledPrice(
                                   label = "Доставка",
                                   amount = 30000
                               )
                           ],
                           max_tip_amount = 50000,
                           suggested_tip_amounts = [10000, 15000, 20000, 30000],
                           start_parameter = 'pay',
                           payload = 'test-invoice-payload')




@dp.message_handler(state = find_articul.SetAmount.new_amount)
async def edit_cart(message: types.Message, state: FSMContext):
    async with state.proxy() as data_amount:
        data_amount["new_amount"] = message.text
        await find_articul.set_amount_art(bot, message, state)

@dp.message_handler(state = PaymentState.ASK_NAME)
async def process_name(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        if len(message.text.split()) == 3:
            data['name'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id, text = "Теперь введите область:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = PaymentState.ASK_REGION)
async def process_city(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['region'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = "Введите пожалуйста город в котором вы живете:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = PaymentState.ASK_CITY)
async def process_city(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['city'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = "Отлично, осталось совсем чуть-чуть, теперь введите название вашей улицы:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = PaymentState.ASK_STREET)
async def process_street(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['street'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = "Введите номер вашего дома:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = PaymentState.ASK_HOUSE)
async def process_street(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['house'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = "Теперь введите номер квартиры")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


@dp.message_handler(state = PaymentState.ASK_APARTMENT)
async def process_street(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['apartment'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = "И наконец, введите индекс")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.message_handler(state = PaymentState.ASK_INDECS)
async def process_house(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
        data['indecs'] = message.text
    await PaymentState.next()
    await bot.edit_message_text(chat_id = message.from_user.id, message_id = message_id,
                                text = f"Пожалуйста, подтвердите введенные данные."
                                       f"\n\nИмя: {data['name']}\nОбласть: {data['region']}\nГород: {data['city']}\nУлица: {data['street']}\nДом: {data['house']}\nКвартира: {data['apartment']}\nИндекс: {data['indecs']}",
                                reply_markup = Inline_keyboard.user_data)
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('back_to_choose'))
async def callback_handler_2(callback_query: types.CallbackQuery):
    product = callback_query.data.split('_')[1]
    cur_img_indx = int(callback_query.data.split('_')[2])
    cur_img_capt = int(callback_query.data.split('_')[3])
    await photo_handler.process_callback(bot, callback_query, cur_img_indx, cur_img_capt, product, db)

@dp.callback_query_handler(lambda c: c.data == 'data-enter', state = PaymentState.CONFIRMATION)
async def process_data_enter(callback_query: types.CallbackQuery, state: FSMContext):
    global message_id
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        database.add_user(
            user_id = user_id,
            name = data['name'],
            city = data['city'],
            region = data['region'],
            street = data['street'],
            number_house = data['house'],
            apartment = data['apartment'],
            indecs = data['indecs']
        )

    await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id = message_id,
                                text = "Отлично теперь нажмите на кнопку оплаты: ")
    await bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id)

    await state.finish()

    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    total_price = 0
    for item in cart_items:
        total_price += int(item[3] * item[4])

    print(f"total price {int(total_price)}")
    await bot.send_invoice(callback_query.from_user.id,
                           title = "Оплата корзины",
                           description = "Описание вашей корзины",
                           provider_token = config.PAYMENT_TOKEN,
                           currency = 'rub',
                           prices = [
                               types.LabeledPrice(
                                   label = "Оплата корзины",
                                   amount = int(total_price * 100)
                               ),
                               types.LabeledPrice(
                                   label = "Доставка",
                                   amount = 30000
                               )
                           ],
                           max_tip_amount = 50000,
                           suggested_tip_amounts = [10000, 20000, 30000, 40000],
                           start_parameter = 'pay',
                           payload = 'test-invoice-payload')


@dp.callback_query_handler(lambda c: c.data == 'data-edit',state = PaymentState.CONFIRMATION)
async def process_data_edit(callback_query: types.CallbackQuery, state: FSMContext):
    await PaymentState.ASK_NAME.set()
    message_id = (await bot.edit_message_text(chat_id = callback_query.message.chat.id,
                                              message_id = callback_query.message.message_id,
                                              text = "Опрос начинается заново. Введите ваше имя в формате ФИО: ")).message_id




dp.callback_query_handler(lambda c: c.data.startswith(('back_notebook_more', 'forward_notebook_more', 'pay_notebook_more', 'back_notebook_more')))
async def callback_handler_2(callback_query: types.CallbackQuery):
    cur_img_ind = int(callback_query.data.split('_')[3])

@dp.callback_query_handler(lambda c: c.data.startswith(('categoryBack', 'categoryForward', 'choose-enter-categorical', 'categoryMore')))
async def callback_handler_2(callback_query: types.CallbackQuery):
    product = callback_query.data.split('_')[1]
    cur_img_indx = int(callback_query.data.split('_')[2])
    cur_img_capt = int(callback_query.data.split('_')[3])
    await photo_handler.process_callback(bot, callback_query, cur_img_indx, cur_img_capt, product, db)


@dp.callback_query_handler(lambda c: c.data in ['back_1', 'forward_1', 'back_return_1'])
async def callback_handler_2(callback_query: types.CallbackQuery):
    await more_category.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['more_back_return'])
async def callback_handler_3(callback_query: types.CallbackQuery):
    await more_category.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith(('forward-enter', 'back-enter', 'amount-sum', 'amount-min', 'product-choose-enter')))
async def callback_handler_4(callback_query: types.CallbackQuery):
    cur_img_indx = int(callback_query.data.split('_')[1])
    cur_img_cap = int(callback_query.data.split('_')[2])
    await photo_hendler_two.process_callback(bot, callback_query, cur_img_indx, cur_img_cap, db)

# @dp.callback_query_handler(lambda c: c.data in ['choose_enter', 'amount_sum', 'amount_min', 'back-enter'])
# async def callback_handler_4(callback_query: types.CallbackQuery):
#     await photo_hendler_two.process_callback(bot, callback_query)

# @dp.callback_query_handler(lambda c: c.data in ['choose_enter_1', 'amount_sum_1', 'amount_min_1', 'set_amount'])
# async def callback_handler_4(callback_query: types.CallbackQuery, state: FSMContext):
#     await find_articul.process_callback(bot, callback_query, state)

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
        print(f"pre_checkout_q.id: {pre_checkout_q.id}")
    except Exception as e:
        print(f"Pay error: {e}")


@dp.message_handler(content_types = ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    user_id = message.from_user.id
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()
    conn.close()

    orders_info = ''
    item_number = 1


    id_order = random.randint(1000,2000)
    order_info = f"*Платеж прошел успешно*\nЗаказ номер {id_order}:\n"
    for item in orders:
        print(item)
        selected_category = item[5]
        order_info += f"*Товар:* {item[0]}\nАртикул: {item[1]}\nКатегория: {selected_category}\nВариант: {item[2]}\nКоличество: {item[3]}\n\n"


    for item in orders:
        print(item)
        amount_price_1 = item[3] * item[4]
        database.set_user_order(user_id, id_order, item[0], item[1], item[2], item[3], amount_price_1)
        database.update_status_order(id_order, status = 'Создан')
    await bot.send_message(user_id,f"{order_info}",parse_mode = 'Markdown')

    current_order_number = database.get_user_order_order_id(id_order)
    orders_info += f"*Заказ: {current_order_number[0]}*\n"
    orders_info = f"*Детали заказа {id_order}*\n"
    for order in current_order_number:
            # all_price = order[4]
            orders_info += f"Товар: {order[0]}\n" \
                           f"Артикул: {order[1]}\n" \
                           f"Вариант: {order[2]}\n" \
                           f"Кол-во: {order[3]}\n\n"
            item_number += 1

    orders_info += f"Статус заказа: Создан\n"
    await bot.send_message(config.ID_ADMIN, f"*🛑ВНИМАНИЕ🛑*\n*Создан новый заказ {id_order}*", parse_mode = 'Markdown')

    await corsina.clear_user_cart(user_id)


@dp.callback_query_handler(lambda c: c.data.startswith('category'))
async def handle_category_choice(callback_query: types.CallbackQuery):
    category = callback_query.data.split('_')[1]
    await show_category_products(bot, callback_query.message.chat.id, category)

@dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditSum"))
async def handle_category_choice(callback_query: types.CallbackQuery):
    corzinaEdit = callback_query.data.split('_')[1]
    await corsina.edit_cart_amount_Sum(bot, callback_query, corzinaEdit)


@dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditMin"))
async def handle_category_choice(callback_query: types.CallbackQuery):
    corzinaEdit = callback_query.data.split('_')[1]
    await corsina.edit_cart_amount_Min(bot, callback_query, corzinaEdit)

@dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditDel"))
async def handle_category_choice(callback_query: types.CallbackQuery):
    corzinaEdit = callback_query.data.split('_')[1]
    await corsina.edit_cart_Delete(bot, callback_query, corzinaEdit)

if __name__ == '__main__':
    try:
        # logger.info(f"\nSTATUS: Бот запущен.\n")
        executor.start_polling(dp,skip_updates = True)
    except Exception as e:
        # logger.error(f"\nERROR: {e}\n")
        print(e)
#
