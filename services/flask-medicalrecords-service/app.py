from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from functools import wraps
from bson import json_util 
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")

# Validar que el URI realmente se haya cargado
if not MONGO_URI:
    raise ValueError("¡ALERTA ROJA! Python no pudo leer MONGO_URI del archivo .env. Revisa el nombre de la variable o si el archivo está guardado.")

client = MongoClient(MONGO_URI)
db = client.hospital_db
records_collection = db.medical_records

TOKEN_SECRETO = "miclave123"

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Token {TOKEN_SECRETO}":
            return jsonify({"error": "No autorizado. Acceso solo permitido desde el API Gateway."}), 403
        return f(*args, **kwargs)
    return decorated



@app.route('/api/medical-records', methods=['GET'])
@require_token
def get_records():
    try:
        records = list(records_collection.find())
        return json.loads(json_util.dumps(records)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/medical-records', methods=['POST'])
@require_token
def create_record():
    try:
        data = request.json
        result = records_collection.insert_one(data)
        return jsonify({
            "id": str(result.inserted_id), 
            "message": "Historial clínico creado exitosamente"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    puerto = int(os.getenv("PORT", 5000))
    print(f"Medical Records Service protegido corriendo en puerto {puerto}")
    app.run(port=puerto, debug=True)