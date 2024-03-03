from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


"""Главное меню"""
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_for_admin = ReplyKeyboardMarkup(resize_keyboard=True)
catalog = KeyboardButton("🛍 Каталог")
korzina = KeyboardButton("🛒 Корзина")
profil = KeyboardButton("👨Профиль")
help = KeyboardButton("🆘 Помощь")
public = KeyboardButton("Публикация анонсов/объявлений")
main_menu.insert(catalog)
main_menu.row(korzina, profil)
main_menu.insert(help)

main_menu_for_admin.add(korzina, profil)
main_menu_for_admin.add(catalog, help)
main_menu_for_admin.add(public)

