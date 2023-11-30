from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Клавиатура для показа корзины"""
clear_button = InlineKeyboardButton(text = 'Очистить',callback_data = 'clear_cart')
payment_button = InlineKeyboardButton(text = 'Оплатить',callback_data = 'payment')
keyboard_basket = InlineKeyboardMarkup().add(clear_button,payment_button)


"""Клавиатура каталога товаров"""
product_categories = ['📔 Ежедневники', '💳 Кард-холдеры', '🖼 Обложки']
show_catalogs = InlineKeyboardMarkup(row_width = 1)  # Создаем Inline клавиатуру
for category in product_categories:
    catalogs_button = InlineKeyboardButton(text = category,callback_data = f'category_{category}')
    show_catalogs.add(catalogs_button)


"""Клавиатура для показа категории товаров в выбранном каталоге"""
category_product = InlineKeyboardMarkup(row_width=2)
btn_back = InlineKeyboardButton(text='⬅', callback_data='back')
btn_forward = InlineKeyboardButton(text='➡', callback_data='forward')
details = InlineKeyboardButton(text='Подробнее', callback_data='details')
btn_enter = InlineKeyboardButton(text='Подтвердить выбор', callback_data='choose_enter_categorical')
back_return = InlineKeyboardButton(text='Назад', callback_data='back_return')
category_product.add(btn_back, btn_forward, btn_enter)


"""Клавиатура для показа товаров в выбранной категории"""
product_show = InlineKeyboardMarkup(row_width=2)
btn_back = InlineKeyboardButton(text='⬅', callback_data='back-enter')
btn_forward = InlineKeyboardButton(text='➡', callback_data='forward-enter')
amount_sum = InlineKeyboardButton(text='➕', callback_data='amount_sum')
amount_min = InlineKeyboardButton(text='➖', callback_data='amount_min')
btn_enter = InlineKeyboardButton(text='Добавить в корзину', callback_data='choose_enter')
back_to_choose_categorical = InlineKeyboardButton(text='Вернуться назад', callback_data='back_to_choose')
product_show.add(btn_back, btn_forward, amount_min, amount_sum, btn_enter)


"""Клавиатура для подтверждения данных пользователя"""
data_enter = InlineKeyboardButton(text = 'Да, все верно',callback_data = 'data-enter')
data_edit = InlineKeyboardButton(text = 'Нет, начать сначала',callback_data = 'data-edit')
user_data = InlineKeyboardMarkup().add(data_edit,data_enter)

confirmation_keyboard = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Изменить', callback_data='change_data'),
    InlineKeyboardButton(text='Подтвердить', callback_data='confirm_data'))

profil_data_edit = InlineKeyboardButton(text = 'Изменить',callback_data = 'change_data')
# profile_forward = InlineKeyboardButton(text = 'Назад',callback_data = 'Return_profile')
profil_data = InlineKeyboardMarkup().add(profil_data_edit)