# Notifications Service — Django 5

Microservicio encargado de la gestión de alertas y recordatorios para
pacientes del sistema hospitalario. Soporta notificaciones por SMS,
Email y App.

**Puerto:** `8002` | **Framework:** Django 5 | **BD:** PostgreSQL

---

## Endpoints

Base URL en desarrollo local: `http://localhost:8002`
Base URL a través del Gateway: `http://localhost:8000`

Todos los endpoints requieren el header:
`Authorization: Token <TOKEN_SECRETO>`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/notifications/` | Listar todas las notificaciones |
| POST | `/api/notifications/` | Crear una notificación |
| GET | `/api/notifications/{id}/` | Obtener por ID |
| PUT | `/api/notifications/{id}/` | Actualizar |
| DELETE | `/api/notifications/{id}/` | Eliminar |

### Ejemplo — Crear notificación
```json
POST /api/notifications/
{
  "patient_id": 1,
  "message": "Recuerde su cita mañana a las 9am",
  "type": "SMS"
}
```

Tipos válidos: `SMS`, `EMAIL`, `APP`

---

## Estructura

```text
django-notifications-service/
├── manage.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env                          # Variables locales (no en repo)
├── fixtures/
│   └── notifications.json        # Datos de prueba iniciales
├── notifications/
│   ├── models.py                 # Modelo Notification
│   ├── serializers.py            # Serializador DRF
│   ├── views.py                  # ViewSet CRUD
│   ├── middleware.py             # InternalTokenMiddleware
│   ├── urls.py                   # Rutas del servicio
│   └── tests.py                  # Pruebas unitarias
└── notifications_config/
    ├── settings.py               # Configuración Django
    └── urls.py                   # URLs raíz
```

---

## Configuración local

### Requisitos
- Python 3.12+
- PostgreSQL 14+

### Variables de entorno — `.env`
```bash
TOKEN_SECRETO=miclave123
DB_NAME=notifications_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Instalación
```bash
cd services/django-notifications-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py loaddata fixtures/notifications.json

# Iniciar servidor
python manage.py runserver 8002
```

---

## Ejecución con Docker

Este servicio se levanta automáticamente con Docker Compose desde la
raíz del proyecto. Al iniciar el contenedor ejecuta automáticamente:

1. Migraciones (`migrate`)
2. Carga de fixtures (`loaddata`)
3. Servidor Gunicorn en puerto `8002`

```bash
# Desde la raíz del proyecto
docker compose --env-file .env.docker up notifications-service -d

# Ver logs
docker logs hospital-notifications-service -f
```

---

## Seguridad

Implementa `InternalTokenMiddleware` que intercepta todas las peticiones
y valida el header `Authorization`. Si el token no coincide con
`TOKEN_SECRETO`, retorna `403 Forbidden`.

```python
# notifications/middleware.py
if request.headers.get('Authorization') != f'Token {self.token}':
    return JsonResponse({'error': 'No autorizado'}, status=403)
```

---

## Pruebas unitarias

```bash
cd services/django-notifications-service
python manage.py test notifications --verbosity=2
```

Las 5 pruebas cubren:

| # | Prueba | Qué verifica |
|---|---|---|
| 1 | `test_middleware_rechaza_request_sin_token` | Middleware retorna 403 sin token |
| 2 | `test_middleware_permite_request_con_token_valido` | Middleware permite acceso con token válido |
| 3 | `test_list_notifications_returns_200` | GET lista notificaciones |
| 4 | `test_create_notification_returns_201` | POST crea notificación |
| 5 | `test_delete_notification_returns_204` | DELETE elimina notificación |