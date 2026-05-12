from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Notification
from .middleware import InternalTokenMiddleware
from .serializers import NotificationSerializer

VALID_TOKEN = 'Token miclave123'


class NotificationTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=VALID_TOKEN)
        self.notification = Notification.objects.create(
            patient_id=1,
            message='Cita confirmada para el 15 de Abril.',
            type='SMS'
        )

    # PRUEBA 1 - Middleware rechaza request sin token
    def test_middleware_rejects_request_without_token(self):
        middleware = InternalTokenMiddleware(lambda r: HttpResponse(status=200))
        request = self.factory.get('/api/notifications/')
        response = middleware(request)
        self.assertEqual(response.status_code, 403)

    # PRUEBA 2 - Middleware permite request con token válido
    def test_middleware_allows_request_with_valid_token(self):
        middleware = InternalTokenMiddleware(lambda r: HttpResponse(status=200))
        request = self.factory.get('/api/notifications/')
        request.META['HTTP_AUTHORIZATION'] = VALID_TOKEN
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    # PRUEBA 3 - GET lista todas las notificaciones
    def test_list_notifications_returns_200(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # PRUEBA 4 - POST crea una notificación correctamente
    def test_create_notification_returns_201(self):
        data = {
            'patient_id': 2,
            'message': 'Recordatorio de examen.',
            'type': 'EMAIL'
        }
        response = self.client.post('/api/notifications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 2)

    # PRUEBA 5 - DELETE elimina una notificación correctamente
    def test_delete_notification_returns_204(self):
        response = self.client.delete(f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())