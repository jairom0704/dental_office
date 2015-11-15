<?php

// Composer: "fzaninotto/faker": "v1.3.0"
use Faker\Factory as Faker;

class ProductTableSeeder extends Seeder {

	public function run()
	{
		$faker = Faker::create();

		foreach(range(1, 100) as $index)
		{
			Product::create([
				'name'		 	=> $faker->userName,
				'description'	=> $faker->text(100+$faker->numberBetween(10,150)),
				'price' 		=> $faker->randomFloat(2,5,30),
				'icon' 			=> 'http://www.bumultimedia.com/trabajos/marcaDiferenciada/mansionMascotas/images/gallery_'.$faker->numberBetween(1,5).'.jpg',
				'category'		=> $faker->numberBetween(1,5)
			]);
		}
	}

}