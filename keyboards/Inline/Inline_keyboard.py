from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Клавиатура для показа корзины"""
keyboard_basket = InlineKeyboardMarkup(row_width = 2)
clear_button = InlineKeyboardButton(text = '❌ Очистить', callback_data = 'clear_cart')
edit_basket = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'edit_cart')
payment_button = InlineKeyboardButton(text = '💳 Оплатить', callback_data = 'payment')
keyboard_basket.add(clear_button, edit_basket, payment_button)

returnOrder = InlineKeyboardMarkup()
returnOrderButton = InlineKeyboardButton(text = 'Назад', callback_data = 'return_order')
returnOrder.add(returnOrderButton)

returnProfil = InlineKeyboardMarkup()
returnProfilButton = InlineKeyboardButton(text = 'Назад', callback_data = 'returnProfil')
returnProfil.add(returnProfilButton)

show_basket_add = InlineKeyboardMarkup()
catalog_basket = InlineKeyboardButton(text = "🛍 Каталог", callback_data = 'back_return')
show_basket = InlineKeyboardButton(text = '📦🛒 Корзина', callback_data = 'show_basket')
show_basket_add.add(catalog_basket, show_basket)



"""Клавиатура каталога товаров"""
product_categories = ['📔 Ежедневники', '💳 Кард-холдеры', '🖼 Обложки', "🔍 Поиск артикула"]
show_catalogs = InlineKeyboardMarkup(row_width = 1)
for category in product_categories:
    catalogs_button = InlineKeyboardButton(text = category, callback_data = f'category_{category}')
    show_catalogs.add(catalogs_button)

"""Клавиатура для показа категории товаров в выбранном каталоге"""
def create_category_keyboard(cur_img_index, cur_img_cap, product):
    category_product = InlineKeyboardMarkup(row_width = 2)
    btn_back = InlineKeyboardButton(text = '⬅', callback_data = f'categoryBack_{product}_{cur_img_index}_{cur_img_cap}')
    btn_forward = InlineKeyboardButton(text = '➡', callback_data = f'categoryForward_{product}_{cur_img_index}_{cur_img_cap}')
    # details = InlineKeyboardButton(text='Подробнее', callback_data='details')
    btn_enter = InlineKeyboardButton(text = '✅ Выбрать категорию', callback_data = f'choose-enter-categorical_{product}_{cur_img_index}_{cur_img_cap}')
    back_return = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'back_return')
    more = InlineKeyboardButton(text = '⁉ Подробнее', callback_data = f'categoryMore_{product}_{cur_img_index}_{cur_img_cap}')
    category_product.add(btn_back, btn_forward, back_return, more)
    category_product.insert(btn_enter)
    return category_product


def create_category_more_ceyboard(cur_img_indx):
    category_product_1 = InlineKeyboardMarkup(row_width = 2)
    btn_back_1 = InlineKeyboardButton(text = '⬅', callback_data = f'back_notebook_more_{cur_img_indx}')
    btn_forward_1 = InlineKeyboardButton(text = '➡', callback_data = f'forward_notebook_more_{cur_img_indx}')
    btn_pay_1 = InlineKeyboardButton(text = "Купить", callback_data = f'pay_notebook_more_{cur_img_indx}')
    back_return_1 = InlineKeyboardButton(text = '🚪 Назад', callback_data = f'back_notebook_more_{cur_img_indx}')

    category_product_1.add(btn_back_1, btn_forward_1, btn_pay_1)
    category_product_1.add(back_return_1)
    return category_product_1


category_product_1 = InlineKeyboardMarkup(row_width = 2)
btn_back_1 = InlineKeyboardButton(text = '⬅', callback_data = 'back_1')
btn_forward_1 = InlineKeyboardButton(text = '➡', callback_data = 'forward_1')
btn_enter = InlineKeyboardButton(text = '✅ Выбрать категорию',callback_data = 'choose_enter_categorical')
back_return_1 = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'more_back_return')
category_product_1.add(btn_back_1, btn_forward_1, back_return_1, btn_enter)



# category_product_1 = InlineKeyboardMarkup(row_width = 2)
# btn_back_1 = InlineKeyboardButton(text = '⬅', callback_data = 'back_1')
# btn_forward_1 = InlineKeyboardButton(text = '➡', callback_data = 'forward_1')
# back_return_1 = InlineKeyboardButton(text = '🚪 Назад', callback_data = 'back_return_1')
# category_product_1.add(btn_back_1, btn_forward_1, back_return_1)

"""Клавиатура для показа товаров в выбранной категории"""
def create_category_product_keyboard(cur_img_index, cur_img_cap):
    product_show = InlineKeyboardMarkup(row_width = 2)
    btn_back = InlineKeyboardButton(text = '⬅', callback_data = f'back-enter_{cur_img_index}_{cur_img_cap}')
    btn_forward = InlineKeyboardButton(text = '➡', callback_data = f'forward-enter_{cur_img_index}_{cur_img_cap}')
    amount_sum = InlineKeyboardButton(text = '➕', callback_data = f'amount-sum_{cur_img_index}_{cur_img_cap}')
    amount_min = InlineKeyboardButton(text = '➖', callback_data = f'amount-min_{cur_img_index}_{cur_img_cap}')
    btn_enter = InlineKeyboardButton(text = '✅ Добавить в корзину', callback_data = f'product-choose-enter_{cur_img_index}_{cur_img_cap}')
    return_back_to_choose_categorical = InlineKeyboardButton(text = '🚪 Вернуться', callback_data = 'back_to_choose')
    product_show.add(btn_back, btn_forward, amount_min, amount_sum, return_back_to_choose_categorical, btn_enter)

    return product_show



btn_back = InlineKeyboardButton(text = '⬅',callback_data = 'back-enter')
btn_forward = InlineKeyboardButton(text = '➡',callback_data = 'forward-enter')
return_back_to_choose_categorical = InlineKeyboardButton(text = '🚪 Вернуться',callback_data = 'back_to_choose')

product_show_nol = InlineKeyboardMarkup(row_width = 2)
product_show_nol.add(btn_back, btn_forward, return_back_to_choose_categorical)



product_show_articul = InlineKeyboardMarkup(row_width = 2)
product_show_articul_for_admin = InlineKeyboardMarkup(row_width = 2)
amount_sum_1 = InlineKeyboardButton(text = '➕', callback_data = 'amount_sum_1')
amount_min_1 = InlineKeyboardButton(text = '➖', callback_data = 'amount_min_1')
set_amount = InlineKeyboardButton(text = 'Установить кол-во', callback_data = 'set_amount')
back_return = InlineKeyboardButton(text = '🚪 Назад',callback_data = 'back_return')

btn_enter_1 = InlineKeyboardButton(text = '✅ Добавить в корзину', callback_data = 'choose_enter_1')
product_show_articul.add(amount_min_1, amount_sum_1, back_return, btn_enter_1)
product_show_articul_for_admin.add(amount_min_1, amount_sum_1, back_return, set_amount, btn_enter_1)


product_show_articul_nol = InlineKeyboardMarkup(row_width = 2)
product_show_articul_nol.add(back_return)


product_show_articul_nol_for_admin = InlineKeyboardMarkup(row_width = 2)
product_show_articul_nol_for_admin.add(back_return, set_amount)

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

profile_data_return = InlineKeyboardButton(text = "🛍 Каталог", callback_data = 'back_return')

profil_data_edit = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'change_data')
profil_data = InlineKeyboardMarkup().add(profil_data_edit)

profil_data_edit_1 = InlineKeyboardButton(text = '✏ Изменить', callback_data = 'change_data_1')
profil_data_order = InlineKeyboardButton(text = 'Мои заказы', callback_data = "myOrder")
profil_data_1 = InlineKeyboardMarkup().add(profile_data_return, profil_data_edit_1, profil_data_order)

# для регистрации в кнопке профиль
not_profil_data_edit_for_profil = InlineKeyboardButton(text = '🐱‍💻 Зарегистрироваться', callback_data = 'create_data_profil')
not_profil_data = InlineKeyboardMarkup().add(profile_data_return, not_profil_data_edit_for_profil)

