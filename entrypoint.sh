#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
./wait-for-it.sh db:5432 -- echo "PostgreSQL is ready"

# Применение миграций, если это необходимо
python manage.py makemigrations 
python manage.py migrate

# Сбор статических файлов
# python manage.py collectstatic --noinput --clear

# Запуск вашего Django приложения
exec "$@"
