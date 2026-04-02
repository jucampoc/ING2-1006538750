const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

const appointments = [
  {
    id: "001",
    patient_id: 1,
    doctor: "Dr. Gregory House",
    specialty: "Infectología",
    date: "2026-04-15",
    hour: "09:00",
    status: "confirmed"
  },
  {
    id: "002",
    patient_id: 2,
    doctor: "Dra. Meredith Grey",
    specialty: "Cirugía General",
    date: "2026-04-16",
    hour: "11:30",
    status: "pending"
  },
  {
    id: "003",
    patient_id: 3,
    doctor: "Dr. Shaun Murphy",
    specialty: "Pediatría",
    date: "2026-04-17",
    hour: "14:00",
    status: "confirmed"
  }
];

async function seed() {
  console.log("⏳ Cargando citas en Cloud Firestore...");
  const collectionRef = db.collection('appointments');

  for (const appt of appointments) {
    await collectionRef.doc(appt.id).set(appt);
    console.log(`✅ Cita ${appt.id} agregada`);
  }
  
  console.log("🚀 ¡Proceso terminado!");
  process.exit();
}

seed().catch(console.error);