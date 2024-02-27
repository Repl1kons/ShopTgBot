import asyncio
import logging
import random
from contextlib import suppress
import catalog
import find_articul
import more_category
import profil_register
from data.db import database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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


sheduler = AsyncIOScheduler(timezone='Europe/Moscow')

class PaymentState(StatesGroup):
    ASK_NAME = State()
    ASK_REGION = State()
    ASK_CITY = State()
    ASK_STREET = State()
    ASK_HOUSE = State()
    ASK_APARTMENT = State()
    ASK_INDECS = State()
    CONFIRMATION = State()





async def start_bot():
    storage = MemoryStorage()
    bot = Bot(token = config.BOT_TOKEN)
    dp = Dispatcher(bot,storage = storage)
    cluster = AsyncIOMotorClient(host = 'localhost:27017')
    db = cluster.ShopTgBot

    dp.message_handler(commands = ['start'])(lambda message: send_welcome(message, bot, db))
    dp.message_handler(commands = ['status'])(lambda message: status_command(message, bot))
    dp.message_handler(lambda message: message.text in ['🆘 Помощь', '/help'])(lambda message: command_help(message, bot))
    dp.message_handler(lambda message: message.text == "👨Профиль")(lambda message: profil_user(message, bot, db))
    dp.callback_query_handler(lambda c: c.data == 'create_data_profil')(lambda call, state=FSMContext: create_profil(bot, call, state))
    dp.message_handler(state = profil_register.ProfilState.GET_NAME)(lambda message, state=FSMContext: start_profile_name(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_REGION)(lambda message, state=FSMContext: start_profile_region(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_CITY)(lambda message, state=FSMContext: start_profile_city(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_STREET)(lambda message, state=FSMContext: start_profile_street(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_HOUSE)(lambda message, state=FSMContext: start_profile_house(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_APARTMENT)(lambda message, state=FSMContext: start_profile_appartment(bot, message, state))
    dp.message_handler(state = profil_register.ProfilState.GET_INDECS)(lambda message, state=FSMContext: start_profile_indecs(bot, message, state))
    dp.callback_query_handler(lambda c: c.data == 'change_data_1',state = '*')(lambda call, state=FSMContext: change_data(call, bot, state))
    dp.callback_query_handler(lambda c: c.data == 'returnProfil')(lambda call: return_on_profile(call, bot, db))
    dp.callback_query_handler(lambda c: c.data == 'data-enter_1',state = profil_register.ProfilState.CONFIRMATION)(lambda call, state=FSMContext: process_data_enter(call, state, bot, db))
    dp.callback_query_handler(lambda c: c.data == 'data-edit_1', state = profil_register.ProfilState.CONFIRMATION)(lambda call, state=FSMContext: process_data_edit(call, state, bot))
    dp.callback_query_handler(lambda c: c.data == 'create_data')(lambda call: create_info_user(bot, call))
    dp.callback_query_handler(lambda c: c.data == 'back_return')(lambda call: back_return(bot, call))
    dp.message_handler(lambda message: message.text == '🛍 Каталог')(lambda message: handle_catalog_1(bot, message))
    dp.message_handler(lambda message: message.text == '🛒 Корзина')(lambda message: handle_corsina(bot, message, db))
    dp.callback_query_handler(lambda c: c.data == 'show_basket_1')(lambda call: show_basket(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditSum"))(lambda call: handle_corzina_sum(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditMin"))(lambda call: handle_corzina_min(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith("corzinaEditDel"))(lambda call: handle_corzina_del(call, bot, db))
    dp.callback_query_handler(lambda c: c.data in ['clear_cart',"pay_cont","edit_cart","show_basket"])(lambda call: callback_handler_corsina(bot, call, db))
    dp.message_handler(state = find_articul.SetAmount.new_amount)(lambda message, state=FSMContext: edit_cart(message, state, bot))
    dp.callback_query_handler(lambda c: c.data == 'payment')(lambda call: start_payment_process(call, bot, db))
    dp.callback_query_handler(lambda c: c.data == 'change_data',state = '*')(lambda call, state=FSMContext: change_data_state(call, state, bot))
    dp.callback_query_handler(lambda c: c.data == 'confirm_data',state = '*')(lambda call, state=FSMContext: confirm_data(call, state, bot, db))
    dp.message_handler(state = PaymentState.ASK_NAME)(lambda message, state=FSMContext: process_name(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_REGION)(lambda message, state=FSMContext: process_region(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_CITY)(lambda message, state=FSMContext: process_city(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_STREET)(lambda message, state=FSMContext: process_street(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_HOUSE)(lambda message, state=FSMContext: process_house(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_APARTMENT)(lambda message, state=FSMContext: process_appoortm(message, state, bot))
    dp.message_handler(state = PaymentState.ASK_INDECS)(lambda message, state=FSMContext: process_indx(message, state, bot))
    dp.callback_query_handler(lambda c: c.data == 'data-enter',state = PaymentState.CONFIRMATION)((lambda call, state=FSMContext: process_data_enter_state(call, state, bot, db)))
    dp.callback_query_handler(lambda c: c.data == 'data-edit',state = PaymentState.CONFIRMATION)((lambda call, state=FSMContext: process_data_edit_state(call, state)))
    dp.callback_query_handler(lambda c: c.data.startswith('back_to_choose'))(lambda call: callback_handler_back_categor(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith(('categoryBack','categoryForward','choose-enter-categorical','categoryMore')))(lambda call: callback_handler_categor(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith(('move_more_back', 'move_more_forward', 'choose_enter_categorical', 'more_back_return')))(lambda call: callback_handler_more(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith(('forward-enter', 'back-enter', 'amount-sum', 'amount-min', 'product-choose-enter', 'back-to-choose')))(lambda call: callback_handler_product(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith('category'))(lambda call: handle_category_choice(call, bot))
    dp.message_handler(state = catalog.ArticulForm.articul_numb)(lambda message, state=FSMContext: handle_find_art(message, state, db))
    dp.callback_query_handler(lambda c: c.data in ['myOrder','return_order'])(lambda call: my_order(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith('order'))(lambda call: handle_order(call, bot, db))
    dp.callback_query_handler(lambda c: c.data == 'return_order')(lambda call: return_on_order(call, bot, db))
    dp.callback_query_handler(lambda c: c.data.startswith('set_status'))(lambda call: callback_set_status(call, bot))
    dp.callback_query_handler(lambda c: c.data.startswith("editStatus"))(lambda call: callback_edit_status(call, bot, db))

    dp.register_pre_checkout_query_handler(lambda pre_checkout_q=types.PreCheckoutQuery: pre_checkout_query(pre_checkout_q, bot))
    dp.register_message_handler(lambda message: successful_payment(message,bot,db), content_types = types.ContentTypes.SUCCESSFUL_PAYMENT)
    dp.register_errors_handler(error_handler)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def send_welcome(message: types.Message, bot: Bot, db):
    start_param = message.get_args()
    print(start_param)

    user_data = await db.User.find_one({'_id': message.from_user.id})
    if user_data:
        welcome_message = \
            f"*🎉 С возращением, {message.from_user.first_name}!*\n\n" \
            f"Я - *твой личный шопинг-бот* 🛍️.\nВот что я могу предложить:\n\n" \
            f"- ✒️ *Уникальные обложки*\n" \
            f"- 📘 *Стильные ежедневники*\n" \
            f"- 🌟 *И многое другое*\n\n" \
            f"*Создано специально для it's my planner | by A-STUDENT!*"
    else:
        with suppress(DuplicateKeyError):
            await db.User.insert_one(dict(
                _id = message.from_user.id,
                data = {
                    'name': '',
                    'city': '',
                    'region': '',
                    'street': '',
                    'number_house': '',
                    'apartment': '',
                    'indecs': '',
                    'phone': '',
                    'email': ''
                }
            ))

            await db.State.insert_one(dict(
                _id = message.from_user.id,
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

            await db.Corsina.insert_one(dict(
                _id = message.from_user.id,
                data = []
            ))

            await message.answer("Вы успешно зарегистрированы в базе данных.")

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
    # if start_param.isdigit():
    #     await find_articul.start_articul(bot,message.chat.id,start_param)

async def command_help(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id,
                           "Если у вас есть вопросы по поводу работе бота или другая информация - напишите нам\n https://t.me/Garnlzerx")

async def my_order(callback_query: types.CallbackQuery, bot: Bot, db):
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

    if callback_query.from_user.id == config.ID_ADMIN:
        user_order_data = await db.Order.find({}).to_list(length = None)
    else:
        user_order_data = await db.Order.find({'user_id': callback_query.from_user.id}).to_list(length = None)

    if user_order_data:
        current_order_number = None
        show_order = InlineKeyboardMarkup(row_width = 1)
        for order in user_order_data:
            order_id = int(order['order_id'])
            if order_id != current_order_number:
                order_button = InlineKeyboardButton(text = order_id,callback_data = f"order_{order_id}")
                show_order.add(order_button)
                current_order_number = order_id
    else:
        show_order = None

    message_text = (
        "*Выберите номер заказа для просмотра*\n\n"
        if user_order_data
        else "Похоже вы еще не сделали ни одного заказа🤨"
    )

    returnProfilButton = InlineKeyboardButton(text = 'Назад',callback_data = 'returnProfil')
    if show_order:
        show_order.add(returnProfilButton)
    else:
        show_order = InlineKeyboardMarkup().add(returnProfilButton)

    await bot.send_message(
        callback_query.from_user.id,
        text = message_text,
        parse_mode = 'Markdown',
        reply_markup = show_order
    )
    await callback_query.answer()

async def status_command(message: types.Message, bot: Bot):
    with open("app.log", "rb") as log_file:
        await bot.send_document(message.chat.id, log_file)

async def handle_order(callback_query: types.CallbackQuery, bot: Bot, db):

    text_order_info = ''
    order = int(callback_query.data.split('_')[1])
    text_order_info += f"*Заказ: {order}*\n\n"
    item_number = 1
    show_order = InlineKeyboardMarkup(row_width = 1)

    user_id = None
    status = None
    print(order)
    user_orders = await db.Order.find({'order_id': order}).to_list(length = None)
    print(user_orders)
    for orders in user_orders:
        for product in orders['products']:
            text_order_info += f"{item_number}. Товар: {product['product_name']}\n" \
                               f"Артикул: {product['articul']}\n" \
                               f"Вариант: {product['selected_variant']}\n" \
                               f"Кол-во: {product['quantity']}\n\n"
            item_number += 1

        user_id = orders['user_id']
        status = orders['status']

    user_data = await db.User.find_one({'_id': user_id})
    if callback_query.from_user.id == config.ID_ADMIN:
        if user_data['data']['name']:
            text_order_info += (f"*Данные пользователя:*\n"
                                f"Имя: {user_data['data']['name']}\n"
                                f"Область: {user_data['data']['region']}\n"
                                f"Город: {user_data['data']['city']}\n"
                                f"Улица: {user_data['data']['street']}\n"
                                f"Дом: {user_data['data']['number_house']}\n"
                                f"Квартира: {user_data['data']['apartment']}\n"
                                f"Индекс: {user_data['data']['indecs']}\n\n")
        text_order_info += f"Статус заказа: {status}\n"
        returnOrderButton = InlineKeyboardButton(text = 'Назад',callback_data = 'return_order')
        order_button = InlineKeyboardButton(text = "Установить статус",callback_data = f'set_status_{order}')
        show_order.add(order_button)
        show_order.insert(returnOrderButton)

        await callback_query.message.edit_text(text = text_order_info, parse_mode = 'Markdown', reply_markup = show_order) # Inline_keyboard.returnOrder
    else:
        text_order_info += f"Статус заказа: {status}\n"
        await callback_query.message.edit_text(text = text_order_info, parse_mode = 'Markdown', reply_markup = Inline_keyboard.returnOrder)
    await callback_query.answer()

async def callback_set_status(callback_query: types.CallbackQuery, bot: Bot):
    order = int(callback_query.data.split('_')[2])
    print(order)
    set_status_keyboard = InlineKeyboardMarkup(row_width = 1)
    returnOrderButton = InlineKeyboardButton(text = 'В пути',callback_data = f'editStatus_{order}_Отправлен')
    order_button = InlineKeyboardButton(text = "Доставлен",callback_data = f'editStatus_{order}_Доставлен')
    set_status_keyboard.add(order_button)
    set_status_keyboard.insert(returnOrderButton)
    await bot.send_message(callback_query.from_user.id, f"выберите статус для заказа {order}:", reply_markup = set_status_keyboard)
    await callback_query.answer()

async def callback_edit_status(callback_query: types.CallbackQuery, bot: Bot, db):
    order = int(callback_query.data.split('_')[1])
    status = callback_query.data.split('_')[2]
    await db.Order.update_one(
        {'order_id': order},  # Условие выборки документа для обновления
        {'$set': {'status': status}}
    )
    await bot.send_message(callback_query.from_user.id, f"Статус заказа был изменен на {status}")
    await callback_query.answer()

async def profil_user(message: types.Message, bot: Bot, db):
    user_id = message.from_user.id
    user_data = await db.User.find_one({'_id': message.from_user.id})
    if user_data['data']['name']:
        full_name = user_data['data']['name'].split(' ')
        print(full_name)
        first_name = full_name[1]
        last_name = full_name[0]
        surname = full_name[2]
        text  = (f"🙍 <b>Профиль пользователя:</b>\n"
                f"🆔 <i>ID:</i> {user_id}\n"
                f"👤 <i>Никнейм:</i> {message.from_user.username}\n\n"
                f"👤 <b>Имя пользователя:</b>\n"
                f"┌ <i>Фамилия:</i> {last_name}\n"
                f"├ <i>Имя:</i> {first_name}\n"
                f"└ <i>Отчество:</i> {surname}\n\n"
                f"🏠 <b>Адрес:</b>\n"
                f"┌ <i>Область:</i> {user_data['data']['region']}\n"
                f"├ <i>Город:</i> {user_data['data']['city']}\n"
                f"├ <i>Улица:</i> {user_data['data']['street']}\n"
                f"├ <i>Дом:</i> {user_data['data']['number_house']}\n"
                f"├ <i>Квартира:</i> {user_data['data']['apartment']}\n"
                f"└ <i>Индекс:</i> {user_data['data']['indecs']}\n")

        await bot.send_message(message.from_user.id, text = text, reply_markup = Inline_keyboard.profil_data_1,
        parse_mode = 'HTML')


    else:
        await bot.send_message(user_id,
                               f"Здравствуйте {message.from_user.username} 👋\nВ данный момент вы не зарегистрированы в боте. Вы можете начать регистрироваться сейчас.",
                               reply_markup = Inline_keyboard.not_profil_data)

async def handle_find_art(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as profil_data:
        profil_data["articul"] = message.text
        await catalog.get_articul(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def create_profil(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await profil_register.process_callback(bot, callback_query, state)
    await callback_query.answer()

async def show_basket(callback_query: types.CallbackQuery, bot: Bot, db):
    await corsina.show_cart(bot, callback_query, db)
    await callback_query.answer()
async def start_profile_name(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["name"] = message.text
        await profil_register.get_name(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_region(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["region"] = message.text
        await profil_register.get_region(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_city(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["city"] = message.text
        await profil_register.get_city(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_street(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["street"] = message.text
        await profil_register.get_street(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_house(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["house"] = message.text
        await profil_register.get_house_numb(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_appartment(bot, message: types.Message, state: FSMContext):
    async with state.proxy() as profil_data:
        profil_data["apartment"] = message.text
        await profil_register.get_apartment(bot, message, state)
        await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def start_profile_indecs(bot, message: types.Message, state: FSMContext):
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

async def change_data(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await profil_register.process_callback(bot, callback_query, state)
    await callback_query.answer()

async def return_on_order(callback_query: types.CallbackQuery, bot: Bot, db):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await my_order(callback_query, bot, db)
    await callback_query.answer()

async def return_on_profile(callback_query: types.CallbackQuery, bot, db):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await profil_user(callback_query, bot, db)
    await callback_query.answer()

async def process_data_enter(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot, db):
    await bot.delete_message(chat_id = callback_query.from_user.id, message_id = callback_query.message.message_id)
    await profil_register.conf(bot, callback_query, state, db)
    await callback_query.answer()

async def process_data_edit(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await profil_register.process_callback(bot, callback_query, state)
    await callback_query.answer()

async def create_info_user(bot, callback_query: types.CallbackQuery):
    await PaymentState.ASK_NAME.set()
    await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")

async def handle_catalog_1(bot, message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await handle_catalog_button(bot, message.chat.id)

async def back_return(bot, callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await handle_catalog_button(bot, callback_query.message.chat.id)
    await callback_query.answer()

async def handle_corsina(bot, message: types.Message, db):
    await corsina.show_cart(bot, message, db)

async def callback_handler_corsina(bot, callback_query: types.CallbackQuery, db):
    await corsina.process_callback(bot, callback_query, db)
    await callback_query.answer()

async def start_payment_process(callback_query: types.CallbackQuery, bot: Bot, db):
    user_id = callback_query.from_user.id
    # user_data = database.get_user_data(user_id)
    user_data = await db.User.find_one({'_id': user_id})
    if user_data['data']['name']:
        await bot.send_message(
            callback_query.from_user.id,
            text = f"*Ваши текущие данные:*\n\n"
                   f"*Имя:*\n{user_data['data']['name']}\n\n"
                   f"*Адрес:*\n{user_data['data']['region']} обл., г.{user_data['data']['city']}, ул.{user_data['data']['street']},{user_data['data']['number_house']}., {user_data['data']['apartment']}\nИндекс: {user_data['data']['indecs']}",
            reply_markup = Inline_keyboard.confirmation_keyboard,
            parse_mode = 'Markdown'
        )

    else:
        await PaymentState.ASK_NAME.set()
        await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату ")
    await callback_query.answer()

async def change_data_state(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    try:
        # database.delete_user(callback_query.from_user.id)
        await PaymentState.ASK_NAME.set()
        await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")
    except Exception as e:
        print(f"Ошибка: {e}")
    await callback_query.answer()

async def confirm_data(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot, db):
    await state.finish()
    user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
    user_corsina_data = user_corsina['data']
    total_price = 0

    for order in user_corsina_data:
        amount = int(order['quantity'])
        price = int(order['price'])
        total_price += int(price * amount)
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
    await callback_query.answer()

async def edit_cart(message: types.Message, state: FSMContext, bot):
    async with state.proxy() as data_amount:
        data_amount["new_amount"] = message.text
        await find_articul.set_amount_art(bot, message, state)

async def process_name(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        if len(message.text.split()) == 3:
            data['name'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "Теперь введите область:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_region(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['region'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "Введите пожалуйста город в котором вы живете:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_city(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['city'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "Отлично, осталось совсем чуть-чуть, теперь введите название вашей улицы:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_street(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['street'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "Введите номер вашего дома:")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_house(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['house'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "Теперь введите номер квартиры")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_appoortm(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['apartment'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = "И наконец, введите индекс")
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_indx(message: types.Message, state: FSMContext, bot: Bot):
    async with state.proxy() as data:
        data['indecs'] = message.text
    await PaymentState.next()
    await bot.send_message(message.from_user.id, text = f"Пожалуйста, подтвердите введенные данные."
                                       f"\n\nИмя: {data['name']}\nОбласть: {data['region']}\nГород: {data['city']}\nУлица: {data['street']}\nДом: {data['house']}\nКвартира: {data['apartment']}\nИндекс: {data['indecs']}",
                                reply_markup = Inline_keyboard.user_data)
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)

async def process_data_enter_state(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot, db):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        await database.add_user(
            user_id = user_id,
            name = data['name'],
            city = data['city'],
            region = data['region'],
            street = data['street'],
            number_house = data['house'],
            apartment = data['apartment'],
            indecs = data['indecs'],
            db=db)





    await callback_query.message.edit_text(text = "Отлично теперь нажмите на кнопку оплаты: ")
    await bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id)

    await state.finish()

    user_corsina = await db.Corsina.find_one({'_id': callback_query.from_user.id})
    user_corsina_data = user_corsina['data']

    total_price = 0

    for order in user_corsina_data:
        amount = int(order['quantity'])
        price = int(order['price'])
        total_price += int(price * amount)

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

    await callback_query.answer()

async def process_data_edit_state(callback_query: types.CallbackQuery, state: FSMContext):
    await PaymentState.ASK_NAME.set()
    await callback_query.message.edit_text(text = "Опрос начинается заново. Введите ваше имя в формате ФИО: ")
    await callback_query.answer()

async def callback_handler_back_categor(callback_query: types.CallbackQuery, bot: Bot, db):
    product = callback_query.data.split('_')[1]
    cur_img_indx = int(callback_query.data.split('_')[2])
    cur_img_capt = int(callback_query.data.split('_')[3])
    await photo_handler.process_callback(bot, callback_query, cur_img_indx, cur_img_capt, product, db)
    await callback_query.answer()

async def callback_handler_categor(callback_query: types.CallbackQuery, bot: Bot, db):
    product = callback_query.data.split('_')[1]
    cur_img_indx = int(callback_query.data.split('_')[2])
    cur_img_capt = int(callback_query.data.split('_')[3])
    await photo_handler.process_callback(bot, callback_query, cur_img_indx, cur_img_capt, product, db)
    await callback_query.answer()

async def callback_handler_more(callback_query: types.CallbackQuery, bot: Bot, db):
    cur_img_indx = int(callback_query.data.split('_')[3])
    print(cur_img_indx)
    await more_category.process_callback(bot, callback_query, cur_img_indx, db)
    await callback_query.answer()

async def callback_handler_product(callback_query: types.CallbackQuery, bot: Bot, db):
    cur_img_indx = int(callback_query.data.split('_')[1])
    cur_img_cap = int(callback_query.data.split('_')[2])

    await photo_hendler_two.process_callback(bot, callback_query, cur_img_indx, cur_img_cap, db)
    await callback_query.answer()

async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, bot: Bot):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
        print(f"pre_checkout_q.id: {pre_checkout_q.id}")
    except Exception as e:
        print(f"Pay error: {e}")

async def successful_payment(message: types.Message, bot: Bot, db):
    user_id = message.from_user.id
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    user_corsina = await db.Corsina.find_one({'_id': user_id})
    user_corsina_data = user_corsina['data']

    id_order = random.randint(1000,2000)
    order_info = f"*Платеж прошел успешно*\nЗаказ номер {id_order}:\n"
    orders_list = []

    for order in user_corsina_data:
        selected_category = order['selected_category']
        order_info += (f"*Товар:* {order['product_name']}\n"
                       f"Артикул: {order['articul']}\n"
                       f"Категория: {selected_category}\n"
                       f"Вариант: {order['selected_variant']}\n"
                       f"Количество: {order['quantity']}\n\n")

        amount_price_1 = order['price'] * order['quantity']

        # Создаем словарь для каждого продукта в заказе
        product_data = {
            'product_name': order['product_name'],
            'articul': order['articul'],
            'selected_variant': order['selected_variant'],
            'quantity': order['quantity'],
            'price': order['price'],
        }
        # Добавляем словарь продукта в список заказов
        orders_list.append(product_data)

    # Вставляем все заказы одним запросом
    await db.Order.insert_many([
        {
            'order_id': id_order,
            'user_id': message.from_user.id,
            'status': 'Создан',
            'products': orders_list
        }
    ])
    item_number = 0
    orders_info = ''
    await bot.send_message(user_id,f"{order_info}",parse_mode = 'Markdown')

    user_order = await db.Order.find_one({'order_id': id_order})
    print(user_order)
    user_order_data = user_order['products']

    for order in user_order_data:
        orders_info += f"*Заказ: {id_order}*\n"
        orders_info = f"*Детали заказа {id_order}*\n"

        orders_info += f"Товар: {order['product_name']}\n" \
                       f"Артикул: {order['articul']}\n" \
                       f"Вариант: {order['selected_variant']}\n" \
                       f"Кол-во: {order['quantity']}\n\n"
        item_number += 1

    orders_info += f"Статус заказа: Создан\n"
    await bot.send_message(config.ID_ADMIN, f"*🛑ВНИМАНИЕ🛑*\n*Создан новый заказ {id_order}*", parse_mode = 'Markdown')

    await db.Corsina.update_one(
        {'_id': user_id},
        {'$set': {'data': []}}
    )

async def handle_category_choice(callback_query: types.CallbackQuery, bot: Bot):
    category = callback_query.data.split('_')[1]
    await show_category_products(bot, callback_query.message.chat.id, category)
    await callback_query.answer()

async def handle_corzina_sum(callback_query: types.CallbackQuery, bot: Bot, db):
    corzinaEdit = callback_query.data.split('_')[1]
    print(corzinaEdit)
    await corsina.edit_cart_amount_Sum(bot, callback_query, corzinaEdit, db)
    await callback_query.answer()

async def handle_corzina_min(callback_query: types.CallbackQuery, bot: Bot, db):
    corzinaEdit = callback_query.data.split('_')[1]
    await corsina.edit_cart_amount_Min(bot, callback_query, corzinaEdit, db)
    await callback_query.answer()

async def handle_corzina_del(callback_query: types.CallbackQuery, bot: Bot, db):
    corzinaEdit = callback_query.data.split('_')[1]
    await corsina.edit_cart_Delete(bot, callback_query, corzinaEdit, db)
    await callback_query.answer()

async def error_handler(update: types.Update, exception):
    print("An error occurred while processing an update:")
    print(exception)


if __name__ == '__main__':
    asyncio.run(start_bot())

