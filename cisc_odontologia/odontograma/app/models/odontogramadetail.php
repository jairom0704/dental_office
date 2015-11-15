<?php

class odontogramadetail extends \Eloquent {
	protected $fillable = [
		'secuencial',
		'state',
		'diagnostico',
		'diagnostico_realizado',
		'diagnostico_final',
		'diagnostico_final_realizado',
		'paciente_id',
		'observacion',
	];

	protected $perPage = 10;


	public function medicalhistory()
	{
		return $this->belongsTo('medicalhistory')->select(array('id', 'name', 'cedula'));
	}
}
