import requests

controller_address = "192.168.202.138"
username = "admin"
password = "adminpsw"
organization_name = "Rostov"
access_point_ip = "192.168.202.139"
access_point_name = "Тест"


def add_access_point_to_organization(controller_address, username, password, organization_name, access_point_ip, access_point_name):
    # Авторизация в контроллере Omada
    login_payload = {
        "username": username,
        "password": password
    }
    session = requests.Session()
    session.post(controller_address + "/api/v1/login", json=login_payload)

    # Получение информации об организациях
    organizations_response = session.get(controller_address + "/api/v1/organizations")
    organizations = organizations_response.json()

    # Поиск ID организации "Rostov"
    organization_id = None
    for organization in organizations:
        if organization["name"] == organization_name:
            organization_id = organization["id"]
            break

    if organization_id is None:
        print("Не удалось найти организацию", organization_name)
        return

    # Добавление точки доступа в организацию
    access_point_data = {
        "ip_address": access_point_ip,
        "name": access_point_name,
        "organization_id": organization_id
    }

    add_access_point_response = session.post(controller_address + "/api/v1/access-points", json=access_point_data)

    if add_access_point_response.status_code == 200:
        print("Точка доступа успешно добавлена в организацию", organization_name)
    else:
        print("Ошибка при добавлении точки доступа. Код ошибки:", add_access_point_response.status_code)

# Пример использования
add_access_point_to_organization(controller_address, username, password, organization_name, access_point_ip, access_point_name)