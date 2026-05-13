import random
from locust import HttpUser, task, between, events


# CREDENCIALES Y ESTADO COMPARTIDO
GATEWAY_URL  = "http://localhost:8000"
USER_EMAIL   = "julian@gmail.com"
USER_PASSWORD = "admin123"

created_ids = {
    "patient":None,
    "appointment":None,
    "medical_record":None,
    "pharmacy":None,
    "notification":None,
}


class HospitalUser(HttpUser):
    """
    Usuario virtual que simula el flujo completo de un operador del sistema
    hospitalario a través del API Gateway.
    """
    host = GATEWAY_URL
    wait_time = between(1, 3)
    token = None

    # Login 
    def on_start(self):
        response = self.client.post(
            "/api/login",
            json={"email": USER_EMAIL, "password": USER_PASSWORD},
        )
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            self.token = None

    def auth_headers(self):
        """Devuelve los headers con el Bearer token de Sanctum."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type":"application/json",
            "Accept":"application/json",
        }


    # GET /api/patients - laravel-patient-service - Lista todos los pacientes
    @task(3)
    def get_patients(self):
        self.client.get(
            "/api/patients",
            headers=self.auth_headers(),
        )


    # POST /api/patients - laravel-patient-service - Crea un nuevo paciente
    @task(2)
    def create_patient(self):
        doc = str(random.randint(1000000000, 9999999999))
        response = self.client.post(
            "/api/patients",
            json={
                "name":              "Locust",
                "last_name":         "TestUser",
                "identity_document": doc,
                "birthday":          "1995-06-20",
                "phone":             "3001112233",
                "blood_type":        "A+",
            },
            headers=self.auth_headers(),
        )
        if response.status_code == 201:
            created_ids["patient"] = response.json().get("id")


    # GET /api/patients/{id} - laravel-patient-service - Detalle de un paciente
    @task(2)
    def get_patient_by_id(self):
        patient_id = created_ids.get("patient") or 1
        self.client.get(
            f"/api/patients/{patient_id}",
            headers=self.auth_headers(),
        )


    # GET /api/appointments - express-appointments-service - Lista todas las citas
    @task(3)
    def get_appointments(self):
        self.client.get(
            "/api/appointments",
            headers=self.auth_headers(),
        )


    # POST /api/appointments - express-appointments-service - Crea una cita médica
    @task(2)
    def create_appointment(self):
        patient_id = created_ids.get("patient") or 1
        response = self.client.post(
            "/api/appointments",
            json={
                "patient_id":       patient_id,
                "doctor_name":      "Dr. Gregory House",
                "appointment_date": "2026-09-15",
                "reason":           "Prueba de carga Locust",
                "status":           "pending",
            },
            headers=self.auth_headers(),
        )
        if response.status_code == 201:
            created_ids["appointment"] = response.json().get("id")


    # GET /api/pharmacy - express-pharmacy-service - Lista medicamentos
    @task(3)
    def get_pharmacy(self):
        self.client.get(
            "/api/pharmacy",
            headers=self.auth_headers(),
        )


    # ─────────────────────────────────────────────────────────────────────────
    # POST /api/pharmacy - express-pharmacy-service - Agrega un medicamento
    @task(1)
    def create_medicine(self):
        response = self.client.post(
            "/api/pharmacy",
            json={
                "name":        f"Medicamento-{random.randint(100, 999)}",
                "description": "Generado por prueba de carga",
                "stock":       random.randint(10, 200),
                "price":       round(random.uniform(500, 5000), 2),
                "category":    "Prueba",
            },
            headers=self.auth_headers(),
        )
        if response.status_code == 201:
            created_ids["pharmacy"] = response.json().get("_id")


    # GET /api/medical-records - flask-medicalrecords-service - Lista historiales
    @task(3)
    def get_medical_records(self):
        self.client.get(
            "/api/medical-records",
            headers=self.auth_headers(),
        )


    # POST /api/medical-records - flask-medicalrecords-service - Crea historial clínico
    @task(2)
    def create_medical_record(self):
        patient_id = created_ids.get("patient") or 1
        response = self.client.post(
            "/api/medical-records",
            json={
                "patient_id": patient_id,
                "diagnosis":  "Diagnóstico de prueba Locust",
                "treatment":  "Tratamiento simulado 500mg",
                "doctor":     "Dr. Locust Tester",
            },
            headers=self.auth_headers(),
        )
        if response.status_code == 201:
            created_ids["medical_record"] = response.json().get("id")


    # GET /api/notifications - django-notifications-service - Lista notificaciones
    @task(2)
    def get_notifications(self):
        self.client.get(
            "/api/notifications",
            headers=self.auth_headers(),
        )


    # Logout al terminar
    def on_stop(self):
        """Se ejecuta una vez por usuario virtual al detener la prueba."""
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self.auth_headers(),
            )


