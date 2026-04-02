<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class AppointmentProxyController extends Controller
{
    private $url = 'http://localhost:3000/api/appointments';
    private $secretToken = 'Token miclave123';

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

    public function show($id)
    {
        $response = Http::withHeaders([
            'Authorization' => $this->secretToken
        ])->get($this->url . '/' . $id);

        return response()->json($response->json(), $response->status());
    }

    public function update(Request $request, $id)
    {
        $response = Http::withHeaders([
            'Authorization' => $this->secretToken
        ])->put($this->url . '/' . $id, $request->all());

        return response()->json($response->json(), $response->status());
    }

    public function destroy($id)
    {
        $response = Http::withHeaders([
            'Authorization' => $this->secretToken
        ])->delete($this->url . '/' . $id);

        return response()->json($response->json(), $response->status());
    }
}
