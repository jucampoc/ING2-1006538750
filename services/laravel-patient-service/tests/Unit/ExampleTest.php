<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\Patient;
use Illuminate\Foundation\Testing\RefreshDatabase;

class PatientTest extends TestCase
{
    use RefreshDatabase;

    private string $token = 'Token miclave123';

    private array $validData = [
        'name'=> 'Juan',
        'last_name'=> 'Pérez',
        'identity_document'=> '1234567890',
        'birthday'=> '1990-05-15',
        'phone'=> '3001234567',
        'blood_type'=> 'O+',
    ];

    // PRUEBA 1 - Middleware rechaza request sin token
    public function test_middleware_rechaza_request_sin_token(): void
    {
        $response = $this->getJson('/api/patients');

        $response->assertStatus(403);
        $response->assertJson(['error' => 'Acceso no autorizado. Token inválido.']);
    }

    // PRUEBA 2 - GET retorna lista de pacientes
    public function test_index_retorna_lista_de_pacientes(): void
    {
        Patient::create($this->validData);

        $response = $this->withHeaders(['Authorization' => $this->token])->getJson('/api/patients');

        $response->assertStatus(200);
        $response->assertJsonIsArray();
        $response->assertJsonCount(1);
    }

    // PRUEBA 3 - POST crea un paciente con datos válidos
    public function test_store_crea_paciente_con_datos_validos(): void
    {
        $response = $this->withHeaders(['Authorization' => $this->token])->postJson('/api/patients', $this->validData);

        $response->assertStatus(201);
        $response->assertJsonFragment(['name' => 'Juan']);
        $this->assertDatabaseHas('patients', ['identity_document' => '1234567890']);
    }

    // PRUEBA 4 - POST rechaza datos incompletos (validación)
    public function test_store_rechaza_datos_incompletos(): void
    {
        $response = $this->withHeaders(['Authorization' => $this->token])
                         ->postJson('/api/patients', [
                             'name' => 'Solo nombre',
                         ]);

        $response->assertStatus(422);
        $response->assertJsonValidationErrors(['last_name', 'identity_document', 'birthday']);
    }

    // PRUEBA 5 - DELETE elimina un paciente existente
    public function test_destroy_elimina_paciente_existente(): void
    {
        $patient = Patient::create($this->validData);

        $response = $this->withHeaders(['Authorization' => $this->token])->deleteJson("/api/patients/{$patient->id}");

        $response->assertStatus(200);
        $response->assertJson(['message' => 'Patient deleted successfully']);
        $this->assertDatabaseMissing('patients', ['id' => $patient->id]);
    }
}
