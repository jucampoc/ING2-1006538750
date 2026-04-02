from django.db import models

class Notification(models.Model):
    patient_id = models.IntegerField()
    message = models.TextField()
    type = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para paciente {self.patient_id} ({self.type})"
