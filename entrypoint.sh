#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
./wait-for-it.sh db:5432 -- echo "PostgreSQL is ready"

# Применение миграций, если это необходимо
python manage.py makemigrations 
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Загрузка данных для демонстрации
python manage.py loaddata demo_fixture.json

# Запуск вашего Django приложения
exec "$@"
