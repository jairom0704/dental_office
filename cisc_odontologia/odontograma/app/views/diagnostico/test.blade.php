@extends('layout')

@section('content')
	<div class="page-header">
		<h3>Diagnosticos</h3>
	</div>


	{{ Form::open([
		'action' => 'PacienteController@store',
		'method' => 'POST',
		'role'   => 'form',
		'id'     => 'diagnostico_data',
	])}}
	<div class="clearfix">
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('paciente_id','Paciente')}}
			{{Form::text('paciente_id', null, ['class'=>'form-control','id'=>'ced'])}}
			{{ $errors->first('paciente_id','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('id','ID')}}
			{{Form::text('id', null, ['class'=>'form-control'])}}
			{{ $errors->first('id','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>

	<div class="col-lg-12">
		{{Form::label('diagnostico','Diagnostico')}}
		{{Form::textarea('diagnostico', null, ['class'=>'form-control'])}}
		{{ $errors->first('diagnostico','<p class="bg-danger">:message</p>')}}
	</div>

	<div class="col-lg-12">
		{{Form::label('diagnostico_final','Texto Plano')}}
		{{Form::textarea('diagnostico_final', null, ['class'=>'form-control'])}}
		{{ $errors->first('diagnostico_final','<p class="bg-danger">:message</p>')}}
	</div>

	</div><!-- Termina el clearfix -->
	<hr>
	<p>
		<a href="#" id="update"	class="btn btn-default">
			Actualizar
		</a>
		<a href="#" id="load" class="btn btn-default">
			cargar
		</a>
		<a href="#" id="save" class="btn btn-default">
			Grabar
		</a>
	</p>
	{{ Form::close() }}

<script>
	$('#save').click(function(){
		$.ajax({
			type : "POST",
			url  : "../diagnostico/save",
			data : $('#diagnostico_data').serialize(),
			success: reset
		});
		
		return false;
	});

	$('#update').click(function(){
		$.ajax({
			type : "POST",
			url  : "../diagnostico/update",
			data : $('#diagnostico_data').serialize(),
			success: reset
		});
		return false;
	});

	$('#load').click(function(){
		$.ajax({
			type : "GET",
			url  : "../public/diagnostico/view/"+$('#ced').val(),
			success: function(data){
				populate('#diagnostico_data', data[0]);
			}
		});
		return false;
	});

	function populate(frm, data) {
		$.each(data, function(key, value){
			console.log(key)
			$('[name='+key+']', frm).val(value);
		});
	}
	function reset(data){
		console.log(data);
		$('#diagnostico_data')[0].reset();
	}
</script>

	
@stop
