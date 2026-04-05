const request = require('supertest');
const app = require('../index');
const Medicine = require('../models/Medicine');

jest.mock('../models/Medicine');

describe('Pruebas Unitarias - Pharmacy Service', () => {
    const TOKEN_VALIDO = 'Token miclave123';

    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('Seguridad (Middleware)', () => {
        it('Debería denegar acceso con código 403 si no hay token', async () => {
            const res = await request(app).get('/api/pharmacy');
            expect(res.statusCode).toEqual(403);
            expect(res.body.error).toBe("Acceso denegado. Solo Gateway permitido.");
        });
    });

    describe('GET /api/pharmacy', () => {
        it('Debería retornar la lista de medicamentos', async () => {
            const mockMedicines = [
                { _id: '1', name: 'Paracetamol', price: 500, stock: 100 },
                { _id: '2', name: 'Ibuprofeno', price: 800, stock: 50 }
            ];
            
            Medicine.find.mockResolvedValue(mockMedicines);

            const res = await request(app)
                .get('/api/pharmacy')
                .set('Authorization', TOKEN_VALIDO);

            expect(res.statusCode).toEqual(200);
            expect(res.body).toHaveLength(2);
            expect(res.body[0].name).toBe('Paracetamol');
        });
    });

    describe('POST /api/pharmacy', () => {
        it('Debería crear un medicamento y retornar 201', async () => {
            const nuevoMedicamento = { name: 'Amoxicilina', price: 1200, stock: 30 };
            
            Medicine.prototype.save = jest.fn().mockResolvedValue(nuevoMedicamento);

            const res = await request(app)
                .post('/api/pharmacy')
                .set('Authorization', TOKEN_VALIDO)
                .send(nuevoMedicamento);

            expect(res.statusCode).toEqual(201);
            expect(Medicine.prototype.save).toHaveBeenCalledTimes(1);
        });
    });
});