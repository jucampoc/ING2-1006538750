<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PatientSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('patients')->insert([
            [
                'name' => 'Juan',
                'last_name' => 'Perez',
                'identity_document' => '1006538001',
                'birthday' => '1995-05-15',
                'phone' => '3001234567',
                'blood_type' => 'O+',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'María',
                'last_name' => 'Rodriguez',
                'identity_document' => '1006538002',
                'birthday' => '1992-08-20',
                'phone' => '3109876543',
                'blood_type' => 'A-',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'name' => 'Julian',
                'last_name' => 'Campo',
                'identity_document' => '1006538750',
                'birthday' => '2003-03-16',
                'phone' => '3132788496',
                'blood_type' => 'O+',
                'created_at' => now(),
                'updated_at' => now(),
            ]
        ]);
    }
}
