import asyncio
import sys
from datetime import datetime
from sys import platform
import os
import pyodbc
from dotenv import load_dotenv
load_dotenv()


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


def sql_inject(descript, reader_ipaddress, name, request_interval) -> None:
    try:
        cursor.execute('''
            SELECT MAX(readerNo) FROM "dbo"."EXP_Machines" ''')
        max_value = cursor.fetchone()[0] + 1
        cursor.execute('''
            INSERT INTO "dbo"."EXP_Machines"
            VALUES (?, ?, ?, ?, ?, ?) ''', (descript, max_value, reader_ipaddress, name, request_interval, 0))
        conn.commit()
        print(f'🈯 <b>БД:</b> <u>Информация занесена.</u> ID - <b>{max_value}</b>')
    except pyodbc.Error as err:
        print("🉐", datetime.now().strftime("%m/%d/%Y %H:%M:%S"), 'Error', err)
    finally:
        cursor.close()
        conn.close()


async def main():
    descript = sys.argv[1]
    reader_ipaddress = sys.argv[2]
    name_latin = sys.argv[3]
    request_interval = sys.argv[4]

    sql_inject(descript, reader_ipaddress, name_latin, request_interval)


if __name__ == '__main__':
    asyncio.run(main())
# print(sql_inject("[Амур] oloo", "192.168.223.11", 'ololo', '5min'))