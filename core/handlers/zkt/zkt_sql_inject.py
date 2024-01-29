import pyodbc
from datetime import datetime
from sys import platform
import os

driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
if platform == "linux" or platform == "linux2":
    driver = 'DRIVER={ODBC Driver 17 for SQL Server}'
elif platform == "win32":
    driver = 'DRIVER={SQL Server}'

server = 'SERVER=192.168.201.40'
port = os.getenv('PORT')
db = os.getenv('DB')
user = os.getenv('USER_DB')
pw = os.getenv('PW_DB')
conn_str = ';'.join([driver, server, port, db, user, pw])

conn = pyodbc.connect(conn_str)
conn.timeout = 60
cursor = conn.cursor()


async def sql_inject(id_zkt, id_user, hours=None, minutes=None):
    try:
        if hours is not None:
            cursor.execute('''
                INSERT INTO "dbo"."EXP_Events"   
                VALUES(?, ?, ?, ?) ''', (id_zkt, datetime.now().strftime(f"%d/%m/%Y {hours}:{minutes}:%S"+".000"), id_user, 0))
            date = datetime.now().strftime(f"%Y-%m-%d {hours}:{minutes}:%S")
        else:
            cursor.execute('''
                INSERT INTO "dbo"."EXP_Events"
                VALUES (?, ?, ?, ?) ''', (id_zkt, datetime.now().strftime("%d/%m/%Y %H:%M:%S"+".000"), id_user, 0))
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conn.commit()
        print(f'Запрос выполнен успешно! Сканер {id_zkt} - Пользователь: {id_user}')
        return f'''
✅<b>{date} запроc выполнен успешно!</b>
<b>ID сканера: <u>{id_zkt}</u></b>
Установлен <b>ID пользователя: <u>{id_user}</u></b>'''
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Не правильный пароль учетной записи базы данных')
            return f'''📛 <b>Не правильный пароль учетной записи базы данных</b>'''
        elif sqlstate == '08S01' or sqlstate == '08001' or sqlstate == '01000':
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} Нет связи с сервером базы данных')
            return f'''
📛 <b>Нет связи с сервером базы данных RFID</b>
Код ошибки: <b>{sqlstate}</b>'''
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:")} Ошибка: {ex}')
            return f'''📛 Ошибка: {ex}х'''
    # finally:
    #     cursor.close()
    #     conn.close()