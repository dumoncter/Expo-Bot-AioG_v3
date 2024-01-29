import asyncio
from datetime import datetime
import requests
import json
import sys

import transliterate.exceptions
from transliterate import translit

date_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
# Задайте параметры подключения к Zabbix API
url = 'http://192.168.202.115/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}

# Задайте данные аутентификации
username = 'Admin '
password = 'zabbix'


# Определите функцию для выполнения запросов к Zabbix API
def make_zabbix_api_request(data):
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = response.json()
    return result


def data_zabbix(ip, name, tags_1, tags_2):
    # Аутентификация в Zabbix API
    auth_data = {
        'jsonrpc': '2.0',
        'method': 'user.login',
        'params': {
            'user': username,
            'password': password
        },
        'id': 1
    }

    auth_result = make_zabbix_api_request(auth_data)
    auth_token = auth_result['result']

    # Получение ID группы узлов сети по имени
    group_data = {
        'jsonrpc': '2.0',
        'method': 'hostgroup.get',
        'params': {
            'output': 'extend',
            'filter': {
                'name': [tags_1]
            }
        },
        'auth': auth_token,
        'id': 2
    }

    group_result = make_zabbix_api_request(group_data)
    group_id = group_result['result'][0]['groupid']

    def translate(name):
        try:
            form_name = translit(name, reversed=True)
            return form_name
        except transliterate.exceptions.LanguageDetectionError as err:
            return name

    # Добавление нового хоста в Zabbix
    host_data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": translate(name),
            "name": name,
            "interfaces": [
                {
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "80",
                    "details": {
                        "version": 3,
                        "bulk": 0,
                        "securityname": "mysecurityname",
                        "contextname": "",
                        "securitylevel": 1
                    }
                }
            ],
            "groups": [
                {
                    "groupid": group_id
                }
            ],
            "tags": [
                {
                    "tag": "БОТ",
                    "value": date_time
                },
                {
                    "tag": tags_1,
                    "value": ""
                },
                {
                    "tag": tags_2,
                    "value": ""
                },

            ],
            "templates": [
                {
                    "templateid": "10186"
                }
            ]
        },
        "auth": auth_token,
        "id": 3

    }

    host_result = make_zabbix_api_request(host_data)

    # Проверка на наличие ошибок
    if 'error' in host_result:
        print('❌ Ошибка при добавлении хоста в Zabbix:', host_result['error']['data'])
    else:
        host_id = host_result['result']['hostids'][0]
        print(f'✅ <b>Zabbix:</b> <u>Новый хост</u> ID - <b>{host_id}</b>')


async def main():
    ip = sys.argv[1]  # Получение аргумента arg1
    name = sys.argv[2]  # Получение аргумента arg2
    tags_1 = sys.argv[3]
    tags_2 = sys.argv[4]

    data_zabbix(ip, name, tags_1, tags_2)


if __name__ == '__main__':
    asyncio.run(main())
