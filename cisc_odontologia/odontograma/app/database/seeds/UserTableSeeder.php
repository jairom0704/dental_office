<?php

// Composer: "fzaninotto/faker": "v1.3.0"
use Faker\Factory as Faker;

class UserTableSeeder extends Seeder {

	public function run()
	{
		User::create([
			'id' 		=> 1,
			'cedula' 	=> '1014777780',
			'name' 		=> 'Administrador',
			'password'	=> \Hash::make('1014777780'),
			'email' 	=> 'admin@mansion_mascota.com',
			'phone' 	=> '2621244',
			'type' 		=> 'admin'
		]);

		User::create([
			'id' 		=> 2,
			'cedula'	=> '0812757578',
			'name' 		=> 'Usuario de pruebas',
			'password'	=> \Hash::make('0812757578'),
			'email' 	=> 'test@mansion_mascota.com',
			'phone' 	=> '2621244',
			'type' 		=> 'admin'
		]);

		$faker = Faker::create();

		foreach(range(1, 10) as $index)
		{
			$user = User::create([
				'cedula'	=> $faker->randomNumber(10),
				'name'		=> $faker->name,
				'password'	=> \Hash::make('123456'),
				'email' 	=> $faker->email,
				'phone' 	=> $faker->phoneNumber,
				'type'		=> 'user'
			]);

			foreach(range(1, $faker->numberBetween(1,2)) as $date)
			{
				$pet = Pet::create([
					'user_id' 	=> $user->id,
					'name'		=> $faker->firstName(),
					'type'		=> $faker->randomElement(['perro','gato','pajaro','otro'])
				]);
			}

			foreach(range(1, $faker->numberBetween(1,3)) as $date)
			{
				Appointment::create([
					'user_id' 	=> $user->id,
					'pet_id' 	=> $pet->id,
					'date'		=> $faker->dateTimeBetween('now', '+3 months'),
					'note'		=> $faker->text(100+$faker->numberBetween(10,150))
				]);
			}

		}
	}

}