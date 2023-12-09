# from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
# import photo_handler
#
# async def send_photo_articul(bot, chat_id, path_dir):
#     global image_direct
#     image_direct = path_dir
#
#     more = InlineKeyboardMarkup(row_width=2)
#     back = InlineKeyboardButton(text='Назад', callback_data='more_back_return')
#     more.add(back)
#     global message_id
#     if image_direct in more:
#         caption_text = more[image_direct]
#
#         with open(image_direct, 'rb') as photo_file:
#
#            message_id = (await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=caption_text, reply_markup=more)).message_id
#     else:
#         # Если image_direct не найден в словаре asas, вы можете отправить сообщение об ошибке
#         await bot.send_message(chat_id=chat_id, text="Информация не найдена")
#
# async def process_callback(bot, callback_query):
#     global message_id
#     global path_a
#     global image_direct
#     if callback_query.data == 'more_back_return':
#         await bot.delete_message(chat_id = callback_query.message.chat.id,message_id = message_id)
#         await photo_handler.start_send_photo(bot, callback_query.message.chat.id, image_dir = path_a)
