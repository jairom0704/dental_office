<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateDiagnosticosTable extends Migration {

	/**
	 * Run the migrations.
	 *
	 * @return void
	 */
	public function up()
	{
		Schema::create('diagnosticos', function(Blueprint $table)
		{
			$table->increments('id')->unsigned();
			$table->biginteger('paciente_id')->unsigned();
			$table->longText('diagnostico');
			$table->longText('diagnostico_texto')->nullable();
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
		Schema::drop('diagnosticos');
	}

}
