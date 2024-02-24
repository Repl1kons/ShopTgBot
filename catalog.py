import find_articul
from photo_handler import start_send_photo
from aiogram import types
from keyboards.Inline import Inline_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class ArticulForm(StatesGroup):
    articul_numb = State()

async def handle_catalog_button(bot, chat_id):
    global messageid
    messageid = (await bot.send_message(chat_id, "Выберите категорию товаров", reply_markup = Inline_keyboard.show_catalogs)).message_id

async def get_articul(bot, message, state: FSMContext):


    user_id = message.from_user.id
    articul_numb = message.text.strip()
    if not articul_numb.isdigit():
        await message.answer("Пожалуйста, введите корректный артикул.")
        return

    # await bot.delete_message(message.from_user.id, message_id2)
    await state.get_state(ArticulForm.articul_numb)
    await state.finish()
    await find_articul.start_articul(bot,message.from_user.id,articul_numb)

async def show_category_products(bot, chat_id, category):
    global messageid
    if category == "📔 Ежедневники":
        path = "planers/categor"
        await bot.delete_message(chat_id,messageid)
        await start_send_photo(bot, chat_id, path)


    if category == "🖼 Обложки":
        path = "covers/categor"
        await bot.delete_message(chat_id,messageid)
        await start_send_photo(bot, chat_id, path)

    if category == "💳 Кард-холдеры":
        path = "cardholder/categor"
        await bot.delete_message(chat_id,messageid)
        await start_send_photo(bot, chat_id, path)

    if category == '🔍 Поиск артикула':
        global message_id2
        await bot.delete_message(chat_id, messageid)
        await ArticulForm.articul_numb.set()
        message_id2 = (await bot.send_message(chat_id, "Введите номер артикула")).message_id
