import pytest
from unittest.mock import MagicMock
from bson.objectid import ObjectId

MOCK_ID     = str(ObjectId())
VALID_TOKEN = 'Token miclave123'


# ─── PRUEBA 1: Middleware rechaza petición sin token ──────────────────────────
def test_require_token_rechaza_sin_token(client):
    res = client.get('/api/medical-records')

    assert res.status_code == 403
    assert res.get_json()['error'] == \
        'No autorizado. Acceso solo permitido desde el API Gateway.'


# ─── PRUEBA 2: GET lista todos los historiales clínicos ───────────────────────
def test_get_records_retorna_200(client):
    mock_record = {
        '_id':        ObjectId(MOCK_ID),
        'patient_id': 1,
        'diagnosis':  'Hipertensión',
        'doctor':     'Dr. Gregory House'
    }
    client._mock_collection.find.return_value = [mock_record]

    res = client.get(
        '/api/medical-records',
        headers={'Authorization': VALID_TOKEN}
    )

    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
    client._mock_collection.find.assert_called_once()


# ─── PRUEBA 3: POST crea un historial y retorna 201 ───────────────────────────
def test_create_record_retorna_201(client):
    client._mock_collection.insert_one.return_value = MagicMock(
        inserted_id=ObjectId(MOCK_ID)
    )

    payload = {
        'patient_id': 2,
        'diagnosis':  'Diabetes tipo 2',
        'doctor':     'Dra. Meredith Grey',
        'treatment':  'Metformina 500mg'
    }

    res = client.post(
        '/api/medical-records',
        json=payload,
        headers={'Authorization': VALID_TOKEN}
    )

    assert res.status_code == 201
    assert res.get_json()['id'] == MOCK_ID
    assert res.get_json()['message'] == 'Historial clínico creado exitosamente'


# ─── PRUEBA 4: GET por ID retorna el historial correcto ───────────────────────
def test_get_record_by_id_retorna_200(client):
    mock_record = {
        '_id':        ObjectId(MOCK_ID),
        'patient_id': 3,
        'diagnosis':  'Fractura de tibia',
        'doctor':     'Dr. Shaun Murphy'
    }
    client._mock_collection.find_one.return_value = mock_record

    res = client.get(
        f'/api/medical-records/{MOCK_ID}',
        headers={'Authorization': VALID_TOKEN}
    )

    assert res.status_code == 200
    client._mock_collection.find_one.assert_called_once_with(
        {'_id': ObjectId(MOCK_ID)}
    )


# ─── PRUEBA 5: DELETE elimina un historial y retorna 200 ──────────────────────
def test_delete_record_retorna_200(client):
    client._mock_collection.delete_one.return_value = MagicMock(deleted_count=1)

    res = client.delete(
        f'/api/medical-records/{MOCK_ID}',
        headers={'Authorization': VALID_TOKEN}
    )

    assert res.status_code == 200
    assert res.get_json()['message'] == 'Historial eliminado exitosamente'