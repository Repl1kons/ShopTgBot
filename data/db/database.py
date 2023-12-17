import sqlite3

"""База данных"""
def add_user(user_id, name, city, region, street, number_house, apartment, indecs):
    sql = '''
        INSERT INTO users (user_id, name_str, city, region, street, number_house, apartment, indecs) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    with sqlite3.connect('data/user_corsina.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (user_id, name, city, region, street, number_house, apartment, indecs))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error inserting user: {e}")

"""База данных заказов"""
def add_order(user_id, product_id, quantity, price):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (user_id, product_id, quantity, price) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, product_id, quantity, price))
    conn.commit()
    conn.close()


async def add_product(articul, name, variant, price, photo_path):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()

    # Проверка, существует ли уже продукт с этим артикулом
    cursor.execute("SELECT * FROM product WHERE articul = ?", (articul,))
    product = cursor.fetchone()

    if product is None:
        # Если продукта нет, вставляем новую запись
        cursor.execute('''
            INSERT INTO product (articul, name_product, variant, price, photo_path) 
            VALUES (?, ?, ?, ?, ?)
        ''', (articul, name, variant, price, photo_path))
    else:
        # Если продукт существует, обновляем его данные
        cursor.execute('''
            UPDATE product 
            SET name_product = ?, variant = ?, price = ?, photo_path = ?
            WHERE articul = ?
        ''', (name, variant, price, photo_path, articul))

    conn.commit()
    conn.close()


# def update_all_amount():
#     conn = sqlite3.connect('data/bot_product.db')
#     cursor = conn.cursor()
#
#     # Обновление поля all_amount во всех записях
#     cursor.execute('''
#         UPDATE product SET all_amount = 50
#     ''')
#
#     conn.commit()
#     conn.close()



def delete_user(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def is_name_filled(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_str FROM users WHERE user_id = ?', (user_id,))
    user_name = cursor.fetchone()
    conn.commit()
    conn.close()
    return user_name is not None and user_name[0] != ''



def get_user_data(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_str, city, region, street, number_house, apartment, indecs FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.commit()
    conn.close()
    return user_data if user_data else None

def get_all_amount(articul):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    cursor.execute('SELECT all_amount FROM product WHERE articul = ?', (articul,))
    all_amount = cursor.fetchone()
    conn.commit()
    conn.close()
    return all_amount if all_amount else None

def get_price(articul):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    cursor.execute('SELECT price FROM product WHERE articul = ?', (articul,))
    price = cursor.fetchone()
    conn.commit()
    conn.close()
    return price if price else None


def update_all_amount(articul, new_amount):
    conn = sqlite3.connect('data/bot_product.db')
    cursor = conn.cursor()
    # Обновляем all_amount для заданного артикула
    cursor.execute('UPDATE product SET all_amount = ? WHERE articul = ?',(new_amount,articul))
    conn.commit()
    conn.close()

def get_total_price(user_id):
    conn = sqlite3.connect('data/user_corsina.db')
    cursor = conn.cursor()
    cursor.execute('SELECT total_price FROM cart_items WHERE user_id = ?',(user_id,))
    total_price = cursor.fetchone()
    conn.commit()
    conn.close()
    return total_price if total_price else None

def get_user_order(user_id):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_order, name_product, articul, variant, quantity, price FROM users_order WHERE user_id = ?',(user_id,))
    parametr = cursor.fetchall()
    conn.commit()
    conn.close()
    return parametr if parametr else None

def get_user_order_order_id(order_id):
    conn = sqlite3.connect('data/bot_users_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_product, articul, variant, quantity, price FROM users_order WHERE id_order = ?',(order_id,))
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