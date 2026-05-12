const request = require('supertest');
const app     = require('../index');
const Medicine = require('../models/Medicine');

jest.mock('../models/Medicine');

const TOKEN_VALIDO = 'Token miclave123';

beforeEach(() => {
    jest.clearAllMocks();
});

// PRUEBA 1: Middleware rechaza petición sin token
test('GET /api/pharmacy sin token debe retornar 403', async () => {
    const res = await request(app).get('/api/pharmacy');

    expect(res.statusCode).toBe(403);
    expect(res.body.error).toBe('Acceso denegado. Solo Gateway permitido.');
});

// PRUEBA 2: GET retorna lista de medicamentos
test('GET /api/pharmacy con token válido debe retornar 200 y la lista', async () => {
    const mockMedicamentos = [
        { _id: '1', name: 'Paracetamol', price: 500,  stock: 100, category: 'Analgésico' },
        { _id: '2', name: 'Ibuprofeno',  price: 800,  stock: 50,  category: 'Antiinflamatorio' }
    ];

    Medicine.find.mockResolvedValue(mockMedicamentos);

    const res = await request(app)
        .get('/api/pharmacy')
        .set('Authorization', TOKEN_VALIDO);

    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body).toHaveLength(2);
    expect(res.body[0].name).toBe('Paracetamol');
});

// PRUEBA 3: POST crea un medicamento y retorna 201
test('POST /api/pharmacy con datos válidos debe retornar 201', async () => {
    const nuevoMedicamento = {
        name:        'Amoxicilina',
        description: 'Antibiótico de amplio espectro',
        price:       1200,
        stock:       30,
        category:    'Antibiótico'
    };

    Medicine.prototype.save = jest.fn().mockResolvedValue(nuevoMedicamento);

    const res = await request(app)
        .post('/api/pharmacy')
        .set('Authorization', TOKEN_VALIDO)
        .send(nuevoMedicamento);

    expect(res.statusCode).toBe(201);
    expect(Medicine.prototype.save).toHaveBeenCalledTimes(1);
});

//PRUEBA 4: PUT actualiza un medicamento y retorna 200
test('PUT /api/pharmacy/:id con datos válidos debe retornar 200', async () => {
    const medicamentoActualizado = {
        _id:   'abc123',
        name:  'Paracetamol',
        price: 600,
        stock: 80
    };

    Medicine.findByIdAndUpdate.mockResolvedValue(medicamentoActualizado);

    const res = await request(app)
        .put('/api/pharmacy/abc123')
        .set('Authorization', TOKEN_VALIDO)
        .send({ price: 600, stock: 80 });

    expect(res.statusCode).toBe(200);
    expect(res.body.price).toBe(600);
    expect(res.body.stock).toBe(80);
});

// PRUEBA 5: DELETE elimina un medicamento y retorna 200
test('DELETE /api/pharmacy/:id con token válido debe retornar 200', async () => {
    Medicine.findByIdAndDelete.mockResolvedValue({ _id: 'abc123' });

    const res = await request(app)
        .delete('/api/pharmacy/abc123')
        .set('Authorization', TOKEN_VALIDO);

    expect(res.statusCode).toBe(200);
    expect(res.body.message).toBe('Medicamento eliminado correctamente');
});