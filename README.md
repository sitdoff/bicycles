# Серивис аренды велосипедов

## О приложении

### Общая информация

Это backend для сервиса аренды велосипедов, который предоставляет RESTful API для выполнения основных операций.

### Дополнительно

-   Написаны модульные тесты на pytest
-   Настроена генерация документации с использованием drf-yasg
-   Написан Dockerfile и docker-compose.yaml для контейнеризации
-   Для асинхронного выполнения задач используется Celery
-   реализована авторизаци пользователя с помощью JWT

### Использованы технологии

-   Python 3.12
-   Django 5.0 и Django REST Framework 3.15
-   база данных - PostgreSQL
-   Docker для контейнеризации
-   Celery для асинхронного выполнения задач
-   Redis в качестве брокера сообщений
-   Flower для мониторинга задач в Celery
-   pytest для тестирования
-   drf-yasg для генерации документации
-   djoser + simple-jwt для аутентификации и генерации токенов

### Файл .env

В файле содержаться значения переменных, которые используютс для корректной работы проекта

```bash
DJANGO_SETTINGS_MODULE - путь к файлу настроект Django

SECRET_KEY - секретный ключ проекта Django

POSTGRES_DB - имя базы данных PostgreSQL
POSTGRES_USER - имя пользователя базы данных PostgreSQL
POSTGRES_PASSWORD - пароль от базы данных
POSTGRES_HOST - хост базы данных
POSTGRES_PORT - порт базы данных

CELERY_BROKER_URL - адрес броккера для Celery
CELERY_RESULT_BACKEND - адрес для результатов задач Celery
```

### Демонстрационные данные

Для демонстрации работы приложения предоставляется суперпользователь со следующими данными:

```
username: admin
password: admin_password
```

## Доступные эндпоинты

### Регистрация нового пользователя

Url: /auth/users/

Method: POST

Payload:

```json
{
  "username": string,
  "email": string,
  "password": "string
}
```

Example payload:

```json
{
    "username": "test_user",
    "email": "5BZp3@example.com",
    "password": "test_password"
}
```

Answer:

```json
{
    "username": string,
    "email": string,
    "id": "integer"
}
```

### Авторизация пользователя(получение JWT)

Url: /auth/jwt/create/

Method: POST

Payload:

```json
{
  "username": string,
  "email": string,
  "password": "string
}
```

Example payload:

```json
{
    "username": "test_user",
    "email": "5BZp3@example.com",
    "password": "test_password"
}
```

Answer:

```json
{
    "refresh": string,
    "access": string
}
```

### Обновление JWT

Url: /auth/jwt/create/

Method: POST

Payload:

```json
{
    "refresh": string
}
```

Example payload:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjQ0MjE4MSwiaWF0IjoxNzIyMzU1NzgxLCJqdGkiOiI4OGQ3NjEyZWE2NDI0YjQwYjkwMDg4MzA0MmNiNjFkNiIsInVzZXJfaWQiOjR9.q4qgtiKOZoW4syxtDeHxV8TQBsBNs7y1J3hza-S-wnw"
}
```

Answer:

```json
{
    "access": string
}
```

### Получение списка доступных велосипедов

Url: /bicycles/available/

Method: GET

Headers:

```
Authorization: JWT <access_jwt_token>
```

Answer:

```json

[
  {
    "id": integer,
    "brand": string,
    "cost_per_hour": string,
    "is_rented": boolean
  },
  ...
]
```

### Аренда велосипеда

Url: /bicycles/rent/

Method: POST

Headers:

```
Authorization: JWT <access_jwt_token>
```

Payload:

```json
{
    "bicycle": integer
}
```

Example payload:

```json
{
    "bicycle": 1
}
```

Answer:

```json

{
    "id": integer,
    "cost": null,
    "paid": boolean,
    "renter": integer,
    "end_time": string,
    "start_time": string,
    "bicycle": integer
}

```

### Возврат велосипеда

Url: /bicycles/return/

Method: POST

Headers:

```
Authorization: JWT <access_jwt_token>
```

Payload:

```json
{}
```

Example payload:

```json
{}
```

Answer:

```json

{
    "success": "Bicycle returned",
    "rent": integer
}

```

### Получение истории аренды пользователя

Url: /bicycles/rent/

Method: GET

Headers:

```
Authorization: JWT <access_jwt_token>
```

Answer:

```json
[
    {
        "id": integer,
        "cost": string,
        "paid": boolean,
        "renter": integer,
        "end_time": string,
        "start_time": string,
        "bicycle": integer
    },
    ...
]
```

## Запуск приложения

### Запуск через docker-compose

1. Склонировать проект

```bash

```

2. Перейти в папку проекта

```bash

```

3. Если есть необходимость, отредактировать файл .env
4. Запустить создание контейнеров. При сборке образа проекта в базу будут загружены данныe для демонстрации.

```bash
docker compose up -build
```

5. После окончания сборки проект будет доступер на http://localhost:8000
