const request = require('supertest');

jest.mock('firebase-admin', () => {
    const appointmentData = {
        patient_id: 1,
        doctor_name: 'Dr. Gregory House',
        appointment_date: '2026-04-15',
        reason: 'Consulta general',
        status: 'pending'
    };

    const mockDoc = {
        exists: true,
        id:     'abc123',
        data:   () => appointmentData
    };

    const mockDocRef = {
        get:    jest.fn().mockResolvedValue(mockDoc),
        update: jest.fn().mockResolvedValue({}),
        delete: jest.fn().mockResolvedValue({})
    };

    const mockCollection = {
        get: jest.fn().mockResolvedValue({
            docs: [{ id: 'abc123', data: () => appointmentData }]
        }),
        add: jest.fn().mockResolvedValue({ id: 'nuevo-id-123' }),
        doc: jest.fn(() => mockDocRef)
    };

    return {
        initializeApp:  jest.fn(),
        credential:     { cert: jest.fn() },
        firestore:      Object.assign(jest.fn(() => ({ collection: jest.fn(() => mockCollection) })), {
            FieldValue: { serverTimestamp: jest.fn(() => 'mock-timestamp') }
        })
    };
});

// Credenciales para que no sea necesario en el entorno de prueba
jest.mock('../serviceAccountKey.json', () => ({
    type:         'service_account',
    project_id:   'mock-project',
    private_key:  '-----BEGIN RSA PRIVATE KEY-----\nMOCK\n-----END RSA PRIVATE KEY-----\n',
    client_email: 'mock@mock-project.iam.gserviceaccount.com'
}), { virtual: true });

const app = require('../index');

const VALID_TOKEN   = 'Token miclave123';
const INVALID_TOKEN = 'Token invalido';

// PRUEBA 1: Middleware rechaza petición sin token
test('GET /api/appointments sin token debe retornar 403', async () => {
    const res = await request(app).get('/api/appointments');
    expect(res.statusCode).toBe(403);
    expect(res.body.error).toBeDefined();
});

// PRUEBA 2: GET lista todas las citas con token válido
test('GET /api/appointments con token válido debe retornar 200 y un arreglo', async () => {
    const res = await request(app)
        .get('/api/appointments')
        .set('Authorization', VALID_TOKEN);
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body[0]).toHaveProperty('id', 'abc123');
});

// PRUEBA 3: POST crea una cita y retorna 201
test('POST /api/appointments con datos válidos debe retornar 201', async () => {
    const nuevaCita = {
        patient_id:       2,
        doctor_name:      'Dra. Meredith Grey',
        appointment_date: '2026-05-10',
        reason:           'Revisión postoperatoria',
        status:           'pending'
    };

    const res = await request(app)
        .post('/api/appointments')
        .set('Authorization', VALID_TOKEN)
        .send(nuevaCita);

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('id', 'nuevo-id-123');
    expect(res.body).toHaveProperty('message', 'Cita Guardada');
});

// PRUEBA 4: GET por ID retorna la cita correcta
test('GET /api/appointments/:id con token válido debe retornar la cita', async () => {
    const res = await request(app)
        .get('/api/appointments/abc123')
        .set('Authorization', VALID_TOKEN);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('id', 'abc123');
    expect(res.body).toHaveProperty('doctor_name', 'Dr. Gregory House');
});

// PRUEBA 5: DELETE elimina la cita y retorna 200
test('DELETE /api/appointments/:id con token válido debe retornar 200', async () => {
    const res = await request(app)
        .delete('/api/appointments/abc123')
        .set('Authorization', VALID_TOKEN);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message', 'Cita Eliminada exitosamente');
});