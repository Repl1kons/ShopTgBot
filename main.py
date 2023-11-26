from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import config
import corsina
from catalog import handle_catalog_button, show_category_products  # Импортируем новый обработчик
import photo_handler
import photo_hendler_two
from aiogram.types import ContentTypes

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = types.KeyboardButton("🛍 Каталог")
    korzina = types.KeyboardButton("🛒 Корзина")
    acac = types.KeyboardButton("🆘 Помощь")
    markup.insert(catalog)
    markup.row(korzina, acac)
    welcome_message = f'Привет, {message.from_user.first_name}!\nУ меня ты сможешь купить некоторые товары!\nКонтакт моего разработчика: https://t.me/Garnlzerx'
    await bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@dp.message_handler(lambda message: message.text == '🆘 Помощь')
async def handle_help(message: types.Message):
    await bot.send_message(message.chat.id, "Команда Помощь")


@dp.message_handler(lambda message: message.text == '🛍 Каталог')
async def handle_catalog(message: types.Message):
    await handle_catalog_button(bot, message.chat.id)


@dp.message_handler(lambda message: message.text == '🛒 Корзина')
async def handle_corsina(message: types.Message):
    await corsina.show_cart(message)

@dp.callback_query_handler(lambda c: c.data in ['clear_cart', "payment"])
async def callback_handler(callback_query: types.CallbackQuery):
    await corsina.process_callback(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['back', 'forward', 'choose_enter_categorical'])
async def callback_handler(callback_query: types.CallbackQuery):
    await photo_handler.process_callback(bot, callback_query)

@dp.callback_query_handler(lambda c: c.data in ['back-enter', 'forward-enter', 'choose_enter', 'amount_sum', 'amount_min'])
async def callback_handler(callback_query: types.CallbackQuery):
    await photo_hendler_two.process_callback(bot, callback_query)

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)

@dp.message_handler(content_types = ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    for k, v, in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id, f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")
    photo_hendler_two.shopping_cart.clear()



@dp.callback_query_handler(lambda c: c.data.startswith('category'))
async def handle_category_choice(callback_query: types.CallbackQuery):
    category = callback_query.data.split('_')[1]
    await show_category_products(bot, callback_query.message.chat.id, category)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
