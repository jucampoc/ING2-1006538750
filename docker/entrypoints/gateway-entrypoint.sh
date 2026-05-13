#!/bin/sh
set -e

echo "⏳ Esperando a que MySQL esté listo..."
until php artisan tinker --execute="DB::connection()->getPdo(); echo 'ok';" 2>/dev/null | grep -q "ok"; do
    echo "   MySQL no está listo — reintentando en 3s..."
    sleep 3
done

echo "✅ MySQL listo. Ejecutando migraciones..."
php artisan migrate --force --no-interaction

echo "✅ Ejecutando seeders..."
php artisan db:seed --class=DatabaseSeeder --force --no-interaction 2>/dev/null || true

echo "🚀 Iniciando servidor Laravel..."
exec php artisan serve --host=0.0.0.0 --port=$APP_PORT