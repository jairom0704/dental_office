@extends('layout')

@section('content')
	<div class="page-header">
		<h3>
			{{ $tratamiento->name }}<br>
		</h3>
	</div>
	{{ Form::open([
		'action' => 'TratamientoController@update',
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
			Información del Tratamiento
		</div>

		<fieldset class="col-lg-6 list-group-item">
			<div class="form-group">
				{{Form::label('name','Nombre del Tratamiento')}}
				{{Form::text('name', $tratamiento->name, ['class'=>'form-control'])}}
				{{ $errors->first('name','<p class="bg-danger">:message</p>')}}
			</div>

			<div class="form-group">			
				{{Form::label('aplicacara','¿Aplica a la cara?')}}
				{{Form::checkbox('aplicacara', 0, $tratamiento->aplicacara)}}
				{{$errors->first('aplicacara','<p class="bg-danger">:message</p>')}}
			</div>
		</fieldset>
		<fieldset class="col-lg-6 list-group-item">
			<div class="form-group">
				{{Form::label('codigo','Código del Tratamiento')}}
				{{Form::text('codigo', $tratamiento->codigo, ['class'=>'form-control'])}}
				{{ $errors->first('codigo','<p class="bg-danger">:message</p>')}}
			</div>

			<div class="form-group">
				{{Form::label('aplicadiente','¿Aplica al diente?')}}
				{{Form::checkbox('aplicadiente', 0, $tratamiento->aplicadiente)}}
				{{ $errors->first('aplicadiente','<p class="bg-danger">:message</p>')}}
			</div>
		</fieldset>

		<div class="col-lg-12 list-group-item">
			{{Form::label('descripcion','Descripción')}}
			{{Form::textarea('descripcion', $tratamiento->descripcion, ['class'=>'form-control'])}}
			{{ $errors->first('descripcion','<p class="bg-danger">:message</p>')}}
		</div>
		<div class="col-lg-6 list-group-item">
			{{Form::label('activo','¿Está Activo?')}}
			{{ Form::select('activo', [
				'1' => 'Habilitado',
				'0' => 'Deshabilitado'],
				$tratamiento->activo,
				['class'=>'form-control']
			) }}
			{{ $errors->first('activo','<p class="bg-danger">:message</p>')}}
		</div>


	</div>
	{{Form::hidden('id', $tratamiento->id)}}
	{{ Form::close() }}



	<p>
		<a href="{{ URL::to('tratamientos') }}"
		class="btn btn-default">
			<span class="glyphicon glyphicon glyphicon glyphicon-arrow-left"></span> regresar a la lista de tratamientos
		</a>
		<a href="{{ URL::to('tratamiento/delete/'.$tratamiento->id) }}"
		class="btn text-danger pull-right">
		Eliminar este tratamiento (cuidado, esta accion es permanente)
		</a>
	</p>

@stop
