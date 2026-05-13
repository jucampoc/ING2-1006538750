<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PharmacyProxyController extends Controller
{
    private $url;
    private $token;

    public function __construct()
    {
        $this->url = env('PHARMACY_SERVICE_URL');
        $this->token = 'Token ' . env('TOKEN_SECRETO');
    }

    public function index() {
        return Http::withHeaders(['Authorization' => $this->token])->get($this->url);
    }

    public function store(Request $request) {
        return Http::withHeaders(['Authorization' => $this->token])->post($this->url, $request->all());
    }

    public function update(Request $request, $id) {
        return Http::withHeaders(['Authorization' => $this->token])->put("$this->url/$id", $request->all());
    }

    public function destroy($id) {
        return Http::withHeaders(['Authorization' => $this->token])->delete("$this->url/$id");
    }
}
