#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
./wait-for-it.sh -t 30 db:5432 -- echo "PostgreSQL is ready"

# Применение миграций, если это необходимо
# Загрузка данных для демонстрации
python manage.py makemigrations && python manage.py migrate && python manage.py loaddata demo_fixture.json

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск тестов
pytest --disable-warnings

# Запуск вашего Django приложения
exec "$@"
