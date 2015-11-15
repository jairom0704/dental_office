@extends('layout')

@section('content')
<div class="page-header">
		<div class="pull-right form-inline">
			<a href="{{ URL::to('paciente/new/') }}" class="btn btn-primary">
				<span class="glyphicon glyphicon-plus"></span>
				Nuevo Paciente
			</a>
		</div>

		<h3>Pacientes</h3>
	</div>
	

<div class="table-responsive panel panel-default">
	<table class="table table-striped table-hover">
		<thead>
			<tr>
				<th>Nombre</th>
				<th>Cedula</th>
				<th>Historia clinica</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			@foreach($pacientes as $paciente)
			<tr>
				<td>
					<a href="{{ URL::to('paciente/view/'.$paciente->id) }}">
						{{ $paciente->name }}
					</a>
				</td>
				<td>{{ $paciente->cedula  	}}</td>
				<td>{{ $paciente->number 	}}</td>
				<td>
					<a href="{{ URL::to('paciente/delete/'.$paciente->id) }}" class="delete_option">
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
				Deseas eliminar este paciente?
			</h4>
		</div>
		<div class="modal-body">
			<a href="#" class="pull-left btn" data-dismiss="modal">
				No, cierra esta pantalla
			</a>
			<a href="#" class="pull-right btn btn-danger">
				Si, elimina el paciente
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
{{ $pacientes->links() }}
@stop
