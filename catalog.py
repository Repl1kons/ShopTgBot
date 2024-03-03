import find_articul
from photo_handler import send_photo
from aiogram import types
from keyboards.Inline import Inline_keyboard


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class ArticulForm(StatesGroup):
    articul_numb = State()

async def handle_catalog_button(bot, chat_id):
    await bot.send_message(chat_id, "Выберите категорию товаров", reply_markup = Inline_keyboard.show_catalogs)

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

async def show_category_products(bot, callback_query: types.CallbackQuery, category):
    if category == "📔 Ежедневники":
        product = "categoryPlaners"
        await callback_query.message.delete()
        await send_photo(bot, callback_query, product)


    if category == "🖼 Обложки":
        product = "categoryCovers"
        await callback_query.message.delete()
        await send_photo(bot,callback_query,product)

    if category == "💳 Кард-холдеры":
        product = "categoryCardholder"
        await callback_query.message.delete()
        await send_photo(bot,callback_query,product)

    # if category == '🔍 Поиск артикула':
    #     await bot.delete_message(chat_id, messageid)
    #     await ArticulForm.articul_numb.set()
    #     message_id2 = (await bot.send_message(chat_id, "Введите номер артикула")).message_id
