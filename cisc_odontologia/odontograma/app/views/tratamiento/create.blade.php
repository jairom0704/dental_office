@extends('layout')

@section('content')
	{{ Form::open([
		'action' => 'TratamientoController@store',
		'method' => 'POST',
		'role' => 'form',
	])}}
	<div class="page-header">
		<h3>Registrar un nuevo Tratamiento</h3>
	</div>

	<div class="clearfix">
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('nombre','Nombre del Tratamiento')}}
			{{Form::text('nombre', null, ['class'=>'form-control'])}}
			{{ $errors->first('nombre','<p class="bg-danger">:message</p>')}}
		</div>

		<div class="form-group">			
			{{Form::label('aplicaCara','¿Aplica a la cara?')}}
			{{ Form::checkbox('aplicaCara', 0, false) }}
			{{ $errors->first('aplicaCara','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>
	<fieldset class="col-lg-6">
		<div class="form-group">
			{{Form::label('codigo','Código del Tratamiento')}}
			{{Form::text('codigo', null, ['class'=>'form-control'])}}
			{{ $errors->first('codigo','<p class="bg-danger">:message</p>')}}
		</div>

		<div class="form-group">
			{{Form::label('aplicaDiente','¿Aplica al diente?')}}
			{{Form::checkbox('aplicaDiente', 0, false) }}
			{{$errors->first('aplicaDiente','<p class="bg-danger">:message</p>')}}
		</div>
	</fieldset>

	<div class="col-lg-12">
		{{Form::label('descripcion','Descripción')}}
		{{Form::textarea('descripcion', null, ['class'=>'form-control'])}}
		{{ $errors->first('descripcion','<p class="bg-danger">:message</p>')}}
	</div>
	<div class="col-lg-6">
		{{Form::label('activo','¿Está Activo?')}}
		{{ Form::select('activo', [
			'1' => 'Habilitado',
			'0' => 'Deshabilitado'],
			null,
			['class'=>'form-control']
		) }}
		{{ $errors->first('activo','<p class="bg-danger">:message</p>')}}
	</div>

	</div><!-- Termina el clearfix -->
	<hr>
	<p>
		<a href="{{ URL::to('tratamientos') }}"
		class="btn btn-default">
			<span class="glyphicon glyphicon-arrow-left"></span> regresar a la lista de tratamientos
		</a>
		<input type="submit" value="Registrar Tratamiento" class="btn btn-primary pull-right">
	</p>
	{{ Form::close() }}
@stop