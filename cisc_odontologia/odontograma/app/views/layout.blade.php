<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Odontograma</title>
	
	{{ HTML::script('assets/js/jquery.js') }}
	{{ HTML::script('assets/js/bootstrap.js') }}

	{{ HTML::style('assets/css/bootstrap.css') }}
	{{ HTML::style('assets/css/bootstrap-theme.min.css') }}
	
</head>
<body>
	<!-- Fixed navbar -->
		<div class="navbar navbar-default navbar-static-top" role="navigation">
			<div class="container">
				<div class="navbar-header">
					<a class="navbar-brand" href="{{ URL::to('/index.php') }}">
						Odontograma
					</a>
				</div>
				<div class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
						<li id="menu_api">
							<a href="{{ URL::to('api') }}">
								API
							</a>
						</li>
						<li id="menu_diagnostico">
							<a href="{{ URL::to('diagnostico') }}">
								Diagnosticos
							</a>
						</li>
						<li id="menu_tratamientos">
							<a href="{{ URL::to('tratamientos') }}">
								Tratamientos
							</a>
						</li>
						<li id="menu_pacientes">
							<a href="{{ URL::to('pacientes') }}">
								Pacientes
							</a>
						</li>
					</ul>
				</div><!--/.nav-collapse -->
			</div><!--/.container -->
		</div>
		<!-- *************************************************************** -->

		<div class="container">
			<div class="row">
				@yield('content')
			</div>
		</div>
		<script>
			$('#menu_{{ $section or "" }}').addClass('active');
		</script>
</body>
</html>
