@extends('layout')

@section('content')
	{{ Form::open([
		'action' => 'PacienteController@store',
		'method' => 'POST',
		'role' => 'form',
	])}}
	<div class="page-header">
		<h3>Registrar un nuevo Paciente</h3>
	</div>
	<div class="clearfix">
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('name','Nombre del Paciente')}}
			<div class="input-group">
				<span class="input-group-addon glyphicon glyphicon-user"></span>
				{{Form::text('name', null, ['class'=>'form-control'])}}
			</div>
			{{ $errors->first('name','<p class="bg-danger">:message</p>')}}
		</div>

		<div class="form-group">
			{{Form::label('cedula','Documento de identidad')}}
			<div class="input-group">
				<span class="input-group-addon glyphicon glyphicon-credit-card"></span>
				{{Form::text('cedula', null, ['class'=>'form-control'])}}
			</div>
			{{ $errors->first('cedula','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('surname','Apellido')}}
			<div class="input-group">
				<span class="input-group-addon glyphicon glyphicon-envelope"></span>
				{{Form::text('surname', null, ['class'=>'form-control'])}}
			</div>
			{{ $errors->first('surname','<p class="bg-danger">:message</p>')}}
		</div>

		<div class="form-group">
			{{Form::label('number','Historia clinica')}}
			<div class="input-group">
				<span class="input-group-addon glyphicon glyphicon-earphone"></span>
				{{Form::text('number', null, ['class'=>'form-control'])}}
			</div>
			{{ $errors->first('number','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>

	<div class="col-lg-12">
		{{Form::label('note','Nota')}}
		<div>
			{{Form::textarea('note', null, ['class'=>'form-control'])}}
		</div>
		{{ $errors->first('note','<p class="bg-danger">:message</p>')}}
	</div>

	</div><!-- Termina el clearfix -->
	<hr>
	<p>
		<a href="{{ URL::to('pacientes') }}"
		class="btn btn-default">
			<span class="glyphicon glyphicon-arrow-left"></span> regresar a la lista de pacientes
		</a>
		<input type="submit" value="Registrar Paciente" class="btn btn-primary pull-right">
	</p>
	{{ Form::close() }}
@stop
