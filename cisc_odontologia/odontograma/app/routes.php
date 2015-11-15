<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the Closure to execute when that URI is requested.
|
*/


/*	GENERALES
------------------------------------------------------------------------*/
Route::get('/', 	array('as' => 'home', function(){ return View::make('index'); }));
Route::get('/api', 	array('as' => 'api',  function(){ return View::make('api'); }));



/*	DIAGNOSTICOS
------------------------------------------------------------------------*/
Route::get('diagnostico', array(
	'as' 	=> 'diagnostico',
	'uses'	=> 'DiagnosticoController@index') );
Route::get('diagnostico/delete/{id}'		, 'DiagnosticoController@destroy' 	);
Route::get('diagnostico/view/{paciente_id}'	, 'DiagnosticoController@details' 	);
Route::post('diagnostico/save'			, 'DiagnosticoController@store' 	);
Route::post('diagnostico/update'		, 'DiagnosticoController@update'	);




/*	TRATAMIENTOS
------------------------------------------------------------------------*/
Route::get('tratamientos', array(
	'as' => 'tratamientos',
	'uses'=>'TratamientoController@index'
));

Route::get('tratamiento/view/{id}', array(
	'as' =>	'tratamiento_profile',
	'uses'=>'TratamientoController@show'
));

Route::get('tratamiento/new' 		, 'TratamientoController@create'  	);
Route::get('tratamiento/delete/{id}' 	, 'TratamientoController@destroy' 	);
Route::post('tratamiento/save'		, 'TratamientoController@store'	  	);
Route::post('tratamiento/update'	, 'TratamientoController@update'  	);
Route::get('tratamientos/list'		, 'TratamientoController@json_list'	);




/*	PACIENTES
------------------------------------------------------------------------*/
Route::get('pacientes', array(
	'as' => 'pacientes',
	'uses'=>'PacienteController@index'
));

Route::get('paciente/view/{id}', array(
	'as' =>	'paciente_profile',
	'uses'=>'PacienteController@show'
));

Route::get('paciente/new' 			, 'PacienteController@create'	);
Route::get('paciente/delete/{id}'		, 'PacienteController@destroy'	);
Route::post('paciente/save'			, 'PacienteController@store'	);
Route::post('paciente/update'			, 'PacienteController@update'	);
Route::get('paciente/con_cedula/{cedula}'	, 'PacienteController@json_search_cedula');
Route::get('paciente/con_nombre/{nombre}'	, 'PacienteController@json_search_nombre');


