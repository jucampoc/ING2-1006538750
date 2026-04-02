require('dotenv').config();
const express = require('express');
const admin = require("firebase-admin");
const cors = require("cors"); 


const serviceAccount = require("./serviceAccountKey.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();
const app = express();

app.use(cors()); 
app.use(express.json());

const TOKEN_SECRETO = "miclave123"; 

function requireToken(req, res, next) {
    const token = req.headers["authorization"]; 
    if (token !== `Token ${TOKEN_SECRETO}`) {    
        return res.status(403).json({ error: "No autorizado. Acceso solo permitido desde el API Gateway." }); 
    }
    next(); 
}


app.get('/api/appointments', requireToken, async (req, res) => {
    try {
        const snapshot = await db.collection('appointments').get();
        const appointments = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        res.json(appointments);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});


app.post('/api/appointments', requireToken, async (req, res) => {
    try {
        const docRef = await db.collection('appointments').add({
            patient_id: req.body.patient_id,
            doctor_name: req.body.doctor_name,
            appointment_date: req.body.appointment_date,
            reason: req.body.reason,
            status: req.body.status || "pending",
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });
        res.status(201).json({ id: docRef.id, message: "Cita Guardada" });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});


app.get('/api/appointments/:id', requireToken, async (req, res) => {
    try {
        const id = req.params.id;
        const doc = await db.collection('appointments').doc(id).get();
        
        if (!doc.exists) {
            return res.status(404).json({ error: "Cita no encontrada" });
        }
        
        res.json({ id: doc.id, ...doc.data() });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});


app.put('/api/appointments/:id', requireToken, async (req, res) => {
    try {
        const id = req.params.id;
        const dataToUpdate = req.body;
        const docRef = db.collection('appointments').doc(id);
        const doc = await docRef.get();

        if (!doc.exists) {
            return res.status(404).json({ error: "No se puede actualizar: Cita no encontrada" });
        }

        await docRef.update(dataToUpdate);
        res.status(200).json({ message: "Cita Actualizada exitosamente" });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});


app.delete('/api/appointments/:id', requireToken, async (req, res) => {
    try {
        const id = req.params.id;
        const docRef = db.collection('appointments').doc(id);
        const doc = await docRef.get();

        if (!doc.exists) {
            return res.status(404).json({ error: "No se puede eliminar: Cita no encontrada" });
        }

        await docRef.delete();
        res.status(200).json({ message: "Cita Eliminada exitosamente" });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(3000, () => console.log('Appointments Service protegido corriendo en puerto 3000'));