<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PatientProxyController extends Controller
{
    private $url = 'http://localhost:8001/api/patients';

    public function index()
    {
        $response = Http::get($this->url);
        return response()->json($response->json(), $response->status());
    }

    public function store(Request $request)
    {
        $response = Http::post($this->url, $request->all());
        return response()->json($response->json(), $response->status());
    }


}
