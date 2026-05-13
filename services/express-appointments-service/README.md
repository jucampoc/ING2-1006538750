# Appointments Service — Express.js

Microservicio encargado de la gestión de citas médicas en tiempo real.
Utiliza Google Cloud Firestore como base de datos en la nube.

**Puerto:** `3000` | **Framework:** Express.js | **BD:** Firebase Firestore

---

## Endpoints

Base URL en desarrollo local: `http://localhost:3000`
Base URL a través del Gateway: `http://localhost:8000`

Todos los endpoints requieren el header:
`Authorization: Token <TOKEN_SECRETO>`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/appointments` | Listar todas las citas |
| POST | `/api/appointments` | Crear una cita |
| GET | `/api/appointments/{id}` | Obtener por ID |
| PUT | `/api/appointments/{id}` | Actualizar cita |
| DELETE | `/api/appointments/{id}` | Eliminar cita |

### Ejemplo — Crear cita
```json
POST /api/appointments
{
  "patient_id": 1,
  "doctor_name": "Dr. Gregory House",
  "appointment_date": "2026-06-15",
  "reason": "Consulta general",
  "status": "pending"
}
```

Valores válidos para `status`: `pending`, `confirmed`, `cancelled`

---

## Estructura

```text
express-appointments-service/
├── index.js                      # Servidor Express y rutas
├── package.json
├── Dockerfile
├── .dockerignore
├── .env                          # Variables locales (no en repo)
├── serviceAccountKey.json        # Credenciales Firebase (no en repo)
├── seed_appointments.js          # Script carga datos iniciales
└── tests/
    └── appointments.test.js      # Pruebas unitarias
```

---

## Configuración local

### Requisitos
- Node.js 20+
- Cuenta de Firebase con Firestore habilitado
- Archivo `serviceAccountKey.json` obtenido desde Firebase Console

### Obtener `serviceAccountKey.json`
1. Entra a [console.firebase.google.com](https://console.firebase.google.com)
2. Selecciona tu proyecto
3. Ve a **Configuración del proyecto** → **Cuentas de servicio**
4. Haz clic en **Generar nueva clave privada**
5. Guarda el archivo como `serviceAccountKey.json` en la raíz del servicio

### Variables de entorno — `.env`
```bash
TOKEN_SECRETO=miclave123
```

### Instalación
```bash
cd services/express-appointments-service

# Instalar dependencias
npm install

# Cargar datos de prueba en Firestore
node seed_appointments.js

# Iniciar servidor
node index.js
```

---

## Ejecución con Docker

El `serviceAccountKey.json` se monta como volumen de solo lectura
en el contenedor — nunca se copia dentro de la imagen.

```bash
# Desde la raíz del proyecto
docker compose --env-file .env.docker up appointments-service -d

# Ver logs
docker logs hospital-appointments-service -f
```

### Requisito obligatorio para Docker
El archivo `serviceAccountKey.json` debe existir antes de levantar
el contenedor:

```bash
# Verificar que existe
ls services/express-appointments-service/serviceAccountKey.json
```

---

## Seguridad

Implementa la función `requireToken` como middleware que valida
el header `Authorization` en cada petición:

```javascript
// index.js
const TOKEN_SECRETO = process.env.TOKEN_SECRETO;
if (!TOKEN_SECRETO) {
    console.error("ERROR: TOKEN_SECRETO no está definida.");
    process.exit(1);
}

function requireToken(req, res, next) {
    const token = req.headers["authorization"];
    if (token !== `Token ${TOKEN_SECRETO}`) {
        return res.status(403).json({
            error: "No autorizado. Acceso solo permitido desde el API Gateway."
        });
    }
    next();
}
```

---

## Pruebas unitarias

```bash
cd services/express-appointments-service
npm test
```

Firebase Admin se mockea completamente — no requiere conexión real
a Firestore durante las pruebas.

Las 5 pruebas cubren:

| # | Prueba | Qué verifica |
|---|---|---|
| 1 | `GET /api/appointments sin token` | Middleware retorna 403 sin token |
| 2 | `GET /api/appointments con token válido` | Lista citas y retorna 200 |
| 3 | `POST /api/appointments con datos válidos` | Crea cita y retorna 201 |
| 4 | `GET /api/appointments/:id con token válido` | Obtiene cita por ID |
| 5 | `DELETE /api/appointments/:id con token válido` | Elimina cita y retorna 200 |