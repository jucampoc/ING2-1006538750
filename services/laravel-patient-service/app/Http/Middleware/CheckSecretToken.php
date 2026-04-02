<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckSecretToken
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): (Response)  $next
     */
    public function handle(Request $request, Closure $next)
    {

        $token = $request->header('Authorization');

        if ($token !== 'Token miclave123') {
            return response()->json(['error' => 'Acceso no autorizado. Token inválido.'], 403);
        }

        return $next($request);
    }
}
