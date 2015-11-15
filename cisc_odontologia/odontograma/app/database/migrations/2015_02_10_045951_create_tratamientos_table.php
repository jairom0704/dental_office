<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateTratamientosTable extends Migration {

	/**
	 * Run the migrations.
	 *
	 * @return void
	 */
	public function up()
	{
		Schema::create('tratamientos', function(Blueprint $table)
		{
			$table->increments('id')->unsigned();
			$table->string('nombre', 100);
			$table->string('codigo', 100);
			$table->string('descripcion')->nullable();
			$table->boolean('aplicaCara')->default(false);
			$table->boolean('aplicaDiente')->default(false);
			$table->enum('activo',['0','1'])->default('1');
			$table->timestamps();
		});
	}

	/**
	 * Reverse the migrations.
	 *
	 * @return void
	 */
	public function down()
	{
		Schema::drop('tratamientos');
	}

}
