from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


"""Главное меню"""
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
catalog = KeyboardButton("🛍 Каталог")
korzina = KeyboardButton("🛒 Корзина")
profil = KeyboardButton("👨Профиль")
help = KeyboardButton("🆘 Помощь")
main_menu.insert(catalog)
main_menu.row(korzina, profil)
main_menu.insert(help)

main_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
adminButton = KeyboardButton("Админ епт")
main_menu_admin.row(adminButton, catalog)
