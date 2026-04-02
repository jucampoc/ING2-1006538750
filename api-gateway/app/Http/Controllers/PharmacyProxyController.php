<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class PharmacyProxyController extends Controller
{
    private $url = 'http://127.0.0.1:3001/api/pharmacy';
    private $token = 'Token miclave123';

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
