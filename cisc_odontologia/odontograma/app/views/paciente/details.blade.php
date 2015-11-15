@extends('layout')

@section('content')
	<div class="page-header">
		<h3>
			{{ $paciente->nombre }}<br>
		</h3>
	</div>
	{{ Form::open([
		'action' => 'PacienteController@update',
		'method' => 'POST',
		'role' => 'form',
	])}}
	<div class="panel panel-default clearfix">
		<div class="panel-heading">
			<div class="pull-right form-inline">
				<input type="submit" 
						value="Grabar Cambios" 
						class="btn btn-primary btn-xs">
			</div>
			Información del Paciente
		</div>
		<fieldset class="col-lg-6 list-group-item">
			<div class="form-group">
				<div class="input-group">
					<span class="input-group-addon glyphicon glyphicon-user"></span>
					{{Form::text('name', $paciente->name, ['class'=>'form-control'])}}
				</div>
				{{ $errors->first('name','<p class="bg-danger">:message</p>')}}
			</div>

			<div class="form-group">
				<div class="input-group">
					<span class="input-group-addon glyphicon glyphicon-credit-card"></span>
					{{Form::text('cedula', $paciente->cedula, ['class'=>'form-control'])}}
				</div>
				{{ $errors->first('cedula','<p class="bg-danger">:message</p>')}}
			</div>
		</fieldset>
		<fieldset class="col-lg-6 list-group-item">
			<div class="form-group">
				<div class="input-group">
					<span class="input-group-addon glyphicon glyphicon-envelope"></span>
					{{Form::text('surname', $paciente->surname, ['class'=>'form-control'])}}
				</div>
				{{ $errors->first('surname','<p class="bg-danger">:message</p>')}}
			</div>

			<div class="form-group">
				<div class="input-group">
					<span class="input-group-addon glyphicon glyphicon-earphone"></span>
					{{Form::text('number', $paciente->number, ['class'=>'form-control'])}}
				</div>
				{{ $errors->first('number','<p class="bg-danger">:message</p>')}}
			</div>
		</fieldset>
		<div class="col-lg-12 list-group-item">
			{{Form::textarea('note', $paciente->note, ['class'=>'form-control'])}}
			{{ $errors->first('note','<p class="bg-danger">:message</p>')}}
		</div>
	</div>
	{{Form::hidden('id', $paciente->id)}}
	{{ Form::close() }}



	<p>
		<a href="{{ URL::to('pacientes') }}"
		class="btn btn-default">
			<span class="glyphicon glyphicon glyphicon glyphicon-arrow-left"></span> regresar a la lista de pacientes
		</a>
		<a href="{{ URL::to('paciente/delete/'.$paciente->id) }}"
		class="btn text-danger pull-right">
		Eliminar este paciente (cuidado, esta accion es permanente)
		</a>
	</p>

@stop
