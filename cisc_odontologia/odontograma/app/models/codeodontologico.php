<?php

class codeodontologico extends \Eloquent {
	protected $fillable = [
		'activo',
		'aplicacara',
		'aplicadiente',
		'codigo',
		'descripcion',
		'name',
	];

	protected $perPage = 10;
}
