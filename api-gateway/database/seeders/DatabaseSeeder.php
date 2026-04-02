<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        \App\Models\User::create([
            'name' => 'julian',
            'email' => 'julian@gmail.com',
            'password' => bcrypt('admin123'),
        ]);

        \App\Models\User::create([
            'name' => 'Recepcionista',
            'email' => 'recepcion@test.com',
            'password' => bcrypt('password123'),
        ]);
    }
}
