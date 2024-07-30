#!/bin/bash
# Устанавливаем строгий режим
set -e

python manage.py collectstatic

# Ожидание доступности базы данных
./wait-for-it.sh db:5432 -- echo "PostgreSQL is ready"

# Применение миграций, если это необходимо
python manage.py makemigrations && python manage.py migrate

# Запуск вашего Django приложения
exec "$@"
