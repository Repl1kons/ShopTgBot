import sqlite3
import more_category
import profil_register
from data.db import database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import config
import corsina
from catalog import handle_catalog_button, show_category_products  # Импортируем новый обработчик
import photo_handler
import photo_hendler_two
from aiogram.types import ContentTypes
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
    ASK_INDECS = State()
    CONFIRMATION = State()


storage = MemoryStorage()
bot = Bot(token = config.BOT_TOKEN)
dp = Dispatcher(bot, storage = storage)


@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    welcome_message = \
        f"*🎉 Здравствуй, {message.from_user.first_name}!*\n\n" \
        f"Я - *твой личный шопинг-бот* 🛍️.\nВот что я могу предложить:\n\n" \
        f"- ✒️ *Уникальные обложки*\n" \
        f"- 📘 *Стильные ежедневники*\n" \
        f"- 🌟 *И многое другое*\n\n" \
        f"*Создано специально для it's my planner | by A-STUDENT!*"
    await bot.send_message(message.chat.id, welcome_message, reply_markup = Markup_keyboards.main_menu,
                           parse_mode = 'Markdown')


@dp.message_handler(lambda message: message.text in ['🆘 Помощь', '/help'])
async def handle_help(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Если у вас есть вопросы по поводу работе бота или другая информация - напишите нам\n https://t.me/Garnlzerx")


@dp.message_handler(lambda message: message.text == "👨Профиль")
async def profil_user(message: types.Message):
    user_id = message.from_user.id
    user_data = database.get_user_data(user_id)

    if user_data:
        full_name = user_data[0].split(' ')
        first_name = full_name[1]
        last_name = full_name[0]
        surname = full_name[2]
        await bot.send_message(
            message.from_user.id,
            text = (f"🙍 <b>Профиль пользователя:</b>\n"
                    f"🆔 <i>ID:</i> {user_id}\n"
                    f"👤 <i>Никнейм:</i> {message.from_user.username}\n\n"
                    f"👤 <b>Имя пользователя:</b>\n"
                    f"┌ <i>Фамилия:</i> {last_name}\n"
                    f"├ <i>Имя:</i> {first_name}\n"
                    f"└ <i>Отчество:</i> {surname}\n\n"
                    f"🏠 <b>Адрес:</b>\n"
                    f"┌ <i>Область:</i> {user_data[2]}\n"
                    f"├ <i>Город:</i> {user_data[1]}\n"
                    f"├ <i>Улица:</i> {user_data[3]}\n"
                    f"├ <i>Дом:</i> {user_data[4]}\n"
                    f"└ <i>Индекс:</i> {user_data[5]}\n"),

            reply_markup = Inline_keyboard.profil_data_1,  # Передал в отдельную строку для ясности
            parse_mode = 'HTML')




    else:
        await bot.send_message(user_id,
                               f"Здравствуйте {message.from_user.username} 👋\nВ данный момент вы не зарегистрированы в боте. Вы можете начать регистрироваться сейчас.",
                               reply_markup = Inline_keyboard.not_profil_data)


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
                               f"Индекс: {profil_data['indecs']}",
                               reply_markup = Inline_keyboard.user_data_1)


@dp.callback_query_handler(lambda c: c.data == 'change_data_1', state = '*')
async def change_data(callback_query: types.CallbackQuery):
    database.delete_user(callback_query.from_user.id)
    await profil_register.process_callback(bot, callback_query, State)


@dp.callback_query_handler(lambda c: c.data == 'return_profile')
async def return_on_profile(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await handle_catalog_button(bot, callback_query.from_user.id)


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
    message_id = (await bot.send_message(message.from_user.id, "Введите ваше имя в формате ФИО:")).message_id


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

@dp.callback_query_handler(lambda c: c.data in ['clear_cart', "pay_cont", "edit_cart", "show_basket"], state = '*')
async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await corsina.process_callback(bot, callback_query, state)


@dp.callback_query_handler(lambda c: c.data == 'payment')
async def start_payment_process(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = database.get_user_data(user_id)
    if user_data:
        await bot.send_message(
            callback_query.from_user.id,
            text = f"*Ваши текущие данные:*\n\n*Имя:*\n{user_data[0]}\n\n*Адрес:*\n{user_data[2]} обл., г.{user_data[1]}, ул.{user_data[3]},{user_data[4]}\nИндекс: {user_data[5]}",
            reply_markup = Inline_keyboard.confirmation_keyboard,
            parse_mode = 'Markdown'
        )

    else:
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО: ")).message_id


@dp.callback_query_handler(lambda c: c.data == 'change_data', state = '*')
async def change_data(callback_query: types.CallbackQuery, state: FSMContext):
    print("Обработчик change_data вызван")  # Для отладки
    try:
        database.delete_user(callback_query.from_user.id)
        await PaymentState.ASK_NAME.set()
        global message_id
        message_id = (await bot.send_message(callback_query.from_user.id, "Введите ваше имя в формате ФИО: ")).message_id
    except Exception as e:
        print(f"Ошибка: {e}")


@dp.callback_query_handler(lambda c: c.data == 'confirm_data', state = '*')
async def confirm_data(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_id = callback_query.from_user.id
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()

    query = "SELECT item_name, articul, selected_variant, quantity, price FROM cart_items WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()

    # Форматирование данных корзины для пользователя
    total_price = 0
    for item in cart_items:
        total_price += int(item[3] * item[4])  # Главное не забыть убрать -800
    total_price = total_price
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


@dp.message_handler(state = corsina.CartEditState.awaiting_item_number)
async def edit_cart(message: types.Message, state: FSMContext):
    async with state.proxy() as data_ed:
        data_ed["item_number"] = message.text
        await corsina.item_number_received(bot, message, state)


@dp.message_handler(state = PaymentState.ASK_NAME)
async def process_name(message: types.Message, state: FSMContext):
    global message_id
    async with state.proxy() as data:
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


# Обработчик для состояния ASK_STREET
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
                                       f"\n\nИмя: {data['name']}\nОбласть: {data['region']}\nГород: {data['city']}\nУлица: {data['street']}\nДом: {data['house']}\nИндекс: {data['indecs']}",
                                reply_markup = Inline_keyboard.user_data)
    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)


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
            indecs = data['indecs']
        )

    await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id = message_id,
                                text = "Отлично теперь нажмите на кнопку оплаты: ")
    await bot.delete_message(chat_id = callback_query.message.chat.id, message_id = callback_query.message.message_id)

    await state.finish()

    conn = sqlite3.connect('data/bot_database.db')
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


@dp.callback_query_handler(lambda c: c.data in ['back', 'forward', 'choose_enter_categorical', 'more'])
async def callback_handler_2(callback_query: types.CallbackQuery):
    await photo_handler.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['back_1', 'forward_1', 'back_return_1'])
async def callback_handler_2(callback_query: types.CallbackQuery):
    await more_category.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['more_back_return'])
async def callback_handler_3(callback_query: types.CallbackQuery):
    await more_category.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['back-enter', 'forward-enter', 'choose_enter', 'amount_sum', 'amount_min', 'back_to_choose'])
async def callback_handler_4(callback_query: types.CallbackQuery):
    await photo_hendler_two.process_callback(bot, callback_query)


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
    except Exception as e:
        print(f"Pay error: {e}")


@dp.message_handler(content_types = ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    user_id = message.from_user.id
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")


    user_data = database.get_user_data(user_id)
    if user_data:
        user_info = f"*Данные пользователя:*\nИмя: {user_data[0]}\nОбласть: {user_data[2]}\nГород: {user_data[1]}\nУлица: {user_data[3]}\nДом: {user_data[4]}\nИндекс: {user_data[5]}"
    else:
        user_info = "Информация о пользователе не найдена."

    # Извлечение данных о заказе
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, articul, selected_variant, quantity, price, selected_category FROM cart_items WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()
    conn.close()

    if user_id == 1066300592:

        order_info = "*Детали заказа:*\n"
        for item in orders:
            print(item)
            amount_price_1 = item[3] * item[4]
            selected_category = item[5]
            order_info += f"*Товар:* {item[0]}\nАртикул: {item[1]}\nКатегория: {selected_category}\nВариант: {item[2]}\nКоличество: {item[3]}\nОбщая стоимость заказа: {amount_price_1}\n\n"

        # Отправка информации пользователю
        await bot.send_message(user_id, f"{user_info}\n\n{order_info}", parse_mode = 'Markdown')
    else:
        order_info = "*Платеж прошел успешно*\n"
        for item in orders:
            print(item)
            amount_price_1 = item[3] * item[4]
            selected_category = item[5]
            order_info += f"`Заказ`\n\n*Товар:* {item[0]}\nАртикул: {item[1]}\nКатегория: {selected_category}\nВариант: {item[2]}\nКоличество: {item[3]}\nОбщая стоимость заказа: {amount_price_1}\n\n"

        # Отправка информации пользователю
        await bot.send_message(user_id, f"{order_info}", parse_mode = 'Markdown')

    # Очистка корзины пользователя
    await corsina.clear_user_cart(user_id)


@dp.callback_query_handler(lambda c: c.data.startswith('category'))
async def handle_category_choice(callback_query: types.CallbackQuery):
    category = callback_query.data.split('_')[1]
    await show_category_products(bot, callback_query.message.chat.id, category)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
