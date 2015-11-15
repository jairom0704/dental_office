<?php

// Composer: "fzaninotto/faker": "v1.3.0"
use Faker\Factory as Faker;

class NewsTableSeeder extends Seeder {

	public function run()
	{
		$faker = Faker::create();

		foreach(range(1, 100) as $index)
		{
			News::create([
				'title'		=> $faker->text(20+$faker->numberBetween(10,100)),
				'content'	=> $faker->text(400+$faker->numberBetween(10,250)),
				'image'		=> 'http://www.bumultimedia.com/trabajos/marcaDiferenciada/mansionMascotas/images/news_'.$faker->numberBetween(1,5).'.png',
				'publish'	=> $faker->randomElement([1,2])
			]);
		}
	}

}