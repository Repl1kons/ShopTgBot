import sqlite3

"""База данных"""
async def add_user(user_id, name, city, region, street, number_house, apartment, indecs, db):
    await db.User.update_one(dict(
        _id = user_id),
        {
            "$set": {'data.name': name,
                     'data.city': city,
                     'data.region': region,
                     'data.street': street,
                     'data.number_house': number_house,
                     'data.apartment': apartment,
                     'data.indecs': indecs}
        }
    )


def get_all_amount(articul):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    cursor.execute('SELECT all_amount FROM product WHERE articul = ?', (articul,))
    all_amount = cursor.fetchone()
    conn.commit()
    conn.close()
    return all_amount if all_amount else None


def update_all_amount(articul, new_amount):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    # Обновляем all_amount для заданного артикула
    cursor.execute('UPDATE product SET all_amount = ? WHERE articul = ?',(new_amount,articul))
    conn.commit()
    conn.close()




def update_status_order(id_order, status):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    # Обновляем all_amount для заданного артикула
    cursor.execute('UPDATE users_order SET status = ? WHERE id_order = ?', (status, id_order,))
    conn.commit()
    conn.close()




def get_user_order(user_id):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_order, name_product, articul, variant, quantity, price FROM users_order WHERE user_id = ?',(user_id,))
    parametr = cursor.fetchall()
    conn.commit()
    conn.close()
    return parametr if parametr else None

def get_all_user_order():
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_order, name_product, articul, variant, quantity, price FROM users_order')
    parametr = cursor.fetchall()
    conn.commit()
    conn.close()
    return parametr if parametr else None

def get_user_order_order_id(order_id):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_product, articul, variant, quantity, price, status, user_id FROM users_order WHERE id_order = ?',(order_id,))
    parametr = cursor.fetchall()
    conn.commit()
    conn.close()
    return parametr if parametr else None

def set_user_order(user_id, id_order, name_product, articul, variant, quantity, price):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users_order (
        user_id,
        id_order,
        name_product,
        articul,
        variant,
        quantity,
        price) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, id_order, name_product, articul, variant, quantity, price))
    conn.commit()
    conn.close()