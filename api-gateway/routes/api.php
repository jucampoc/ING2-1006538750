<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PatientProxyController;
use App\Http\Controllers\AppointmentProxyController;
use App\Http\Controllers\MedicalRecordProxyController;

// Rutas públicas
Route::post('/login', [AuthController::class, 'login']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

// Ruta "ficticia" requerida por Laravel para generar el correo de recuperación
Route::get('/reset-password/{token}', function (string $token) {
    return response()->json(['token' => $token]);
})->name('password.reset');

// Rutas protegidas por Sanctum
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);

    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    Route::get('/patients', [PatientProxyController::class, 'index']);
    Route::post('/patients', [PatientProxyController::class, 'store']);
    Route::get('/patients/{id}', [PatientProxyController::class, 'show']);
    Route::put('/patients/{id}', [PatientProxyController::class, 'update']);
    Route::delete('/patients/{id}', [PatientProxyController::class, 'destroy']);

    Route::get('/appointments', [AppointmentProxyController::class, 'index']);
    Route::post('/appointments', [AppointmentProxyController::class, 'store']);
    Route::put('/appointments/{id}', [AppointmentProxyController::class, 'update']);
    Route::delete('/appointments/{id}', [AppointmentProxyController::class, 'destroy']);


    Route::get('/medical-records', [MedicalRecordProxyController::class, 'index']);
    Route::post('/medical-records', [MedicalRecordProxyController::class, 'store']);
    Route::get('/medical-records/{id}', [MedicalRecordProxyController::class, 'show']);
    Route::put('/medical-records/{id}', [MedicalRecordProxyController::class, 'update']);
    Route::delete('/medical-records/{id}', [MedicalRecordProxyController::class, 'destroy']);


});
