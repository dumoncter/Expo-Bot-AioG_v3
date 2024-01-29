import docker


def restart_bot():
    client = docker.from_env()
    docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    docker_client.containers.get("telegram_bot").restart()
    print(client)
    return
    # # Создаем клиент Docker
    # client = docker.from_env()
    #
    # # Определяем имя контейнера бота
    # container_name = 'telegram_bot'
    #
    # # Получаем объект контейнера
    # container = client.containers.get(container_name)
    #
    # # Останавливаем контейнер
    # container.stop()
    #
    # # Удаляем контейнер
    # container.remove()
    #
    # # Создаем новый контейнер на основе образа
    # client.containers.run('telegram_bot', detach=True, name=container_name)

