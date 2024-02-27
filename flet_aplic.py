import flet
from flet import Page, ElevatedButton, MainAxisAlignment, TextAlign, TextField, Text

import config
import data.db.database
from main import bot


async def main(page: Page):
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700
    page.window_resizable = False

    async def auth(e):
        _login = int(login_input.value)

        # if _login == config.ID_ADMIN:
        #     # user = data.db.database.get_user_data(_login)
        #     await page.clean_async()
        #     await page.add_async(Text(f"Данные пользователя:\n"
        #                               f"Имя: {user[0]}\n"
        #                               f"Город: {user[1]}"))
        #     await bot.send_message(_login, f"{user[0]} has new authorization")

    login_input = TextField(text_align=TextAlign.CENTER, label='ID')

    await page.add_async(
        login_input,
        ElevatedButton("Authorize", on_click=auth)
    )


if __name__ == "__main__":
    flet.app(target=main, view = flet.WEB_BROWSER)
