
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
# Seguridad
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
# Estructura del Proyecto

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

# Instalación y Configuración

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

- Validación: Si el header Authorization no coincide con `Token miclave123`, el servicio responde con un 403 Forbidden, protegiendo los datos de accesos directos no autorizados.


## 4. Appointments Service (Node.js/Express) - Puerto 3000
Servicio encargado de la gestión de citas médicas en tiempo real. Utiliza una arquitectura orientada a documentos con persistencia en la nube.
### Configuración de Cloud Firestore
A diferencia de los servicios anteriores, este microservicio no requiere una base de datos local. Utiliza Google Firebase:
- Archivo de Credenciales: Es obligatorio contar con el archivo **serviceAccountKey.json** en la raíz del servicio (obtenido desde la consola de Firebase).
- Base de Datos: Cloud Firestore en modo nativo.

### Instalación y Configuración
```bahs
# Entrar al directorio
cd services/express-appointments-service/

# Instalar dependencias (express, firebase-admin, dotenv, cors)
npm install

# Ejecutar el Script de Seeder
# Esto cargará las citas iniciales de los doctores House, Grey y Murphy en la nube
node seed_appointments.js

# Iniciar el servicio
node index.js
```
### Seguridad y Middleware
El servicio implementa la función requireToken, un middleware que valida de forma estricta el acceso desde el Gateway:
- Header Requerido: Authorization: `Token miclave123`
- Respuesta ante error: `403 No autorizado. Acceso solo permitido desde el API Gateway.`
## 5. Pharmacy Service (Node.js/Express) - Puerto 3001
Este microservicio se encarga de la gestión del inventario de la farmacia del hospital. Utiliza **MongoDB Atlas** para almacenar los documentos, lo que permite una estructura de datos flexible para los medicamentos.

### Configuración del archivo .env
```bash
PORT=3001
# La contraseña ha sido ocultada por seguridad. 
# Asegúrese de usar sus credenciales reales de Atlas.
MONGO_URI=mongodb+srv://admin:<password>@pharmacy.ptuxrkp.mongodb.net/?appName=pharmacy
TOKEN_INTERNO=miclave123
```

### Instalación y Ejecución
```bash
# Entrar al directorio del servicio
cd services/express-pharmacy-service

# Instalar dependencias (express, mongoose, cors, dotenv)
npm install

# Iniciar el servicio (se conectará automáticamente a MongoDB Atlas)
node index.js
```

### Seguridad Interna
Implementa el `authMiddleware`, el cual lee la variable `TOKEN_INTERNO` del `.env` y la compara con el header de la petición. Si no coincide, bloquea la solicitud con un código `403 Forbidden`, asegurando que solo el **API Gateway** pueda realizar operaciones de inventario.
## 6. Medical Records Service (Python/Flask) - Puerto 5000
Este microservicio gestiona los historiales clínicos de los pacientes. Utiliza **Python (Flask)** y **MongoDB Atlas**, aprovechando la naturaleza schema-less (sin esquema) de NoSQL para almacenar diagnósticos y tratamientos que pueden variar ampliamente en su estructura.

### Configuración del archivo .env
El servicio requiere la cadena de conexión a su respectiva base de datos en MongoDB Atlas y la definición del puerto.
```bash
PORT=5000
# La contraseña ha sido ocultada por seguridad. 
# Asegúrese de usar sus credenciales reales.
MONGO_URI=mongodb+srv://admin:<password>@ing2.pk2iepi.mongodb.net/hospital_db?appName=ing2
```

### Instalación y Carga de Datos
Gracias a que el servicio cuenta con su archivo `requirements.txt`, la instalación de dependencias es directa.
```bash
# Entrar al directorio
cd services/flask-medicalrecords-service

# (Opcional pero recomendado) Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias (Flask, PyMongo, python-dotenv, etc.)
pip install -r requirements.txt

# Ejecutar el script de semillas para limpiar la BD y cargar 3 historiales de prueba
python seed_records.py

# Iniciar el servidor Flask
python app.py
```
### Seguridad Interna
Implementa el decorador personalizado `@require_token` en Python. Este *wrapper* intercepta la petición antes de ejecutar la función de la ruta, validando el header `Authorization`. Si el token no es válido, retorna un error `403 Forbidden`.

# Referencia de Endpoints (API Gateway)
El API Gateway es el único punto de entrada público del sistema. Todas las peticiones deben realizarse a http://localhost:8000, y el Gateway se encargará de enrutarlas al microservicio correspondiente.

### Autenticación (Rutas Públicas)
Estas rutas no requieren token y se utilizan para la gestión de acceso de los usuarios del sistema.
| Método | Endpoint | Descripción | Body (JSON)
| :--- | :--- | :--- | :--- |
POST | `/api/login` | Autentica al usuario y devuelve el token de acceso. | `email`, `password`
POST | `/api/register` | Crea un nuevo usuario en el sistema. | `name`, `email`, `password`, `password_confirmation`

### Servicios Integrados (Rutas Protegidas)
**Requisito estricto:** Todas las peticiones a estas rutas deben incluir el header de autorización de Laravel Sanctum obtenido en el Login:
`Authorization: Bearer <tu_token_aqui>`

**Pacientes (Patient Service)**
- **GET** `/api/patients` - Lista todos los pacientes.
- **POST** `/api/patients` - Crea un paciente.
- **GET** `/api/patients/{id}` - Obtiene detalles de un paciente.
- **PUT** `/api/patients/{id}` - Actualiza un paciente.
- **DELETE** `/api/patients/{id}` - Elimina un paciente.

**Citas Médicas (Appointments Service)**
- **GET** `/api/appointments` - Lista todos las citas.
- **POST** `/api/appointments` - Crea una nueva cita.
- **GET** `/api/appointments/{id}` - Obtiene una cita por ID.
- **PUT** `/api/appointments/{id}` - Actualiza estado/fecha de la cita.
- **DELETE** `/api/appointments/{id}` - Cancela/Elimina una cita.

**Farmacia (Pharmacy Service)**
- **GET** `/api/pharmacy` - Catálogo completo de medicamentos.
- **POST** `/api/pharmacy` - Añade un nuevo medicamento al inventario.
- **GET** `/api/pharmacy/{id}` - Detalle de un medicamento.
- **PUT** `/api/pharmacy/{id}` - Actualiza precio o stock.
- **DELETE** `/api/pharmacy/{id}` - Retira un medicamento.

**Historial Clínico (Medical Records Service)**
- **GET** `/api/medical-records` - Lista los historiales clínicos.
- **POST** `/api/medical-records` - Agrega un nuevo registro o diagnóstico.
- **GET** `/api/medical-records/{id}` - Busca un historial por ID.
- **PUT** `/api/medical-records/{id}` - Actualiza tratamiento/diagnóstico.
- **DELETE** `/api/medical-records/{id}` - Elimina un registro clínico.

### Cerrar Sesión

| Método | Endpoint | Descripción | Requiere
| :--- | :--- | :--- | :--- |
POST | `/api/logout` | Revoca el token de acceso actual del usuario. | Bearer Token

### Ejemplo de Petición (Thunder Client / Postman)
Si desea crear una cita médica, debe configurar tu cliente REST de la siguiente manera:

**URL**: POST `http://localhost:8000/api/appointments`

**Headers**
```bash
Accept: application/json
Content-Type: application/json
Authorization: Bearer 1|abcdef1234567890...
```

**Body (JSON)**
```json
{
  "patient_id": 3,
  "doctor_name": "Dr. Shaun Murphy",
  "appointment_date": "2026-05-20",
  "reason": "Revisión general",
  "status": "pending"
}
```


# Flujo de Petición (Ejemplo: Crear una Cita Médica)
El siguiente esquema demuestra el ciclo de vida de una petición dentro del sistema, evidenciando el funcionamiento de las dos capas de seguridad (Sanctum y Shared Secret).

```bash
1. [CLIENTE]  POST /api/appointments  + Authorization: Bearer <Token_Sanctum>
       │
       ▼
2. [GATEWAY]  Middleware auth:sanctum valida el token del cliente
              ✓ Token válido → continuar
              ✗ Token inválido/ausente → 401 Unauthenticated
       │
       ▼
3. [GATEWAY]  AppointmentProxyController (o equivalente) recibe la solicitud
              • Extrae los datos del body (patient_id, doctor_name, etc.)
              • Inyecta header interno: Authorization: Token miclave123
       │
       ▼
4. [GATEWAY → EXPRESS]  HTTP POST http://localhost:3000/api/appointments
                        Headers: Authorization: Token miclave123
                        Body: { patient_id: 3, doctor_name: "Dr. Shaun Murphy"... }
       │
       ▼
5. [EXPRESS]  Middleware requireToken (Capa 2) valida el Token Interno
              ✓ Clave válida → continuar
              ✗ Clave inválida/ausente → 403 Forbidden (Acceso denegado. Solo Gateway...)
       │
       ▼
6. [EXPRESS]  Ruta POST /api/appointments
              • Asigna el serverTimestamp() actual
              • Guarda el nuevo documento en Google Cloud Firestore
              • Retorna el ID del documento generado
       │
       ▼
7. [GATEWAY]  Recibe respuesta del microservicio Express (Status 201)
              • Retorna la respuesta transparente al cliente original
       │
       ▼
8. [CLIENTE]  Recibe confirmación HTTP 201 Created: { "id": "doc_id_firebase", "message": "Cita Guardada" }
```
# Guía de Pruebas (Thunder Client / Postman)
A continuación se presenta un flujo de trabajo completo para probar la integración de todo el sistema a través del API Gateway.

**Paso 1 — Registrar un Usuario (Médico/Admin)**
- Método: `POST`
- URL: `http://localhost:8000/api/register`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "name": "Julian",
  "email": "julian@gmail.com",
  "password": "password123",
  "password_confirmation": "password123"
}
```
**Paso 2 — Login (Obtener Token Sanctum)**
- Método: `POST`
- URL: `http://localhost:8000/api/login`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "email": "julian@gmail.com",
  "password": "password123"
}
```
 *Acción requerida:* Copiar el valor del campo token de la respuesta JSON para usarlo en los siguientes pasos.

**Paso 3 — Registrar un Paciente**
- Método: `POST`
- URL: `http://localhost:8000/api/patients`
- Headers: 
    - `Authorization: Bearer <token_copiado>`
    - `Content-Type: application/json`


- Body:
```json
{
    "name": "Ana",
    "last_name": "López",
    "identity_document": "1020304050",
    "birthday": "1995-08-15",
    "phone": "3009876543",
    "blood_type": "O+"
}
```
*Nota:* Anota el id del paciente devuelto en la respuesta (ej. 4).

**Paso 4 — Verificar Datos del Paciente**
Método: GET

- URL: `http://localhost:8000/api/patients/4` (Reemplaza '4' por el ID obtenido en el Paso 3)
- Headers:
    - Authorization: `Bearer <token_copiado>`

**Paso 5 — Agendar una Cita Médica (Firestore)**
- Método: `POST`
- URL: `http://localhost:8000/api/appointments`
- Headers:
    - `Authorization: Bearer <token_copiado>`
    - `Content-Type: application/json`
- Body:
```json
{
    "patient_id": 4, 
    "doctor_name": "Dr. Gregory House",
    "appointment_date": "2026-04-20",
    "reason": "Migraña crónica",
    "status": "pending"
}
```
*Nota:* (Recuerda reemplaza '4' por el ID obtenido en el Paso 3)

**Paso 6 — Crear Historial Clínico (MongoDB)**
- Método: `POST`
- URL: `http://localhost:8000/api/medical-records`
- Headers:
    - `Authorization: Bearer <token_copiado>`
    - `Content-Type: application/json`
- Body:
```json
{
    "patient_id": 4,
    "diagnosis": "Migraña crónica severa",
    "treatment": "Ibuprofeno 400mg cada 8 horas y reposo en habitación oscura",
    "doctor": "Dr. Gregory House"
}
```
*Nota:* (Recuerda reemplaza '4' por el ID obtenido en el Paso 3)

**Paso 7 — Cerrar Sesión**
- Método: `POST`
- URL: `http://localhost:8000/api/logout`
- Headers:
    - `Authorization: Bearer <token_copiado>`

Al ejecutar este paso, el token actual será revocado en la base de datos del Gateway, y cualquier petición posterior a los microservicios será denegada con un error `401 Unauthenticated`.
# Bases de Datos

El sistema utiliza un enfoque de persistencia políglota, seleccionando el motor de base de datos más adecuado para las necesidades específicas de cada microservicio.

| Componente | Motor | Uso |
| :--- | :--- | :--- |
| **API Gateway** | MySQL (Local) | Usuarios administradores y tokens de acceso (Sanctum) |
| **Patients Service** | MySQL (Local) | Datos demográficos estructurados de pacientes |
| **Notifications Service** | PostgreSQL (Local) | Registro transaccional de notificaciones y alertas |
| **Appointments Service** | Firebase Cloud Firestore | Gestión de citas médicas (documentos en tiempo real) |
| **Pharmacy Service** | MongoDB Atlas | Inventario y catálogo de medicamentos |
| **Med. Records Service** | MongoDB Atlas | Historiales clínicos (documentos flexibles sin esquema estricto) |

---

## Variables de Entorno Resumen

Las configuraciones sensibles se manejan a través de archivos `.env` en cada servicio. A continuación, se describen las variables más críticas:

| Variable | Servicio(s) | Descripción |
| :--- | :--- | :--- |
| `DB_CONNECTION` | Gateway, Patients | Define el motor relacional (mysql) |
| `DB_DATABASE` | Gateway, Patients, Notif. | Nombre de la base de datos local |
| `TOKEN_SECRETO` / `TOKEN_INTERNO` | Microservicios | Clave compartida para validar peticiones del Gateway (`miclave123`) |
| `MONGO_URI` | Pharmacy, Med. Records | URI de conexión a la base de datos en MongoDB Atlas |
| `PORT` | Express, Flask | Define el puerto local de ejecución del microservicio |
| `serviceAccountKey.json` | Appointments | Archivo JSON (credenciales) para conexión con Google Firebase |

---

## Tecnologías Utilizadas

El monorepo integra múltiples lenguajes y frameworks para demostrar interoperabilidad.

| Componente | Tecnología | Lenguaje | Puerto |
| :--- | :--- | :--- | :--- |
| **API Gateway** | Laravel 11 | PHP 8.2+ | `8000` |
| **Patients Service** | Laravel 11 | PHP 8.2+ | `8001` |
| **Notifications Service** | Django 5 | Python 3 | `8002` |
| **Appointments Service** | Express.js | Node.js | `3000` |
| **Pharmacy Service** | Express.js | Node.js | `3001` |
| **Medical Records Service** | Flask | Python 3 | `5000` |
| **Bases de Datos Relacionales** | MySQL, PostgreSQL | SQL | `3306`, `5432` |
| **Bases de Datos NoSQL** | MongoDB, Firestore | BSON / JSON | Cloud |
| **Autenticación Externa** | Laravel Sanctum | - | - |
| **Autenticación Interna** | Shared Token Middleware | - | - |