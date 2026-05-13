# Patient Service — Laravel 11

Microservicio encargado de la gestión del registro y datos demográficos
de los pacientes del sistema hospitalario.

**Puerto:** `8001` | **Framework:** Laravel 11 | **BD:** MySQL

---

## Endpoints

Base URL en desarrollo local: `http://localhost:8001`
Base URL a través del Gateway: `http://localhost:8000`

Todos los endpoints requieren el header:
`Authorization: Token <TOKEN_SECRETO>`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/patients` | Listar todos los pacientes |
| POST | `/api/patients` | Crear paciente |
| GET | `/api/patients/{id}` | Obtener por ID |
| PUT | `/api/patients/{id}` | Actualizar paciente |
| DELETE | `/api/patients/{id}` | Eliminar paciente |

### Ejemplo — Crear paciente
```json
POST /api/patients
{
  "name": "Ana",
  "last_name": "López",
  "identity_document": "1020304050",
  "birthday": "1995-08-15",
  "phone": "3009876543",
  "blood_type": "O+"
}
```

### Validaciones
| Campo | Regla |
|---|---|
| `name` | Requerido, string, máx. 255 caracteres |
| `last_name` | Requerido, string, máx. 255 caracteres |
| `identity_document` | Requerido, string, único |
| `birthday` | Requerido, formato fecha |
| `phone` | Opcional, string |
| `blood_type` | Opcional, string |

---

## Estructura

```text
laravel-patient-service/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   └── PatientController.php   # CRUD de pacientes
│   │   └── Middleware/
│   │       └── CheckSecretToken.php    # Validación token interno
│   └── Models/
│       └── Patient.php                 # Modelo Eloquent
├── database/
│   ├── migrations/                     # Estructura de tablas
│   ├── seeders/
│   │   └── PatientSeeder.php           # Datos de prueba
│   └── factories/
├── routes/
│   └── api.php                         # Definición de rutas
├── tests/
│   └── Feature/
│       └── PatientTest.php             # Pruebas unitarias
├── Dockerfile
├── .dockerignore
└── .env                                # Variables locales (no en repo)
```

---

## Configuración local

### Requisitos
- PHP 8.4+
- Composer
- MySQL 8.0+

### Variables de entorno — `.env`
```bash
APP_KEY=base64:TU_KEY_AQUI
APP_ENV=local
APP_DEBUG=true

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=hospital_patients
DB_USERNAME=root
DB_PASSWORD=root

TOKEN_SECRETO=miclave123
```

### Instalación
```bash
cd services/laravel-patient-service

# Instalar dependencias
composer install

# Generar APP_KEY
php artisan key:generate

# Ejecutar migraciones y seeders
php artisan migrate --seed

# Iniciar servidor
php artisan serve --port=8001
```

---

## Ejecución con Docker

Al iniciar el contenedor ejecuta automáticamente:

1. Espera a que MySQL esté listo
2. Migraciones (`migrate --force`)
3. Seeders (`PatientSeeder`)
4. Servidor Laravel en puerto `8001`

```bash
# Desde la raíz del proyecto
docker compose --env-file .env.docker up mysql patient-service -d

# Ver logs
docker logs hospital-patient-service -f
```

Logs esperados:
```bash
⏳ Esperando a que MySQL esté listo...
✅ MySQL listo. Ejecutando migraciones...
✅ Ejecutando seeders...
🚀 Iniciando servidor Laravel...
INFO  Server running on [http://0.0.0.0:8001].
```

---

## Seguridad

Implementa `CheckSecretToken` como middleware que valida el header
`Authorization` en cada petición leyendo el token desde variables
de entorno:

```php
// app/Http/Middleware/CheckSecretToken.php
public function handle(Request $request, Closure $next)
{
    $token    = $request->header('Authorization');
    $expected = 'Token ' . env('TOKEN_SECRETO');

    if ($token !== $expected) {
        return response()->json([
            'error' => 'Acceso no autorizado. Token inválido.'
        ], 403);
    }

    return $next($request);
}
```

---

## Pruebas unitarias

```bash
cd services/laravel-patient-service
php artisan test tests/Feature/PatientTest.php --verbose
```

Usa `RefreshDatabase` con SQLite en memoria — no requiere conexión
real a MySQL durante las pruebas.

Agrega esto al `phpunit.xml` para habilitar SQLite en pruebas:
```xml
<env name="DB_CONNECTION" value="sqlite"/>
<env name="DB_DATABASE" value=":memory:"/>
```

Las 5 pruebas cubren:

| # | Prueba | Qué verifica |
|---|---|---|
| 1 | `test_middleware_rechaza_request_sin_token` | Middleware retorna 403 sin token |
| 2 | `test_index_retorna_lista_de_pacientes` | GET lista pacientes y retorna 200 |
| 3 | `test_store_crea_paciente_con_datos_validos` | POST crea paciente y retorna 201 |
| 4 | `test_store_rechaza_datos_incompletos` | POST retorna 422 con datos inválidos |
| 5 | `test_destroy_elimina_paciente_existente` | DELETE elimina paciente y retorna 200 |
