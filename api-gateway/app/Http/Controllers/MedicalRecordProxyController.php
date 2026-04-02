<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MedicalRecordProxyController extends Controller
{
    private $url;
    private $secretToken;

    public function __construct()
    {
        $this->url = env('MEDICAL_RECORDS_SERVICE_URL');
        $this->secretToken = env('MEDICAL_RECORDS_SECRET_TOKEN');
    }

    public function index()
    {
        $response = Http::withHeaders([
            'Authorization' => $this->secretToken
        ])->get($this->url);

        return response()->json($response->json(), $response->status());
    }

    public function store(Request $request)
    {
        $response = Http::withHeaders([
            'Authorization' => $this->secretToken
        ])->post($this->url, $request->all());

        return response()->json($response->json(), $response->status());
    }
}
