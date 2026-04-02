from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from functools import wraps
from bson import json_util
from bson.objectid import ObjectId 
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")


if not MONGO_URI:
    raise ValueError("ERROR.")

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
    

@app.route('/api/medical-records/<record_id>', methods=['GET'])
@require_token
def get_record(record_id):
    try:
        record = records_collection.find_one({"_id": ObjectId(record_id)})
        if record:
            return json.loads(json_util.dumps(record)), 200
        return jsonify({"error": "Historial no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "ID inválido o error en el servidor"}), 400
    

@app.route('/api/medical-records/<record_id>', methods=['PUT'])
@require_token
def update_record(record_id):
    try:
        data = request.json
        result = records_collection.update_one({"_id": ObjectId(record_id)}, {"$set": data})
        if result.matched_count:
            return jsonify({"message": "Historial actualizado exitosamente"}), 200
        return jsonify({"error": "Historial no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "ID inválido o error en el servidor"}), 400

@app.route('/api/medical-records/<record_id>', methods=['DELETE'])
@require_token
def delete_record(record_id):
    try:
        result = records_collection.delete_one({"_id": ObjectId(record_id)})
        if result.deleted_count:
            return jsonify({"message": "Historial eliminado exitosamente"}), 200
        return jsonify({"error": "Historial no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "ID inválido o error en el servidor"}), 400


if __name__ == '__main__':
    puerto = int(os.getenv("PORT", 5000))
    print(f"Medical Records Service protegido corriendo en puerto {puerto}")
    app.run(port=puerto, debug=True)