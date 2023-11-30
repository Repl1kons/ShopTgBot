import sqlite3

"""База данных"""
def add_user(user_id, name, city, region, street, number_house):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, name_str, city, region, street, number_house) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, name, city, region, street, number_house))
    conn.commit()
    conn.close()

"""База данных заказов"""
def add_order(user_id, product_id, quantity, price):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (user_id, product_id, quantity, price) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, product_id, quantity, price))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def is_name_filled(user_id):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_str FROM users WHERE user_id = ?', (user_id,))
    user_name = cursor.fetchone()
    conn.commit()
    conn.close()
    return user_name is not None and user_name[0] != ''



def get_user_data(user_id):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_str, city, region, street, number_house FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.commit()
    conn.close()
    return user_data if user_data else None

def get_total_price(user_id):
    conn = sqlite3.connect('data/bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT total_price FROM cart_items WHERE user_id = ?',(user_id,))
    total_price = cursor.fetchone()
    conn.commit()
    conn.close()
    return total_price if total_price else None