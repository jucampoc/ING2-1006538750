require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const Medicine = require('./models/Medicine');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;
const TOKEN_INTERNO = process.env.TOKEN_INTERNO;

const authMiddleware = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    if (authHeader !== `Token ${TOKEN_INTERNO}`) {
        return res.status(403).json({ error: "Acceso denegado. Solo Gateway permitido." });
    }
    next();
};


// 1. Obtener todos los medicamentos
app.get('/api/pharmacy', authMiddleware, async (req, res) => {
    try {
        const medicines = await Medicine.find();
        res.json(medicines);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// 2. Crear un medicamento
app.post('/api/pharmacy', authMiddleware, async (req, res) => {
    try {
        const medicine = new Medicine(req.body);
        await medicine.save();
        res.status(201).json(medicine);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// 3. Actualizar medicamento (Stock/Precio)
app.put('/api/pharmacy/:id', authMiddleware, async (req, res) => {
    try {
        const updated = await Medicine.findByIdAndUpdate(req.params.id, req.body, { new: true });
        res.json(updated);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// 4. Eliminar medicamento
app.delete('/api/pharmacy/:id', authMiddleware, async (req, res) => {
    try {
        await Medicine.findByIdAndDelete(req.params.id);
        res.json({ message: "Medicamento eliminado correctamente" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


// CONEXIÓN A BD Y EXPORTACIÓN DE APP
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log("Conectado a MongoDB Atlas - Base de Datos: Pharmacy");
        if (process.env.NODE_ENV !== 'test') {
            app.listen(PORT, () => console.log(`Servicio Farmacia en puerto ${PORT}`));
        }
    })
    .catch(err => console.error("Error de conexión:", err));
module.exports = app; 


mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log("Conectado a MongoDB Atlas - Base de Datos: Pharmacy");
        app.listen(PORT, () => console.log(`Servicio Farmacia en puerto ${PORT}`));
    })
    .catch(err => console.error("Error de conexión:", err));