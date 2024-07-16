# Grocery store

## Описание

API для продуктового магазина.

## Технологии

- Python
- Django
- Django Rest Framework

## Запуск проекта в dev-режиме на Linux

1. Склонируйте репозиторий и перейдите в директорию проекта

    ```shell
    git clone https://github.com/mign0n/grocery_store.git && cd grocery_store
    ```

2. Установите виртуальное окружение, установите зависимости, выполните миграции
с помощью команд:

    ```shell
    python -m venv venv
    source venv/bin/activate
    make install-deps
    python grocery_store/manage.py migrate
    ```

3. Создайте суперпользователя django для доступа в админ-панель

   ```shell
    python grocery_store/manage.py createsuperuser
   ```

4. Запустите сервер:

    ```shell
    python grocery_store/manage.py runserver
    ```

5. Админ-панель будет доступна по адресу: http://127.0.0.1:8000/admin
6. Интерактивная документация по API: http://127.0.0.1:8000/api/docs
