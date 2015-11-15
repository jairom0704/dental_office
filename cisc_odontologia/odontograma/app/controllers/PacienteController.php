<?php

class PacienteController extends \BaseController {

	public function index()
	{
		$pacientes = medicalhistory::paginate();
		return View::make('paciente/index')
						->with('pacientes', $pacientes)
						->with('section', 'pacientes');
	}

	
	public function create()
	{
		return View::make('paciente/create')
						->with('section', 'pacientes');
	}

	
	public function validate( $data, $uniqueness = true )
	{
		$mail_unique = ($uniqueness) ? '|unique:pacientes,email'  : '';
		$ced_unique  = ($uniqueness) ? '|unique:pacientes,cedula' : '';
		$rules = [
			'name' 	=> 'required',
			'cedula' 	=> 'required|digits:10'.$ced_unique,
		];

		return \Validator::make( $data, $rules );
	}

	public function store()
	{
		$data = Input::all();
		$validation = $this->validate($data);

		if( $validation->fails() )
			return Redirect::back()->withInput()->withErrors($validation->messages());

		medicalhistory::create($data);
		return Redirect::route('pacientes');
	}



	public function show($id)
	{
		$paciente = medicalhistory::find($id);
		return View::make('paciente/details')
						->with('section', 'pacientes')
						->with('paciente', $paciente);
	}


	public function update()
	{
		$data = Input::except('_token');
		$validation = $this->validate($data, false);

		if( $validation->fails() )
			return Redirect::back()->withInput()->withErrors($validation->messages());

		$paciente = medicalhistory::find($data['id']);
		$paciente->update($data);
		return Redirect::route('paciente_profile', $paciente->id);
	}


	public function destroy($id)
	{
		$paciente = medicalhistory::find($id);
		$paciente->diagnosticos()->delete();
		$paciente->delete();
		return Redirect::route('pacientes');
	}




	//=====================================================================================
	// 	API REST
	//=====================================================================================


	/**
	 * function: json_search_cedula
	 * parameters: cedula
	 * method: GET
	 * description: devuelve la informacion de un usuario si su cedula coinciden
	 * con el registro en la base de datos.
	 ********************************************************************/
	public function json_search_cedula($cedula)
	{
		$paciente = medicalhistory::where('cedula',$cedula)->get();
		return Response::json($paciente);
	}


	/**
	 * function: json_search_nombre
	 * parameters: nombre
	 * method: GET
	 * description: devuelve la informacion de un usuario si su nombre coinciden
	 * con el registro en la base de datos.
	 ********************************************************************/
	public function json_search_nombre($nombre)
	{
		$paciente = medicalhistory::where('name', 'LIKE', '%'.$nombre.'%')->get();
		return Response::json($paciente);
	}
}
