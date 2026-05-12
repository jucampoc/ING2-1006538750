from django.test import TestCase, Client
import json

class NotificationTests(TestCase):
    def setUp(self):
        # setUp se ejecuta automáticamente antes de CADA prueba
        self.client = Client()
        # Django convierte las cabeceras HTTP; 'Authorization' se pasa como 'HTTP_AUTHORIZATION'
        self.headers = {'HTTP_AUTHORIZATION': 'Token miclave123'}

    def test_rechazar_sin_token(self):
        # 1. Prueba de Seguridad: Petición sin cabeceras
        response = self.client.get('/api/notifications/')
        self.assertIn(response.status_code, [401, 403])

    def test_obtener_notificaciones(self):
        # 2. Prueba de Lectura: Camino Feliz
        response = self.client.get('/api/notifications/', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_crear_notificacion(self):
        # 3. Prueba de Creación: Camino Feliz
        payload = {"patient_id": 1, "message": "Cita confirmada", "type": "SMS"}
        response = self.client.post('/api/notifications/', 
                                    data=json.dumps(payload), 
                                    content_type='application/json',
                                    **self.headers)
        self.assertEqual(response.status_code, 201)

    def test_crear_notificacion_faltan_datos(self):
        # 4. Prueba de Validación: Faltan campos obligatorios
        payload = {"message": "Cita confirmada"} # Omitimos intencionalmente el patient_id
        response = self.client.post('/api/notifications/', 
                                    data=json.dumps(payload), 
                                    content_type='application/json',
                                    **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_metodo_no_permitido(self):
        # 5. Prueba de Robustez: Verbo HTTP incorrecto
        response = self.client.put('/api/notifications/', 
                                   data=json.dumps({}), 
                                   content_type='application/json',
                                   **self.headers)
        self.assertEqual(response.status_code, 405) # 405 Method Not Allowed