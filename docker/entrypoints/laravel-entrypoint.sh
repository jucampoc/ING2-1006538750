#!/bin/sh
set -e

echo "Esperando a que MySQL esté listo..."
until php artisan migrate:status > /dev/null 2>&1; do
    echo "   MySQL no está listo — reintentando en 3s..."
    sleep 3
done

echo "MySQL listo. Ejecutando migraciones..."
php artisan migrate --force --no-interaction

echo "Ejecutando seeders..."
php artisan db:seed --force --no-interaction

echo "Iniciando servidor Laravel..."
exec php artisan serve --host=0.0.0.0 --port=$APP_PORT