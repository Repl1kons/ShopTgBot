from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


"""Главное меню"""
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder = "Выберите действия из меню")
catalog = KeyboardButton("🛍 Каталог")
korzina = KeyboardButton("🛒 Корзина")
profil = KeyboardButton("👨Профиль")
help = KeyboardButton("🆘 Помощь")
main_menu.insert(catalog)
main_menu.row(korzina, profil)
main_menu.insert(help)

