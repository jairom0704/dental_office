<?php

class medicalhistory extends \Eloquent {
	protected $fillable = [
		'cedula',
		'email',
		'name',
		'note',
		'surname',
	];

	protected $perPage = 10;

	public function odontograma_detail()
	{
		return $this->hasMany('odontograma_detail');
	}
}
