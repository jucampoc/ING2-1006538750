
# Sistema de Gestión Hospitalaria - Microservicios
Ingeniería de Software II - Julian Camilo Campo Cabrera -
02 de Abril del 2026




## Descripción General del Proyecto

Este sistema implementa una arquitectura de microservicios para la gestión hospitalaria. El acceso a todos los servicios está centralizado y protegido a través de un API Gateway.


## Arquitectura del Sistema

```text
        +-----------------------------------------------------------+
        |                     CLIENTES (REST)                       |
        |                (Thunder Client / Web)                     |
        +----------------------------+------------------------------+
                                     |
                                     | HTTP/HTTPS (Port 8000)
                                     v
        +----------------------------+------------------------------+
        |                     API GATEWAY                           |
        |              Laravel 11 | Port: 8000                      |
        |        +-----------------------------------------+        |
        |        | Autenticación Sanctum | Proxy Routing   |        |
        |        +-----------------------------------------+        |
        +------+-----------+-----------+------------+-----------+---+
               |           |           |            |           |
      _________v___________v___________v____________v___________v________
     |                                                                  |
     |                    RED INTERNA / MICROSERVICIOS                  |
     |__________________________________________________________________|
               |           |           |               |                |
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
### Capa 1: Cliente → Gateway (Sanctum)
La autenticación se gestiona mediante **Laravel Sanctum**, proporcionando tokens de acceso personales (SPA/Mobile friendly).

| Elemento | Detalle |
| :--- | :--- |
| **Mecanismo** | Bearer Token (PlainTextToken) |
| **Header** | `Authorization: Bearer <token>` |
| **Invalidación** | Revocación en tabla `personal_access_tokens` |
| **Database** | MySQL (api-gateway) |

### Capa 2: Gateway → Microservicios (Shared Secret)
Para asegurar que los microservicios solo respondan al Gateway, se utiliza un token de autorización compartido.

* **Header:** `Authorization: Token miclave123`
* **Implementación:** El Gateway inyecta este header en cada petición hacia los servicios internos para superar el middleware auth.secret (Laravel) o el InternalTokenMiddleware (Django).

**Rutas sin autenticación:**
* `POST /api/login`
* `POST /api/register`
* `POST /api/password-recovery`

**Rutas con autenticación JWT obligatoria:**
* Todas las rutas de servicios internos (`/api/patients`, `/api/appointments`, `/api/notifications`, `/api/pharmacy`, `/api/medical-records`)

 **Nota:** Los microservicios nunca son accesibles directamente desde el exterior. Solo el Gateway (Port 8000) conoce su URL interna y clave de acceso.

 ### Capa 3: Gestión de Secretos y Persistencia (En desarrollo)
En cumplimiento con las buenas prácticas y para mitigar riesgos de filtración de credenciales detectados por GitHub:

* **Secret Management:** Las URIs de conexión a **MongoDB Atlas** y las llaves de **Cloud Firestore** se gestionan exclusivamente mediante variables de entorno (`.env`).
* **Git Integrity:** El archivo `.gitignore` está configurado para excluir archivos sensibles, evitando la exposición de secretos en el repositorio público.
* **Aislamiento de Datos:** Las bases de datos locales están configuradas para aceptar conexiones exclusivamente desde el microservicio propietario.
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

### 1. API Gateway - Laravel 11
```bash
# clonar el repositorio
git clone https://github.com/jucampoc/ING2-1006538750.git

# nos dirigimos al proyecto
cd ING2-1006538750/

# nos dirigimos al api-gateway
cd api-gateway/

# Instalar dependencias PHP
composer install

# Copiar y configurar variables de entorno
cp .env.example .env
php artisan key:generate
```
### .env
```bash
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=api-gateway
DB_USERNAME=root
DB_PASSWORD=root

# URLs de Microservicios
MEDICAL_RECORDS_SERVICE_URL=[http://127.0.0.1:5000/api/medical-records](http://127.0.0.1:5000/api/medical-records)
# Los demás servicios usan URLs configuradas internamente en los ProxyControllers
```

```bash
# Crear tablas y cargar usuarios de prueba (julian@gmail.com / admin123)
php artisan migrate --seed

# iniciar servidor 
php artisan serv
```


## 2. Patient Service (Laravel 11) - Puerto 8001

Cada microservicio es autónomo. Asegúrese de que este servicio apunte a su propia base de datos:

```Bash
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=hospital-patients  # Base de datos específica del servicio
DB_USERNAME=root
DB_PASSWORD=root
```

```bahs
# Entrar al directorio
cd services/laravel-patient-service

# Instalar dependencias
composer install

# Configurar APP_KEY si no existe
php artisan key:generate

# Ejecutar migraciones y cargar Seeders
# Esto creará a los pacientes de prueba: Juan, María y Julian.
php artisan migrate --seed

# Iniciar el servicio en el puerto asignado
php artisan serve --port=8001
```
## 3. Notifications Service (Django) - Puerto 8002
Servicio especializado en la gestión de alertas y recordatorios para pacientes (SMS, Email, App) utilizando Django REST Framework y PostgreSQL.

### Configuración de Base de Datos
El servicio requiere una instancia de PostgreSQL corriendo localmente con las siguientes credenciales:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'notifications_db',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
### Instalación y Carga de Datos
```bash
# Entrar al directorio
cd services/django-notifications-service

# Instalar dependencias (Django, djangorestframework, psycopg2)
pip install django djangorestframework psycopg2-binary

# Ejecutar migraciones para crear la estructura en PostgreSQL
python manage.py migrate

# Cargar datos de prueba iniciales (Fixtures)
# Esto insertará notificaciones para los pacientes 1, 2 y 3
python manage.py loaddata fixtures/notifications.json

# Iniciar el servidor de desarrollo
python manage.py runserver 8002
```

### Seguridad y Middleware
Este servicio implementa un Middleware personalizado (InternalTokenMiddleware) que intercepta todas las peticiones para validar el token de comunicación interna.

- Validación: Si el header Authorization no coincide con Token miclave123, el servicio responde con un 403 Forbidden, protegiendo los datos de accesos directos no autorizados.

