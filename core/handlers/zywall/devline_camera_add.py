import requests
from requests.auth import HTTPBasicAuth

# Установите необходимые параметры для добавления камеры
camera_data = {
    'ip': '192.168.202.96',
    'port': 80,
    'username': 'admin',
    'password': 'Ckj;ysqgfhjkm13',
}

admin = "admin"
password = "PurgeXenos2012"

# Выполните запрос на добавление камеры
response = requests.get('http://192.168.206.115:9786/camera/list', auth=HTTPBasicAuth(admin, password))

# Проверьте статус код ответа
if response.status_code == 200:
    # Камера успешно добавлена
    print('Камера успешно добавлена', response.text)
else:
    # Обработайте ошибку
    print('Ошибка при добавлении камеры:', response.text)