import sqlite3

def create_database_user_info():
    conn = sqlite3.connect('user_corsina.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name_str TEXT,
            city TEXT,
            region TEXT,
            street TEXT,
            number_house TEXT,
            apartment TEXT,
            indecs TEXT
        )
    ''')

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        articul TEXT,
        selected_category TEXT,
        selected_variant TEXT,
        quantity INTEGER,
        price REAL,
        total_price INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);
    ''')

    conn.commit()
    conn.close()

"""Создание таблицы с товарами"""
# def create_database_product():
#     conn = sqlite3.connect('bot_product.db')
#     cursor = conn.cursor()
#
#     cursor.execute('''
#             CREATE TABLE IF NOT EXISTS product (
#                 articul INTEGER,
#                 name_product TEXT,
#                 variant INTEGER,
#                 price INTEGER,
#                 photo_path STRING,
#                 all_amount INTEGER
# );
#     ''')
#
#     conn.commit()
#     conn.close()


# def create_database_users_order():
#     conn = sqlite3.connect('bot_users_order.db')
#     cursor = conn.cursor()
#
#     cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users_order (
#                 user_id INTEGER,
#                 id_order INTEGER,
#                 name_product TEXT,
#                 articul INTEGER,
#                 variant INTEGER,
#                 quantity INTEGER,
#                 price INTEGER,
#                 status STRING
# );
#     ''')

    # conn.commit()
    # conn.close()

if __name__ == "__main__":
    # create_database_users_order()
    create_database_user_info()
    # create_database_product()
