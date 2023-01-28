import sqlite3

#select_db('orders', 'users', 'tg_id', message.chat.id)
def select_db(cell, chapter, item, value):
    connect=sqlite3.connect('db.db')
    cursor=connect.cursor()
    if value=='0':
        cursor.execute(f"SELECT {cell} FROM {chapter}")
    else:
        value=str(value)
        cursor.execute(f"SELECT {cell} FROM {chapter} WHERE {item}=(?)",(value,))
    data=cursor.fetchone()
    connect.commit()
    try:
        return data[0]
    except:
        return False
        
#update_db('categor', 'settings', 'id', '1', categor)
def update_db(cell, chapter, item,  value, value2):
    connect  = sqlite3.connect('db.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE {chapter} SET {cell} = (?) WHERE {item}=(?)', (value2, value )) 
    connect.commit()

#insert_db('code,user,status','orders',(code, message.chat.id,0), '?,?,?')
def insert_db(cell, chapter, value, value2):
    connect  = sqlite3.connect('db.db')
    cursor = connect.cursor()
    cursor.execute(f'INSERT INTO {chapter} ({cell}) VALUES ({value2})', value)
    connect.commit() 

def count_db(cell,chapter):
    connect  = sqlite3.connect('db.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT COUNT ({cell}) FROM {chapter}')
    data=cursor.fetchone()
    connect.commit()
    try:
        return data[0]
    except:
        return False