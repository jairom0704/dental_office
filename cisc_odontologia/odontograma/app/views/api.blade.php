@extends('layout')

@section('content')
		<div class="page-header">
			<h2>API Odontograma</h2>
		</div>
		<div class="panel panel-default clearfix">
			<div class="panel-heading">
				Listado de Endpoints
			</div>
			<ul class="list-group">
				<li class="list-group-item">
					<h3>Pacientes por cédula</h3>
					<h4>
						<a href="./public/paciente/con_cedula/0909767676">
						http://www.dominio.com/public/paciente/con_cedula/000000
						</a>
					</h4>
					<p>
						<strong>Metodo:</strong> GET
						<br>
						<strong>Parametros:</strong> Cedula
						<br>
						<strong>Descripcion:</strong> busca el paciente al que pertenece la cedula dada.
					</p>	
				</li>
				<li class="list-group-item">
					<h3>Pacientes por nombre</h3>
					<h4>
						<a href="./public/paciente/con_nombre/perico de los palotes">
						http://www.dominio.com/public/paciente/con_nombre/000000
						</a>
					</h4>
					<p>
						<strong>Metodo:</strong> GET
						<br>
						<strong>Parametros:</strong> nombre
						<br>
						<strong>Descripcion:</strong> busca el paciente por el nombre dado.
					</p>	
				</li>
				<li class="list-group-item">
					<h3>Grabar diagnóstico</h3>
					<h4>
						<a href="./public/diagnostico/save">
						http://www.dominio.com/public/diagnostico/save?id_paciente=0000&diagnostico={JSON}
						</a>
					</h4>
					<p>
						<strong>Metodo:</strong> POST
						<br>
						<strong>Parametros:</strong> id_paciente, diagnostico
						<br>
						<strong>Descripcion:</strong> graba el objeto del diagnostico asociandolo a un id de paciente. Si ya existe un registro asociado a ese paciente entonces sobreescribe el diagnostico con el nuevo objeto json.
					</p>	
				</li>
				<li class="list-group-item">
					<h3>Pedir los diagnósticos de un paciente</h3>
					<h4>
						<a href="./public/diagnostico/view/1">
						http://www.dominio.com/public/diagnostico/view/000000
						</a>
					</h4>
					<p>
						<strong>Metodo:</strong> GET
						<br>
						<strong>Parametros:</strong> id_paciente
						<br>
						<strong>Descripcion:</strong> retorna un arreglo de los diagnósticos asociados al id de paciente. vacío en caso de no encontrarse ningún diagnóstico previo.
					</p>	
				</li>
				<li class="list-group-item">
					<h3>Listado de tratamientos habilitados</h3>
					<h4>
						<a href="./public/tratamientos/list">
						http://www.dominio.com/public/tratamientos/list
						</a>
					</h4>
					<p>
						<strong>Metodo:</strong> GET
						<br>
						<strong>Parametros:</strong> 
						<br>
						<strong>Descripcion:</strong> devuelve el listado de tratamientos ingresados en la base de datos.
					</p>	
				</li>
			</ul>
		</div>
	</div>
	<script src="http://192.168.0.5:35729/livereload.js"></script>
</body>
</html>
@stop
