# Medical Records Service — Flask

Microservicio encargado de la gestión de historiales clínicos de los
pacientes. Utiliza MongoDB Atlas como base de datos en la nube,
aprovechando su naturaleza schema-less para almacenar diagnósticos
y tratamientos de estructura variable.

**Puerto:** `5000` | **Framework:** Flask | **BD:** MongoDB Atlas

---

## Endpoints

Base URL en desarrollo local: `http://localhost:5000`
Base URL a través del Gateway: `http://localhost:8000`

Todos los endpoints requieren el header:
`Authorization: Token <TOKEN_SECRETO>`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/medical-records` | Listar todos los historiales |
| POST | `/api/medical-records` | Crear historial clínico |
| GET | `/api/medical-records/{id}` | Obtener por ID |
| PUT | `/api/medical-records/{id}` | Actualizar historial |
| DELETE | `/api/medical-records/{id}` | Eliminar historial |

### Ejemplo — Crear historial
```json
POST /api/medical-records
{
  "patient_id": 1,
  "diagnosis": "Hipertensión leve",
  "treatment": "Enalapril 10mg diario",
  "doctor": "Dr. Gregory House"
}
```

---

## Estructura

```text
flask-medicalrecords-service/
├── app.py                        # Servidor Flask y rutas
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env                          # Variables locales (no en repo)
├── seed_records.py               # Script carga datos iniciales
├── conftest.py                   # Configuración pytest
└── tests/
    ├── __init__.py
    └── test_app.py               # Pruebas unitarias
```

---

## Configuración local

### Requisitos
- Python 3.12+
- Cuenta de MongoDB Atlas con cluster activo

### Variables de entorno — `.env`
```bash
TOKEN_SECRETO=miclave123
MONGO_URI=mongodb+srv://admin:<password>@ing2.pk2iepi.mongodb.net/hospital_db?appName=ing2
PORT=5000
```

### Instalación
```bash
cd services/flask-medicalrecords-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Cargar datos de prueba en MongoDB Atlas
python seed_records.py

# Iniciar servidor
python app.py
```

---

## Ejecución con Docker

```bash
# Desde la raíz del proyecto
docker compose --env-file .env.docker up medicalrecords-service -d

# Ver logs
docker logs hospital-medicalrecords-service -f
```

Logs esperados al iniciar:
```bash
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
```

---

## Seguridad

Implementa el decorador `@require_token` que intercepta cada petición
y valida el header `Authorization` leyendo el token desde variables
de entorno:

```python
# app.py
TOKEN_SECRETO = os.getenv("TOKEN_SECRETO")
if not TOKEN_SECRETO:
    raise ValueError("La variable de entorno TOKEN_SECRETO no está definida.")

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Token {TOKEN_SECRETO}":
            return jsonify({
                "error": "No autorizado. Acceso solo permitido desde el API Gateway."
            }), 403
        return f(*args, **kwargs)
    return decorated
```

---

## Pruebas unitarias

```bash
cd services/flask-medicalrecords-service
pytest tests/ -v
```

MongoDB se mockea completamente con `unittest.mock` — no requiere
conexión real a Atlas durante las pruebas.

Las 5 pruebas cubren:

| # | Prueba | Qué verifica |
|---|---|---|
| 1 | `test_require_token_rechaza_sin_token` | Middleware retorna 403 sin token |
| 2 | `test_get_records_retorna_200` | GET lista historiales y retorna 200 |
| 3 | `test_create_record_retorna_201` | POST crea historial y retorna 201 |
| 4 | `test_get_record_by_id_retorna_200` | GET obtiene historial por ID |
| 5 | `test_delete_record_retorna_200` | DELETE elimina historial y retorna 200 |