import sqlite3

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('data.db')
    return __connection

def init_db(force: bool = False):
    
    conn = get_connection()

    c = conn.cursor() 

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message(
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            price       TEXT NOT NULL,
            description TEXT NOT NULL,
            datee        TEXT NOT NULL
        )
    ''')

    conn.commit()

def add_message(user_id: int, price: str, description: str, datee: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, price, description, datee) VALUES (?, ?, ?, ?)', (user_id, price, description, datee))
    conn.commit()

def fetchall(table, columns):
    conn = get_connection()
    c = conn.cursor()
    columns_joined = ', '.join(columns)
    c.execute(f"SELECT {columns_joined} From {table}")
    lines = c.fetchall()
    result = []
    for line in lines:
        dict_line = {}
        for i, col in enumerate(columns):
            dict_line[col] = line[i]
        result.append(dict_line)
    return result


if __name__ == '__main__':
    init_db() 
    add_message(user_id = 483528710, price = '888', description = 'пятерочка', datee = '13 Apr 2021')
    add_message(user_id = 483528710, price = '190', description = 'шаурма', datee = '13 Apr 2021')
    print(fetchall('user_message', ['id', 'user_id', 'price', 'description', 'datee']))