from pymongo import MongoClient
import datetime

MONGO_URI = "mongodb+srv://admin:miclave123@ing2.pk2iepi.mongodb.net/hospital_db?appName=ing2"
client = MongoClient(MONGO_URI)
db = client['hospital_db'] 
records_collection = db['medical_records']


records = [
    {
        "patient_id": 1,
        "diagnosis": "Gripe común y fatiga",
        "treatment": "Reposo y Acetaminofén 500mg cada 8 horas",
        "doctor": "Dr. Gregory House",
        "date": datetime.datetime.now()
    },
    {
        "patient_id": 2,
        "diagnosis": "Post-operatorio estable",
        "treatment": "Limpieza de herida y control de dolor",
        "doctor": "Dra. Meredith Grey",
        "date": datetime.datetime.now()
    },
    {
        "patient_id": 3,
        "diagnosis": "Control de crecimiento sano",
        "treatment": "Continuar con dieta balanceada",
        "doctor": "Dr. Shaun Murphy",
        "date": datetime.datetime.now()
    }
]

def seed():
    print("⏳ Conectando a MongoDB Atlas...")
    records_collection.delete_many({}) 
    
    result = records_collection.insert_many(records)
    print(f"Se insertaron {len(result.inserted_ids)} historiales clínicos.")

if __name__ == "__main__":
    seed()