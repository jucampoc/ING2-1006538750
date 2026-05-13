---

## Modelo de datos

```javascript
// models/Medicine.js
{
  name:        String (requerido),
  description: String,
  stock:       Number (requerido, default: 0),
  price:       Number (requerido),
  category:    String (default: 'General'),
  createdAt:   Date,
  updatedAt:   Date
}
```

---

## Seguridad

Implementa `authMiddleware` que valida el header `Authorization`
en cada petición leyendo el token desde variables de entorno:

```javascript
// index.js
const TOKEN_INTERNO = process.env.TOKEN_SECRETO;
if (!TOKEN_INTERNO) {
    console.error("ERROR: TOKEN_SECRETO no está definida.");
    process.exit(1);
}

const authMiddleware = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    if (authHeader !== `Token ${TOKEN_INTERNO}`) {
        return res.status(403).json({
            error: "Acceso denegado. Solo Gateway permitido."
        });
    }
    next();
};
```

---

## Pruebas unitarias

```bash
cd services/express-pharmacy-service
npm test
```

Mongoose se mockea completamente — no requiere conexión real
a MongoDB Atlas durante las pruebas.

Las 5 pruebas cubren:

| # | Prueba | Qué verifica |
|---|---|---|
| 1 | `GET /api/pharmacy sin token` | Middleware retorna 403 sin token |
| 2 | `GET /api/pharmacy con token válido` | Lista medicamentos y retorna 200 |
| 3 | `POST /api/pharmacy con datos válidos` | Crea medicamento y retorna 201 |
| 4 | `PUT /api/pharmacy/:id con datos válidos` | Actualiza medicamento y retorna 200 |
| 5 | `DELETE /api/pharmacy/:id con token válido` | Elimina medicamento y retorna 200 |