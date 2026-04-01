<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PatientProxyController;

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
});
