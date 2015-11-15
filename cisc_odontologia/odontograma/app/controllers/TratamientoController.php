<?php

class TratamientoController extends \BaseController {

	
	public function index()
	{
		$tratamientos = codeodontologico::paginate();
		return View::make('tratamiento/index')
						->with('tratamientos', $tratamientos)
						->with('section', 'tratamientos');
	}

	
	public function create()
	{
		return View::make('tratamiento/create')
						->with('section', 'tratamientos');
	}

	
	public function validate( $data, $uniqueness = true )
	{
		$rules = [
			'name' 		=> 'required',
			'codigo' 	=> 'required',
		];

		return \Validator::make( $data, $rules );
	}

	public function store()
	{
		$data = Input::all();
		$validation = $this->validate($data);

		if( $validation->fails() )
			return Redirect::back()->withInput()->withErrors($validation->messages());

		$data['aplicacara'  ] = ( Input::has('aplicaCara'  ) ) ? true : false;
		$data['aplicadiente'] = ( Input::has('aplicaDiente') ) ? true : false;

		codeodontologico::create($data);
		return Redirect::route('tratamientos');
	}



	public function show($id)
	{
		$tratamiento = codeodontologico::find($id);
		return View::make('tratamiento/details')
						->with('section', 'tratamientos')
						->with('tratamiento', $tratamiento);
	}


	public function update()
	{
		$data = Input::except('_token');
		$validation = $this->validate($data, false);

		if( $validation->fails() )
			return Redirect::back()->withInput()->withErrors($validation->messages());

		
		$data['aplicacara'  ] = ( Input::has('aplicaCara'  ) ) ? true : false;
		$data['aplicadiente'] = ( Input::has('aplicaDiente') ) ? true : false;

		$tratamiento = codeodontologico::find($data['id']);
		$tratamiento->update($data);
		return Redirect::route('tratamiento_profile', $tratamiento->id);
	}


	public function destroy($id)
	{
		$tratamiento = codeodontologico::find($id);
		$tratamiento->delete();
		return Redirect::route('tratamientos');
	}




	//=====================================================================================
	// 	API REST
	//=====================================================================================


	
	/* function: json_list
	 * parameters: none
	 * method: GET
	 * description: devuelve el listado de todos los tratamientos activos.
	------------------------------------------------------------*/
	public function json_list()
	{
		$tratamiento = codeodontologico::select(['codigo','name','aplicacara','aplicadiente'])
									->where('activo',True)
									->get();
		return Response::json($tratamiento);
	}
}
