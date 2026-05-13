# Documentación Docker — Sistema de Gestión Hospitalaria

---

## Arquitectura de contenedores

El sistema levanta 8 contenedores en la red interna `hospital-network`:

| Contenedor | Imagen base | Puerto externo | Puerto interno |
|---|---|---|---|
| `hospital-api-gateway` | `php:8.4-fpm-alpine` | `8000` | `8000` |
| `hospital-patient-service` | `php:8.4-fpm-alpine` | `8001` | `8001` |
| `hospital-notifications-service` | `python:3.12-slim` | `8002` | `8002` |
| `hospital-appointments-service` | `node:20-alpine` | `3000` | `3000` |
| `hospital-pharmacy-service` | `node:20-alpine` | `3001` | `3001` |
| `hospital-medicalrecords-service` | `python:3.12-slim` | `5000` | `5000` |
| `hospital-mysql` | `mysql:8.0` | `3307` | `3306` |
| `hospital-postgres` | `postgres:14-alpine` | `5433` | `5432` |

> MySQL y PostgreSQL exponen puertos alternativos al exterior para evitar
> conflictos con instalaciones locales de Windows/XAMPP.

---

## Red interna

Dentro de Docker los servicios se comunican por **nombre de contenedor**,
no por `localhost`. El Gateway usa estas URLs internas:
```text
http://patient-service:8001
http://notifications-service:8002
http://appointments-service:3000
http://pharmacy-service:3001
http://medicalrecords-service:5000
http://mysql:3306
http://postgres:5432
```

Desde tu máquina accedes por `localhost` con el puerto externo:
```text
http://localhost:8000  →  API Gateway
http://localhost:3307  →  MySQL (cliente externo como DBeaver)
http://localhost:5433  →  PostgreSQL (cliente externo)
```

---

## Volúmenes

| Volumen | Contenedor | Datos |
|---|---|---|
| `mysql_data` | `hospital-mysql` | BD `api_gateway` y `hospital_patients` |
| `postgres_data` | `hospital-postgres` | BD `notifications_db` |

MongoDB Atlas y Firebase son servicios en la nube — sin volúmenes locales.

---

## Variables de entorno

Todas se definen en `.env.docker` en la raíz. Nunca se sube al repositorio.

| Variable | Contenedor(es) | Descripción |
|---|---|---|
| `TOKEN_SECRETO` | Todos los microservicios | Token compartido Gateway↔Servicios |
| `MYSQL_ROOT_PASSWORD` | mysql, api-gateway, patient-service | Contraseña root MySQL |
| `MYSQL_GATEWAY_DB` | mysql, api-gateway | Nombre BD Gateway |
| `MYSQL_PATIENTS_DB` | mysql, patient-service | Nombre BD Patients |
| `POSTGRES_DB` | postgres, notifications-service | Nombre BD Notifications |
| `POSTGRES_USER` | postgres, notifications-service | Usuario PostgreSQL |
| `POSTGRES_PASSWORD` | postgres, notifications-service | Contraseña PostgreSQL |
| `MONGO_URI_PHARMACY` | pharmacy-service | URI MongoDB Atlas Pharmacy |
| `MONGO_URI_RECORDS` | medicalrecords-service | URI MongoDB Atlas Medical Records |
| `GATEWAY_APP_KEY` | api-gateway | Laravel APP_KEY |
| `PATIENTS_APP_KEY` | patient-service | Laravel APP_KEY |

---

## Healthchecks

MySQL y PostgreSQL tienen healthchecks configurados. Los microservicios
que dependen de ellos esperan a que estén listos antes de arrancar.

```bash
# Verificar estado de todos los contenedores
docker compose --env-file .env.docker ps
```

Estado esperado:
```bash
hospital-mysql     Up (healthy)
hospital-postgres  Up (healthy)
hospital-*         Up
```

---

## Troubleshooting

### Contenedor en estado Restarting
```bash
docker logs hospital-<servicio> --tail=30
```

### Error de conexión a MySQL desde un servicio Laravel
```bash
# Verificar que MySQL esté healthy
docker compose --env-file .env.docker ps

# Probar conexión desde dentro del contenedor
docker exec -it hospital-api-gateway php artisan db:show
```

### Error de autenticación MongoDB Atlas
La contraseña en `MONGO_URI_PHARMACY` o `MONGO_URI_RECORDS` tiene el
placeholder `<password>`. Edita `.env.docker` y reinicia:
```bash
docker compose --env-file .env.docker up \
  pharmacy-service medicalrecords-service -d --force-recreate
```

### Puerto 3306 o 5432 en uso
XAMPP local ocupa estos puertos. El compose ya los mapea a `3307` y `5433`.
Si persiste el conflicto, detén MySQL/PostgreSQL desde el panel de XAMPP.

### Reconstruir desde cero
```bash
docker compose --env-file .env.docker down -v
docker rmi $(docker images "ing2-1006538750*" -q) 2>/dev/null
docker system prune -f
docker compose --env-file .env.docker build --no-cache
docker compose --env-file .env.docker up -d
```

### Entrar a un contenedor
```bash
docker exec -it hospital-api-gateway sh
docker exec -it hospital-notifications-service bash
```