from data.db import database
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.Inline import Inline_keyboard


class ProfilState(StatesGroup):
    GET_NAME = State()
    GET_REGION = State()
    GET_CITY = State()
    GET_STREET = State()
    GET_HOUSE = State()
    GET_APARTMENT = State()
    GET_INDECS = State()
    CONFIRMATION = State()


async def get_name(bot, message, state: FSMContext):
    user_id = message.from_user.id


    name = message.text.strip()
    # await bot.send_message(user_id, f'Имя {name}')
    if len(name.split()) == 3:
        await state.get_state(ProfilState.GET_NAME)
        await ProfilState.next()
        await bot.edit_message_text(chat_id = user_id, message_id = message_id, text = "Теперь введите область:")
    else:
        await ProfilState.GET_NAME.set()
        # await bot.send_message(chat_id = user_id, text = "Введите свое имя в формате ФИО:")
    # await bot.delete_message(chat_id = message.chat.id,message_id = message.message_id)

    # await bot.delete_message(chat_id = message.from_user.id,message_id = message.message_id)


async def get_region(bot, message, state: FSMContext):
    user_id = message.from_user.id
    region = message.text.strip()
    # await bot.send_message(user_id, f'Регион {region}')
    await state.get_state(ProfilState.GET_REGION)
    await ProfilState.next()
    await bot.edit_message_text(chat_id = user_id, message_id = message_id, text = "Теперь введите город:")


async def get_city(bot, message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text.strip()
    # await bot.send_message(user_id, f'Город {city}')
    await state.get_state(ProfilState.GET_CITY)
    await ProfilState.next()
    await bot.edit_message_text(chat_id = user_id, message_id = message_id, text = "Теперь введите улицу:")

async def get_street(bot, message, state: FSMContext):
    user_id = message.from_user.id
    street = message.text.strip()
    # await bot.send_message(user_id, f'улица {street}')
    await state.get_state(ProfilState.GET_STREET)
    await ProfilState.next()
    await bot.edit_message_text(chat_id = user_id, message_id = message_id, text = "Теперь введите дом:")



async def get_house_numb(bot, message, state: FSMContext):
    user_id = message.from_user.id

    await state.get_state(ProfilState.GET_APARTMENT)
    await ProfilState.next()
    await bot.edit_message_text(chat_id = user_id, message_id = message_id, text = "Теперь введите квартиру:")

async def get_apartment(bot,message,state: FSMContext):
    user_id = message.from_user.id
    await state.get_state(ProfilState.GET_HOUSE)
    await ProfilState.next()
    await bot.edit_message_text(chat_id = user_id,message_id = message_id,text = "Теперь введите индекс:")

async def get_indecs(bot, message, state: FSMContext):
    user_id = message.from_user.id
    house = message.text.strip()
    # await bot.send_message(user_id,f'Дом {house}')
    await state.get_state(ProfilState.GET_INDECS)
    await ProfilState.next()

async def conf(bot, message, state: FSMContext, db):
    async with state.proxy() as data:
        await database.add_user(
            user_id = message.from_user.id,
            name = data['name'],
            city = data['city'],
            region = data['region'],
            street = data['street'],
            number_house = data['house'],
            apartment = data['apartment'],
            indecs = data['indecs'],
            db = db)

    print(message.from_user.id)
    user_id = message.from_user.id
    user_data = await db.User.find_one({'_id': message.from_user.id})

    full_name = user_data['data']['name'].split(' ')
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
                f"┌ <i>Область:</i> {user_data['data']['region']}\n"
                f"├ <i>Город:</i> {user_data['data']['city']}\n"
                f"├ <i>Улица:</i> {user_data['data']['street']}\n"
                f"├ <i>Дом:</i> {user_data['data']['number_house']}\n"
                f"├ <i>Квартира:</i> {user_data['data']['apartment']}\n"
                f"└ <i>Индекс:</i> {user_data['data']['indecs']}\n"),
        reply_markup = Inline_keyboard.profil_data_1,
        parse_mode = 'HTML'
    )


    await state.finish()

async def process_callback(bot, callback_query: types.CallbackQuery, state: FSMContext):
    global message_id

    user_id = callback_query.from_user.id

    if callback_query.data == 'create_data_profil':
        await ProfilState.GET_NAME.set()
        # await bot.delete_message(user_id, callback_query.message.message_id)
        message_id = (await bot.send_message(user_id, "Введите свое имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")).message_id

    if callback_query.data == 'change_data_1':
        await ProfilState.GET_NAME.set()
        message_id = (await bot.send_message(user_id, "Введите свое имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")).message_id

    if callback_query.data == 'data-edit_1':
        await ProfilState.GET_NAME.set()
        message_id = (await bot.send_message(user_id, "Введите свое имя в формате ФИО:\nАккуратней, я очень чувствителен к формату")).message_id