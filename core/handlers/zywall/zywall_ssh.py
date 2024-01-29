import asyncio
import os
import sys
import transliterate.exceptions
from transliterate import translit
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import string
import random
from dotenv import load_dotenv

load_dotenv()
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))


async def main():
    ip = sys.argv[1]
    ip_zywall = sys.argv[2]
    latin_name = sys.argv[3]
    mac = sys.argv[4]
    device = {
        'device_type': 'zyxel_os',
        'host': ip_zywall,
        'username': os.getenv('USERNAME_ZYWALL'),
        'password': os.getenv('PASS_ZYWALL'),
        'port': 22,  # optional, defaults to 22
        'secret': '',  # optional, defaults to ''
        'session_log': 'output.txt'
    }
    commands_add_ip = [
        'configure terminal',
        f'ip dhcp pool Static_LAN1_{ran}',
        f'host {ip}',
        f'hardware-address {mac}',
        f'description {latin_name}',
        'exit',
        'write',
        'interface lan1',
        f'ip dhcp-pool Static_LAN1_{ran}',
        'exit',
        'write',
    ]

    ssh_add(device, commands_add_ip)


def ssh_add(device_data, commands_add_ip):
    try:
        net_connect = ConnectHandler(**device_data)
        output = net_connect.send_config_set(commands_add_ip)
        print(f'🐍 <b>Zywall:</b> <u>IP успешно добавлен!</u>')  # необходимо проработать ошибки самого zywall
    except NetmikoTimeoutException as e:
        print(f'Ошибка подключения: {e}')
    except NetmikoAuthenticationException as e:
        print(f'Ошибка авторизации: {e}')


def translate(name):
    try:
        form_name = translit(name, reversed=True)
        return form_name
    except transliterate.exceptions.LanguageDetectionError as err:
        return name


if __name__ == "__main__":
    asyncio.run(main())


