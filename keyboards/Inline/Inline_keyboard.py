from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Клавиатура для показа корзины"""
keyboard_basket = InlineKeyboardMarkup(row_width = 2)
clear_button = InlineKeyboardButton(text = '❌ Очистить', callback_data = 'clear_cart')
edit_basket = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'edit_cart')
payment_button = InlineKeyboardButton(text = '💳 Оплатить', callback_data = 'payment')
keyboard_basket.add(clear_button, edit_basket, payment_button)

show_basket_add = InlineKeyboardMarkup()
show_basket = InlineKeyboardButton(text = '📦🛒 К корзине', callback_data = 'show_basket')
show_basket_add.add(show_basket)

# show_basket_return = InlineKeyboardMarkup()
# show_basket_ret = InlineKeyboardButton(text = 'К корзине', callback_data = 'show_basket')
# show_basket_return.add(show_basket_ret)

"""Клавиатура каталога товаров"""
product_categories = ['📔 Ежедневники', '💳 Кард-холдеры', '🖼 Обложки']
show_catalogs = InlineKeyboardMarkup(row_width = 1)
for category in product_categories:
    catalogs_button = InlineKeyboardButton(text = category, callback_data = f'category_{category}')
    show_catalogs.add(catalogs_button)

"""Клавиатура для показа категории товаров в выбранном каталоге"""
category_product = InlineKeyboardMarkup(row_width = 2)
btn_back = InlineKeyboardButton(text = '⬅', callback_data = 'back')
btn_forward = InlineKeyboardButton(text = '➡', callback_data = 'forward')
# details = InlineKeyboardButton(text='Подробнее', callback_data='details')
btn_enter = InlineKeyboardButton(text = '✅ Выбрать категорию', callback_data = 'choose_enter_categorical')
back_return = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'back_return')
more = InlineKeyboardButton(text = '⁉ Подробнее', callback_data = 'more')
category_product.add(btn_back, btn_forward, back_return, more)
category_product.insert(btn_enter)


category_product_1 = InlineKeyboardMarkup(row_width = 2)
btn_back_1 = InlineKeyboardButton(text = '⬅', callback_data = 'back_1')
btn_forward_1 = InlineKeyboardButton(text = '➡', callback_data = 'forward_1')
back_return_1 = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'more_back_return')
category_product_1.add(btn_back_1, btn_forward_1, back_return_1, btn_enter)


# category_product_1 = InlineKeyboardMarkup(row_width = 2)
# btn_back_1 = InlineKeyboardButton(text = '⬅', callback_data = 'back_1')
# btn_forward_1 = InlineKeyboardButton(text = '➡', callback_data = 'forward_1')
# back_return_1 = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'back_return_1')
# category_product_1.add(btn_back_1, btn_forward_1, back_return_1)

"""Клавиатура для показа товаров в выбранной категории"""
product_show = InlineKeyboardMarkup(row_width = 2)
btn_back = InlineKeyboardButton(text = '⬅', callback_data = 'back-enter')
btn_forward = InlineKeyboardButton(text = '➡', callback_data = 'forward-enter')
amount_sum = InlineKeyboardButton(text = '➕', callback_data = 'amount_sum')
amount_min = InlineKeyboardButton(text = '➖', callback_data = 'amount_min')
btn_enter = InlineKeyboardButton(text = '✅ Добавить в корзину', callback_data = 'choose_enter')
return_back_to_choose_categorical = InlineKeyboardButton(text = '🚪 Вернуться', callback_data = 'back_to_choose')
product_show.add(btn_back, btn_forward, amount_min, amount_sum, return_back_to_choose_categorical, btn_enter)

"""Клавиатура для подтверждения данных пользователя"""
data_enter = InlineKeyboardButton(text = '✅ Да, все верно', callback_data = 'data-enter')
data_edit = InlineKeyboardButton(text = '❌ Нет, начать сначала', callback_data = 'data-edit')
user_data = InlineKeyboardMarkup().add(data_edit, data_enter)

data_enter_1 = InlineKeyboardButton(text = '✅ Да, все верно', callback_data = 'data-enter_1')
data_edit_1 = InlineKeyboardButton(text = '❌ Нет, начать сначала', callback_data = 'data-edit_1')
user_data_1 = InlineKeyboardMarkup().add(data_edit_1, data_enter_1)



confirmation_keyboard = InlineKeyboardMarkup(row_width = 2).add(
    InlineKeyboardButton(text = '✏ Изменить', callback_data = 'change_data'),
    InlineKeyboardButton(text = '✅ Подтвердить', callback_data = 'confirm_data'))

profile_data_return = InlineKeyboardButton(text = "К выбору товаров", callback_data = 'return_profile')

profil_data_edit = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'change_data')
profil_data = InlineKeyboardMarkup().add(profil_data_edit)

profil_data_edit_1 = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'change_data_1')
profil_data_1 = InlineKeyboardMarkup().add(profile_data_return, profil_data_edit_1)

# для регистрации в кнопке профиль
not_profil_data_edit_for_profil = InlineKeyboardButton(text = '🐱‍💻 Зарегистрироваться', callback_data = 'create_data_profil')
not_profil_data = InlineKeyboardMarkup().add(profile_data_return, not_profil_data_edit_for_profil)

