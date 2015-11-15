<?php

class DiagnosticoController extends \BaseController {


	public function index()
	{
		return View::make('diagnostico/test')
						->with('section', 'diagnosticos');
	}

	
	public function validate( $data, $uniqueness = true )
	{
		$rules = [
			'diagnostico'  => 'required',
			'paciente_id' => 'required',
		];

		return \Validator::make( $data, $rules );
	}

	public function store()
	{
		$data = Input::all();
		$validation = $this->validate($data);

		if( $validation->fails() )
			return Response::json(['error'=>'los datos no son correctos o no estan completos']);

		$diagnostico = odontogramadetail::create($data);
		$data_update=[];
		$data_update['state']='draft';
		$data_update['secuencial']='D'.substr("0000000000" . $diagnostico['id'],strlen($diagnostico['id']) );
		$diagnostico->update($data_update);
		return Response::json($diagnostico);
	}



	public function details($paciente_id)
	{
		$diagnostico = odontogramadetail::select(['id','diagnostico','diagnostico_final','diagnostico_realizado','observacion','created_at', 'secuencial'])->
									where('paciente_id',$paciente_id)->
									take(10)->
									orderBy('created_at','Desc')->
									get();
		return Response::json($diagnostico);
	}


	public function update()
	{
		$data = Input::except('_token');
		$validation = $this->validate($data, false);

		if( $validation->fails() )
			return Response::json(['error'=>'los datos no son correctos o no estan completos']);

		$diagnostico = odontogramadetail::find($data['id']);
		$diagnostico->update($data);
		return Response::json($diagnostico);
	}


	public function destroy($id)
	{
		$diagnostico = odontogramadetail::find($id);
		$diagnostico->delete();
		return Response::json(['result'=>'el diagnostico fue eliminado']);
	}
}
