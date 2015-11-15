@extends('layout')

@section('content')
<div class="page-header">
		<div class="pull-right form-inline">
			<a href="{{ URL::to('tratamiento/new/') }}" class="btn btn-primary">
				<span class="glyphicon glyphicon-plus"></span>
				Nuevo Tratamiento
			</a>
		</div>

		<h3>Tratamientos</h3>
	</div>
	

<div class="table-responsive panel panel-default">
	<table class="table table-striped table-hover">
		<thead>
			<tr>
				<th>Nombre</th>
				<th>Estado</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			@foreach($tratamientos as $tratamiento)
			<tr>
				<td>
					<a href="{{ URL::to('tratamiento/view/'.$tratamiento->id) }}">
						{{ $tratamiento->name }}
					</a>
				</td>
				<td>
					{{ ($tratamiento->activo === '1')? 'Habilitado' : 'Deshabilitado'	}}
				</td>
				<td>
					<a href="{{ URL::to('tratamiento/delete/'.$tratamiento->id) }}" class="delete_option">
					<span class="glyphicon glyphicon-trash"></span>
					</a>
				</td>
			</tr>
			@endforeach
		</tbody>
	</table>
</div>
<div class="modal fade" id="delete-modal">
  <div class="modal-dialog">
	<div class="modal-content">
		<div class="modal-header">
			<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
			<h4 class="modal-title">
				Deseas eliminar este tratamiento?
			</h4>
		</div>
		<div class="modal-body">
			<a href="#" class="pull-left btn" data-dismiss="modal">
				No, cierra esta pantalla
			</a>
			<a href="#" class="pull-right btn btn-danger">
				Si, elimina el tratamiento
			</a>
			<p class="clearfix"></p>
		</div>
	</div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

<script>
	$('.delete_option').click(function(){
		$('#delete-modal a.btn-danger').attr("href",$(this).attr('href'));
		$('#delete-modal').modal({show:true});
		return false;
	});
</script>
{{ $tratamientos->links() }}
@stop
