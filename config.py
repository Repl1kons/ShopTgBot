BOT_TOKEN = "6532834159:AAFqX_4uZb4fyJY_46UsRTq6-qV8dESfzFc"
PAYMENT_TOKEN = "381764678:TEST:71796"

# from aiogram import Bot, Dispatcher, executor, types
# import config
# import logging
#
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(config.BOT_TOKEN)
# dp = Dispatcher(bot)
#
# PRICE = types.LabeledPrice(label='Купить ежедневник', amount = 1000*100)
#
# @dp.message_handler(commands = ["start"])
# async def start(message: types.Message):
#     await bot.send_invoice(message.chat.id,
#                            title = 'Оплата',
#                            description = 'Оплата заказа',
#                            provider_token = config.PAYMENT_TOKEN,
#                            currency = 'rub',
#                            photo_url = "https://sun9-16.userapi.com/impg/HhbeKifN2LITt_VdkYCxZmaOLKzWlqamMpCmiA/zHtt38urPg4.jpg?size=604x604&quality=95&sign=06841b75c204611cb93dd908a2311beb&c_uniq_tag=zX0B0sxoDyoH3-OeJBu5WAeqfbFMUSFzyDQbB-ffFqM&type=album",
#                            photo_width=416,
#                            photo_height = 234,
#                            photo_size = 416,
#                            is_flexible = False,
#                            prices = [PRICE],
#                            start_parameter = 'buy-todolist',
#                            payload  = 'test-invoice-payload')
#
#
# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_q.id, ok = True)
#
# @dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
# async def success_pay(message: types.Message):
#     payment_info = message.successful_payment.to_python()
#     for k, v in payment_info.items():
#         print(f'{k} = {v}')
#
#     await bot.send_message(message.chat.id,
#                            f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment}")
#
#
#
#
# executor.start_polling(dp)
#