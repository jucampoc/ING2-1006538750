# Sistema de Gestión Hospitalaria — Microservicios
**Ingeniería de Software II — Julian Camilo Campo Cabrera**

---

## Descripción General

Sistema hospitalario basado en arquitectura de microservicios. Todas las 
peticiones externas pasan obligatoriamente por un API Gateway centralizado 
que gestiona autenticación y enrutamiento hacia los servicios internos.

---

## Arquitectura del Sistema

```text
        +-----------------------------------------------------------+
        |                     CLIENTES (REST)                       |
        |              (Thunder Client / Postman / curl)            |
        +----------------------------+------------------------------+
                                     |
                                     | HTTP (Port 8000)
                                     v
        +----------------------------+------------------------------+
        |                     API GATEWAY                           |
        |              Laravel 11 — Port: 8000                      |
        |     [ Autenticación Sanctum ] [ Proxy Routing ]           |
        +------+----------+----------+-----------+----------+-------+
               |          |          |           |          |
               v          v          v           v          v
        +------+--+ +-----+---+ +----+----+ +----+---+ +---+------+
        |PATIENTS | |NOTIFIC. | |APPOINT. | |PHARMACY| |MED.REC.  |
        |Laravel  | |Django   | |Express  | |Express | |Flask     |
        |Port:8001| |Port:8002| |Port:3000| |Port:3001| |Port:5000|
        +------+--+ +-----+---+ +----+----+ +----+---+ +---+------+
               |          |          |           |          |
               v          v          v           v          v
           MySQL      PostgreSQL  Firestore   MongoDB    MongoDB
          (Docker)    (Docker)    (Cloud)     (Atlas)    (Atlas)
```

---

## Tecnologías

| Componente | Tecnología | Lenguaje | Puerto |
|---|---|---|---|
| **API Gateway** | Laravel 11 | PHP 8.4 | `8000` |
| **Patients Service** | Laravel 11 | PHP 8.4 | `8001` |
| **Notifications Service** | Django 5 | Python 3.12 | `8002` |
| **Appointments Service** | Express.js | Node.js 20 | `3000` |
| **Pharmacy Service** | Express.js | Node.js 20 | `3001` |
| **Medical Records Service** | Flask | Python 3.12 | `5000` |
| **MySQL** | Docker `mysql:8.0` | SQL | `3307` |
| **PostgreSQL** | Docker `postgres:14` | SQL | `5433` |
| **MongoDB Atlas** | Cloud | NoSQL | Cloud |
| **Firebase Firestore** | Cloud | NoSQL | Cloud |

---

## Estructura del Repositorio

```text
ING2-1006538750/
├── docker-compose.yml
├── .env.docker
├── locustfile.py
├── docker/
│   ├── mysql/init.sql
│   └── entrypoints/
│       ├── gateway-entrypoint.sh
│       └── patient-entrypoint.sh
├── api-gateway/                  → ver api-gateway/README.md
├── docs/
│   └── docker.md                 → documentación detallada de Docker
└── services/
    ├── laravel-patient-service/      → ver services/laravel-patient-service/README.md
    ├── django-notifications-service/ → ver services/django-notifications-service/README.md
    ├── express-appointments-service/ → ver services/express-appointments-service/README.md
    ├── express-pharmacy-service/     → ver services/express-pharmacy-service/README.md
    └── flask-medicalrecords-service/ → ver services/flask-medicalrecords-service/README.md
```

---

## Seguridad

Dos capas de autenticación protegen el sistema:

**Capa 1 — Cliente → Gateway:** Laravel Sanctum con Bearer Token.

**Capa 2 — Gateway → Microservicios:** Shared Secret (`TOKEN_SECRETO`) 
inyectado por el Gateway en cada petición interna. Los microservicios 
rechazan cualquier acceso directo con `403 Forbidden`.

---

## Despliegue con Docker Compose

### Requisitos
- Docker Desktop 4.0+ con WSL2 Integration (Windows)
- Docker Engine 24.0+ (Linux/Mac)
- Credenciales de MongoDB Atlas
- Archivo `serviceAccountKey.json` de Firebase

### Configuración

Crea el archivo `.env.docker` en la raíz del proyecto con las siguientes
variables — consulta `docs/docker.md` para descripción detallada de cada una:

```bash
TOKEN_SECRETO=miclave123
MYSQL_ROOT_PASSWORD=root
MYSQL_GATEWAY_DB=api_gateway
MYSQL_PATIENTS_DB=hospital_patients
POSTGRES_DB=notifications_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
MONGO_URI_PHARMACY=mongodb+srv://admin:<password>@pharmacy.ptuxrkp.mongodb.net/?appName=pharmacy
MONGO_URI_RECORDS=mongodb+srv://admin:<password>@ing2.pk2iepi.mongodb.net/hospital_db?appName=ing2
GATEWAY_APP_KEY=base64:TU_KEY_AQUI
PATIENTS_APP_KEY=base64:TU_KEY_AQUI
```

Coloca el archivo `serviceAccountKey.json` en:
```bash
services/express-appointments-service/serviceAccountKey.json
```

### Levantar el sistema

```bash
# Construir imágenes
docker compose --env-file .env.docker build

# Levantar todos los servicios
docker compose --env-file .env.docker up -d

# Verificar estado
docker compose --env-file .env.docker ps
```

### Comandos útiles

```bash
# Ver logs de un servicio
docker logs hospital-api-gateway -f

# Reiniciar un servicio
docker compose --env-file .env.docker restart api-gateway

# Detener sin borrar datos
docker compose --env-file .env.docker down

# Detener y borrar volúmenes
docker compose --env-file .env.docker down -v
```

> Para instrucciones detalladas de pruebas y troubleshooting 
> consulta [`docs/docker.md`](docs/docker.md).

---

## Puertos

| Servicio | Puerto |
|---|---|
| API Gateway | `8000` |
| Patient Service | `8001` |
| Notifications Service | `8002` |
| Appointments Service | `3000` |
| Pharmacy Service | `3001` |
| Medical Records Service | `5000` |
| MySQL (externo) | `3307` |
| PostgreSQL (externo) | `5433` |