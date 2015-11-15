<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en"> <![endif]-->
<!-- Consider adding an manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
	<meta charset="utf-8">

	<!-- Use the .htaccess and remove these lines to avoid edge case issues.
			 More info: h5bp.com/b/378 -->
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

	<title></title>
	<meta name="description" content="">
	<meta name="author" content="">

	<!-- Mobile viewport optimized: j.mp/bplateviewport -->
	<meta name="viewport" content="width=device-width,initial-scale=1">

	<!-- Place favicon.ico and apple-touch-icon.png in the root directory: mathiasbynens.be/notes/touch-icons -->

	<!-- CSS: implied media=all -->
	<!-- CSS concatenated and minified via ant build script-->
	<link rel="stylesheet" href="./css/style.css">
	<link rel="stylesheet" href="./css/jquery-ui-1.8.17.custom.css">
	<link rel="stylesheet" href="./css/jquery.svg.css">
	<link rel="stylesheet" href="./css/select2.css">
	<link rel="stylesheet" href="./css/odontograma.css">
	<link rel="stylesheet" href="./css/tab.css">
	<!-- end CSS-->

	<!-- More ideas for your <head> here: h5bp.com/d/head-Tips -->

	<!-- All JavaScript at the bottom, except for Modernizr / Respond.
			 Modernizr enables HTML5 elements & feature detects; Respond is a polyfill for min/max-width CSS3 Media Queries
			 For optimal performance, use a custom Modernizr build: www.modernizr.com/download/ -->
	<script src="./js/modernizr-2.0.6.min.js"></script>
</head>

<body>

	<div id="container">
		<header>
			<!-- 
				Cambio: formulario para buscar paciente por nombre o cedula
			*************************************************************-->
			<form action="#" id="form_buscar_paciente">
				<strong>CEDULA PACIENTE </strong>
				<input type="text" name="q" id="q" >
				<input type="submit" value="BUSCAR">
			</form>
			<!-- ************************************************************* -->
		</header>

		<div class="requiere_id_paciente">
				<!-- 
					Cambio: formulario para mostrar los datos del paciente
				*************************************************************-->
				<form action="#" method="get" id="form_paciente">
							<input type="hidden" name="id" id="form_paciente_id">
				</form>
				<p>
			<strong>HISTORIAL CLINICO:</strong>
			<span id="form_paciente_number"></span>
			<strong>CEDULA:</strong>
			<span id="form_paciente_cedula"></span>, 
			<strong>NOMBRE:</strong>
			<span id="form_paciente_nombre"></span>, 
			<!--<input type="text" name="telefono" id="form_paciente_telefono">
			<label>email:</label>-->
			
				</p>
						
				<!-- ************************************************************ -->

				<hr>

				<!-- 
					Cambio: formulario con los datos del diagnóstico
				*************************************************************-->
				<form action="#" method="get" id="form_diagnostico">
					<fieldset>
						<legend>DIAGNÓSTICO</legend>
						<select 
							data-bind=" options: historialDiagnosticos, 
													value: diagnosticoSeleccionado, 
													optionsText: function(item){
																					var t = item.created_at.split(/[- :]/)
																					var created_at = new Date(t[0], t[1]-1, t[2], t[3], t[4], t[5]);
																					var date = new Date(created_at.getTime() - (5*60*60*1000));
																					return item.secuencial+'&nbsp;&nbsp;&nbsp;  Fecha:&nbsp;'+date.toLocaleString();
																				},
													optionsCaption: 'Nuevo diagnóstico'">
						</select>
						<input type="hidden" name="id" id="form_diagnostico_id">
						<input type="button" name="Grabar" value="Grabar diagnóstico" id="grabar">
					</fieldset>
				</form>
				<!-- ************************************************************ -->

		</div>



		<div id="main" role="main"  class="requiere_id_paciente">
		
			<div id="tratamiento">
				<ul class="tabs">
					<li>
						<input type="radio" name="tabs" id="tab1" checked  data-bind="click: $root.toggleFalseTipoTratamiento"/>
						<label for="tab1">Por realizar</label>
						<div id="tab-content1" class="tab-content">
							
							<select id="hola2"
								data-bind=" options        : tratamientosPosibles, 
											optionsText    : function(item){ return item.name+' - '+item.codigo; },
											optionsValue   : function(item){ return JSON.stringify(item); },
											optionsCaption : 'Seleccione un código CIE/Otros',
											value          : tratamientoSeleccionado,
											select2        : {}
											">
							</select>


							<ul data-bind="foreach: tratamientosAplicados" id="diagnostico_listado">
								<li>
									P<span data-bind="text: diente.id"></span> 
									C. <span data-bind="text: nomenclatura"></span> 
									- [<span data-bind="text: tratamiento.codigo"></span> 
									<span data-bind="text: tratamiento.name"></span>]
									| 
									<a href="#" data-bind="click: $parent.quitarTratamiento">Eliminar</a>
								</li>
							</ul>
						</div>
					</li>

					<li>
						<input type="radio" name="tabs" id="tab2" data-bind="click: $root.toggleTrueTipoTratamiento"/>
						<label for="tab2">Realizados</label>
						<div id="tab-content2" class="tab-content">
							<ul data-bind="foreach: tratamientosRealizados" id="diagnostico_hecho_listado">
								<li>
									P<span data-bind="text: diente.id"></span> 
									C. <span data-bind="text: nomenclatura"></span>
									| 
									<a href="#" data-bind="click: $parent.quitarTratamientoRealizado">Eliminar</a>
								</li>
							</ul>
						</div>
					</li>
				</ul>
				<br/>
			</div>
			<div id="odontograma-wrapper">
				<h2>ODONTOGRAMA</h2>
				<div id="odontograma"></div>
			</div>      
		</div>
		<footer class="requiere_id_paciente">
			<hr>
			<strong>OBSERVACIONES</strong>
			<br />
			<textarea name="observaciones" id="observaciones"></textarea>
		</footer>
	</div> <!--! end of #container -->  

	<!-- scripts concatenated and minified via ant build script-->
	<script defer src="./js/jquery-2.1.3.min.js"></script>
	<script defer src="./js/plugins.js"></script>
	<script defer src="./js/jquery-ui-1.8.17.custom.min.js"></script>
	<script defer src="./js/jquery.tmpl.js"></script>
	<script defer src="./js/knockout-min.js"></script>
	<!--<script defer src="./js/knockout-2.0.0.js"></script>-->
	<script defer src="./js/jquery.svg.min.js"></script>  
	<script defer src="./js/jquery.svggraph.min.js"></script>  
	<script defer src="./js/select2.js"></script>  
	<script defer src="./js/odontograma.js"></script>
	<script defer src="./js/diagnosticos.js"></script>
	<!-- end scripts-->

	
	<!-- Change UA-XXXXX-X to be your site's ID -->
	<script>
		window._gaq = [['_setAccount','UAXXXXXXXX1'],['_trackPageview'],['_trackPageLoadTime']];
		Modernizr.load({
			load: ('https:' == location.protocol ? '//ssl' : '//www') + '.google-analytics.com/ga.js'
		});
	</script>


	<!-- Prompt IE 6 users to install Chrome Frame. Remove this if you want to support IE 6.
			 chromium.org/developers/how-tos/chrome-frame-getting-started -->
	<!--[if lt IE 7 ]>
		<script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js"></script>
		<script>window.attachEvent('onload',function(){CFInstall.check({mode:'overlay'})})</script>
	<![endif]-->
	
</body>
</html>
