import sqlite3

def create_database():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name_str TEXT,
            city TEXT,
            region TEXT,
            street TEXT,
            number_house TEXT,
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

if __name__ == "__main__":
    create_database()
