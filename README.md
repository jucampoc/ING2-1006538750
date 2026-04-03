
# Sistema de Gestión Hospitalaria - Microservicios
Ingeniería de Software II - Julian Camilo Campo Cabrera -
02 de Abril del 2026




## Descripción General del Proyecto

Este sistema implementa una arquitectura de microservicios para la gestión hospitalaria. El acceso a todos los servicios está centralizado y protegido a través de un API Gateway.


## Arquitectura del Sistema

```text
       +-----------------------------------------------------------+
       |                      CLIENTES (REST)                      |
       |                  (Thunder Client / Web)                   |
       +----------------------------+------------------------------+
                                    |
                                    | HTTP/HTTPS (Port 8000)
                                    v
       +----------------------------+------------------------------+
       |                     API GATEWAY                           |
       |             Laravel 11 | Port: 8000                       |
       |        +-----------------------------------------+        |
       |        | Autenticación JWT | Enrutamiento (Proxy)|        |
       |        +-----------------------------------------+        |
       +------+-----------+-----------+------------+-----------+---+
              |           |           |            |           |
      ________v___________v___________v____________v___________v________
     |                                                                  |
     |                     RED INTERNA / MICROSERVICIOS                 |
     |__________________________________________________________________|
              |           |           |               |                 |
     +--------v---+  +----v-------+  +v-----------+  +v----------+  +---v--------+
     |  PATIENTS  |  |NOTIFICATIONS| |APPOINTMENTS|  | PHARMACY   | |MED. RECORDS|
     | Laravel 11 |  |   Django    | | Express.js |  | Express.js | |   Flask    |
     | Port: 8001 |  | Port: 8002  | | Port: 3000 |  | Port: 3001 | | Port: 5000 |
     +--------+---+  +----+-------+  +-----+------+  +-----+------+ +------------+
              |           |                |               |               |
              v           v                v               v               v
     +--------+---+  +----+-------+  +-----+------+  +-----+------+  +-----+------+
     |   MySQL    |  | PostgreSQL |  | Firestore  |  |  MongoDB   |  |  MongoDB   |
     |  (Local)   |  |  (Local)   |  |  (Cloud)   |  |  (Atlas)   |  |  (Atlas)   |
     +------------+  +------------+  +------------+  +------------+  +------------+
```
## Seguridad
El sistema implementa un modelo de seguridad por capas para garantizar la integridad de los datos hospitalarios
### Capa 1: Cliente → Gateway (JWT)
| Elemento | Detalle |
| :--- | :--- |
| **Algoritmo** | `HS256 (HMAC SHA-256)` |
| **Header** | `Authorization: Bearer <token>` |
| **Expiración** | Configurable |
| **Invalidación** | Blacklist en base de datos MySQL |
| **Librería** | `tymon/jwt-auth` para Laravel 11 |

**Rutas sin autenticación:**
* `POST /api/login`
* `POST /api/register`
* `POST /api/password-recovery`

**Rutas con autenticación JWT obligatoria:**
* Todas las rutas de servicios internos (`/api/patients`, `/api/appointments`, `/api/notifications`, `/api/pharmacy`, `/api/medical-records`)

### Capa 2: Gateway → Microservicios (X-Internal-Key)
Los microservicios internos no son accesibles directamente desde el exterior. Solo el Gateway conoce su ubicación interna y clave de acceso.

| Elemento | Detalle |
| :--- | :--- |
| **Mecanismo** | Header HTTP personalizado |
| **Header** | `X-Internal-Key: <clave_secreta_compartida>` |
| **Configuración** | Variable de entorno en Gateway y en cada microservicio |
| **Rechazo** | El microservicio devuelve `403 Forbidden` si la clave falta o es errónea |

 **Nota:** Los microservicios nunca son accesibles directamente desde el exterior. Solo el Gateway (Port 8000) conoce su URL interna y clave de acceso.

 ### Capa 3: Gestión de Secretos y Persistencia (En desarrollo)
En cumplimiento con las buenas prácticas y para mitigar riesgos de filtración de credenciales detectados por GitHub:

* **Secret Management:** Las URIs de conexión a **MongoDB Atlas** y las llaves de **Cloud Firestore** se gestionan exclusivamente mediante variables de entorno (`.env`).
* **Git Integrity:** El archivo `.gitignore` está configurado para excluir archivos sensibles, evitando la exposición de secretos en el repositorio público.
* **Aislamiento de Datos:** Los motores de base de datos relacionales (**MySQL** y **PostgreSQL**) están configurados para aceptar conexiones únicamente desde el host local de los microservicios correspondientes.
## Estructura del Proyecto

El proyecto sigue una arquitectura de monorepositorio con una clara separación entre el punto de entrada y los servicios especializados.

```text
ING2-1006538750/
├── api-gateway/                        # Puerto 8000 (Laravel 11)
│   ├── app/Http/Controllers/           # Lógica de Proxy y Auth (JWT)
│   ├── routes/api.php                  # Enrutamiento hacia microservicios
│   └── .env                            # JWT_SECRET y Service URLs
├── docs/                               # Diagramas y archivos de la Entrega #1
└── services/                           # Directorio de Microservicios
    ├── django-notifications-service/   # Puerto 8002 (Django)
    │   ├── notifications/              # App de alertas
    │   ├── settings.py                 # Configuración PostgreSQL
    │   └── manage.py                   # CLI de Django
    ├── express-appointments-service/   # Puerto 3000 (Express.js)
    │   ├── config/firebase.js          # SDK de Cloud Firestore
    │   ├── routes/                     # Endpoints de Citas
    │   └── package.json                # Dependencias Node.js
    ├── express-pharmacy-service/       # Puerto 3001 (Express.js)
    │   ├── models/                     # Esquemas Mongoose (Atlas)
    │   └── app.js                      # Servidor Express
    ├── flask-medicalrecords-service/   # Puerto 5000 (Flask)
    │   ├── database/db.py              # Conexión PyMongo (Atlas)
    │   ├── app.py                      # Rutas de Historias Clínicas
    │   └── requirements.txt            # Dependencias Python
    └── laravel-patient-service/        # Puerto 8001 (Laravel 11)
        ├── app/Models/Patient.php      # Modelo de Datos (MySQL)
        ├── database/migrations/        # Estructura de tablas
        └── routes/api.php              # CRUD de Pacientes
```

## Instalación y Configuración

Siga estos pasos para configurar el entorno de desarrollo local y desplegar los microservicios.

### Requisitos Previos

Asegúrese de tener instalados los siguientes entornos:
* **PHP 8.2+** & **Composer** (Gateway & Patients)
* **Python 3.10+** & **Pip** (Notifications & Medical Records)
* **Node.js 18+** & **NPM** (Appointments & Pharmacy)
* **MySQL 8.0** & **PostgreSQL 14**
* **Cuentas Cloud:** MongoDB Atlas y Firebase (Google Cloud).

---

### Paso 1: Clonar el Proyecto
```bash
# clonar el repositorio
git clone [https://github.com/jucampoc/ING2-1006538750.git)

# nos dirigimos al proyecto
cd ING2-1006538750

# Instalar dependencias PHP
composer install

# Copiar y configurar variables de entorno
cp .env.example .env
php artisan key:generate
```
### Configuración del .env

```bash
APP_NAME=Laravel
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://localhost

APP_LOCALE=en
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=en_US

APP_MAINTENANCE_DRIVER=file
# APP_MAINTENANCE_STORE=database

# PHP_CLI_SERVER_WORKERS=4

BCRYPT_ROUNDS=12

LOG_CHANNEL=stack
LOG_STACK=single
LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=api-gateway
DB_USERNAME=root
DB_PASSWORD=root

SESSION_DRIVER=database
SESSION_LIFETIME=120
SESSION_ENCRYPT=false
SESSION_PATH=/
SESSION_DOMAIN=null

BROADCAST_CONNECTION=log
FILESYSTEM_DISK=local
QUEUE_CONNECTION=database

CACHE_STORE=database
# CACHE_PREFIX=

MEMCACHED_HOST=127.0.0.1

REDIS_CLIENT=phpredis
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=log
MAIL_SCHEME=null
MAIL_HOST=127.0.0.1
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
AWS_USE_PATH_STYLE_ENDPOINT=false

VITE_APP_NAME="${APP_NAME}"

MEDICAL_RECORDS_SERVICE_URL=http://127.0.0.1:5000/api/medical-records
MEDICAL_RECORDS_SECRET_TOKEN="Token miclave123"
```