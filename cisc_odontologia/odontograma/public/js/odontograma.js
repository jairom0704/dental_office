/* 
 * Cambio: creo esta variable necesaria para acceder a la
 * funcion de renderizado del odontograma desde la clase 
 * de diagnostico.
 *------------------------------------------------------*/
var render_odontograma = null;


jQuery(function(){

	function drawDiente(svg, parentGroup, diente){
		if(!diente) throw new Error('Error no se ha especificado el diente.');
		
		var x = diente.x || 0,
			y = diente.y || 0;
		
		var defaultPolygon = {fill: 'white', stroke: 'navy', strokeWidth: 0.5};
		var dienteGroup = svg.group(parentGroup, {transform: 'translate(' + x + ',' + y + ')'});

		var caraSuperior = svg.polygon(dienteGroup,
			[[0,0],[20,0],[15,5],[5,5]],  
		    defaultPolygon);
	    caraSuperior = $(caraSuperior).data('cara', 'S');
		
		var caraInferior =  svg.polygon(dienteGroup,
			[[5,15],[15,15],[20,20],[0,20]],  
		    defaultPolygon);			
		caraInferior = $(caraInferior).data('cara', 'I');

		var caraDerecha = svg.polygon(dienteGroup,
			[[15,5],[20,0],[20,20],[15,15]],  
		    defaultPolygon);
	    caraDerecha = $(caraDerecha).data('cara', 'D');
		
		var caraIzquierda = svg.polygon(dienteGroup,
			[[0,0],[5,5],[5,15],[0,20]],  
		    defaultPolygon);
		caraIzquierda = $(caraIzquierda).data('cara', 'Z');		    
		
		var caraCentral = svg.polygon(dienteGroup,
			[[5,5],[15,5],[15,15],[5,15]],  
		    defaultPolygon);	
		caraCentral = $(caraCentral).data('cara', 'C');		    
	    
	    var caraCompleto = svg.text(dienteGroup, 6, 30, diente.id.toString(), 
	    	{fill: 'navy', stroke: 'navy', strokeWidth: 0.1, style: 'font-size: 6pt;font-weight:normal'});
    	caraCompleto = $(caraCompleto).data('cara', 'X');
    	
		//Busco los tratamientos aplicados al diente
		var tratamientosAplicadosAlDiente = ko.utils.arrayFilter(vm.tratamientosAplicados(), function(t){
			return t.diente.id == diente.id;
		});
		var tratamientosRealizadosAlDiente = ko.utils.arrayFilter(vm.tratamientosRealizados(), function(t){
			return t.diente.id == diente.id;
		});
		var caras = [];
		caras['S'] = caraSuperior;
		caras['I'] = caraInferior;
		caras['C'] = caraCentral;
		caras['X'] = caraCompleto;
		caras['Z'] = caraIzquierda;
		caras['D'] = caraDerecha;

		for (var i = tratamientosAplicadosAlDiente.length - 1; i >= 0; i--) {
			var t = tratamientosAplicadosAlDiente[i];
			caras[t.cara].attr('fill', 'red');

			if( t.cara === 'X' )
			{
				caras['S'].attr('fill', 'red');
				caras['I'].attr('fill', 'red');
				caras['C'].attr('fill', 'red');
				caras['D'].attr('fill', 'red');
				caras['Z'].attr('fill', 'red');
			}
				
		};

		for (var i = tratamientosRealizadosAlDiente.length - 1; i >= 0; i--) {
			var t = tratamientosRealizadosAlDiente[i];
			caras[t.cara].attr('fill', 'blue');
    
			if( t.cara === 'X' )
			{
				caras['S'].attr('fill', 'blue');
				caras['I'].attr('fill', 'blue');
				caras['C'].attr('fill', 'blue');
				caras['D'].attr('fill', 'blue');
				caras['Z'].attr('fill', 'blue');
			}
				
		};

		$.each([caraCentral, caraIzquierda, caraDerecha, caraInferior, caraSuperior, caraCompleto], function(index, value){
	    	value.click(function(){
	    		var me = $(this);
	    		var cara = me.data('cara');
				
				if(!vm.tratamientoSeleccionado() && !vm.tratamientoRealizado){
					alert('Debe seleccionar un código CIE previamente.');	
					return false;
				}

				//Validaciones
				//Validamos el tratamiento
				/* 
	 			* Cambio: ahora se debe parsear el tratamiento, por que 
	 			* para poder usar la busqueda con select2 tuve que convertir
	 			* el valor del select en texto plano.
	 			*------------------------------------------------------*/
	 			if(!vm.tratamientoSeleccionado() === false )
	 			{
					var tratamiento = JSON.parse(vm.tratamientoSeleccionado());

					if(cara == 'X' && !tratamiento.aplicadiente){
						alert('El código CIE seleccionado no se puede aplicar a toda la pieza.');
						return false;
					}
					if(cara != 'X' && !tratamiento.aplicacara){
						alert('El código CIE seleccionado no se puede aplicar a una cara.');
						return false;
					}
					VerificarTratamiento(diente, cara);
					vm.tratamientosAplicados.push({diente: diente, cara: cara, nomenclatura: obtener_nombre(cara, diente), tratamiento: tratamiento});
					vm.tratamientoSeleccionado(null);
				}
				
				//Validaciones
				//Validamos el tratamiento
				/* 
	 			* Cambio: se aumenta el mismo procedimiento pero para los
	 			* tratamientos realizados
	 			*------------------------------------------------------*/
	 			if(vm.tratamientoRealizado === true )
	 			{
					VerificarTratamiento(diente, cara);
					vm.tratamientosRealizados.push({diente: diente, cara: cara, nomenclatura: obtener_nombre(cara, diente), tratamiento: ''});
				}
				
				//Actualizo el SVG
				renderSvg();
	    	}).mouseenter(function(){
	    		var me = $(this);
	    		me.data('oldFill', me.attr('fill'));
	    		me.attr('fill', 'yellow');
	    	}).mouseleave(function(){
	    		var me = $(this);
	    		me.attr('fill', me.data('oldFill'));
	    	});			
		});
	};


	function VerificarTratamiento( diente, cara )
	{
		var tratamientosAplicadosAlDiente = ko.utils.arrayFilter(vm.tratamientosAplicados(), function(t){
			return t.diente.id == diente.id;
		});
		var tratamientosRealizadosAlDiente = ko.utils.arrayFilter(vm.tratamientosRealizados(), function(t){
			return t.diente.id == diente.id;
		});

		console.log(tratamientosAplicadosAlDiente);
		console.log('----------------------------------------')
		console.log(tratamientosRealizadosAlDiente);

		for (var i = tratamientosAplicadosAlDiente.length - 1; i >= 0; i--) {
			console.log('hay por lo menos un tratamiento aplicado');
			var t = tratamientosAplicadosAlDiente[i];
			console.log(t);
			console.log('compruebo si se aplica el tratamiento a la misma cara:')
			console.log(t.cara +'-'+ cara);
			if( t.cara === cara )
			{
				vm.tratamientosAplicados.remove(t);
			}
		};

		for (var i = tratamientosRealizadosAlDiente.length - 1; i >= 0; i--) {
			var t = tratamientosRealizadosAlDiente[i];
			if( t.cara == cara )
			{
				vm.tratamientosRealizados.remove(t);
			}
		};
	}




	function renderSvg(){
		console.log('update render');

		var svg = $('#odontograma').svg('get').clear();
		var parentGroup = svg.group({transform: 'scale(1.5)'});
		var dientes = vm.dientes();
		for (var i =  dientes.length - 1; i >= 0; i--) {
			var diente =  dientes[i];
			var dienteUnwrapped = ko.utils.unwrapObservable(diente); 
			drawDiente(svg, parentGroup, dienteUnwrapped);
		};
	}
	/* 
	 * Cambio: expongo en el entorno publico la funcion de renderSvg
	 *------------------------------------------------------*/
	render_odontograma = renderSvg;

	//View Models
	function DienteModel(id, x, y){
		var self = this;

		self.id = id;	
		self.x = x;
		self.y = y;		
	};

	function ViewModel(){
		var self = this;

		self.tratamientosPosibles    = ko.observableArray([]);
		self.tratamientoSeleccionado = ko.observable(null);
		self.tratamientosAplicados   = ko.observableArray([]);
		self.tratamientosRealizados  = ko.observableArray([]);
		self.tratamientoRealizado    = false;

		/* 
		 * Cambio: añadido los bindings para el diagnostico
		 *------------------------------------------------------*/
		self.historialDiagnosticos   = ko.observableArray([]);
		self.diagnosticoSeleccionado = ko.observable(null);
		/*------------------------------------------------------*/


		/* 
		 * Cambio: añadido evento cuando selecciono otro diagnostico
		 * del combo box
		 *------------------------------------------------------*/
		self.diagnosticoSeleccionado.subscribe(function(newValue) {
			Diagnostico.visualizar(newValue);
		});
		/*------------------------------------------------------*/



		/* 
		 * Cambio: Funcion para intercambiar el modo de tratamiento
		 * 'por realizar' o 'realizado' segun el tab seleccionado 
		 * desde la pantalla de usuario
		 *------------------------------------------------------*/
		self.toggleTrueTipoTratamiento = function(vm){
			vm.tratamientoRealizado = true;
			return true;
		}
		self.toggleFalseTipoTratamiento = function(vm){
			vm.tratamientoRealizado = false;
			return true;
		}
		/*------------------------------------------------------*/



		self.quitarTratamiento = function(tratamiento){
			self.tratamientosAplicados.remove(tratamiento);
			renderSvg();
		}

		self.quitarTratamientoRealizado = function(tratamiento){
			self.tratamientosRealizados.remove(tratamiento);
			renderSvg();
		}

		//Cargo los dientes
		var dientes = [];
		//Dientes izquier
		for(var i = 0; i < 8; i++){
			dientes.push(new DienteModel(18 - i, i * 25, 0));	
		}
		for(var i = 3; i < 8; i++){
			dientes.push(new DienteModel(55 - i, i * 25, 1 * 40));	
		}
		for(var i = 3; i < 8; i++){
			dientes.push(new DienteModel(85 - i, i * 25, 2 * 40));	
		}
		for(var i = 0; i < 8; i++){
			dientes.push(new DienteModel(48 - i, i * 25, 3 * 40));	
		}
		//Dientes derechos
		for(var i = 0; i < 8; i++){
			dientes.push(new DienteModel(21 + i, i * 25 + 210, 0));	
		}
		for(var i = 0; i < 5; i++){
			dientes.push(new DienteModel(61 + i, i * 25 + 210, 1 * 40));	
		}
		for(var i = 0; i < 5; i++){
			dientes.push(new DienteModel(71 + i, i * 25 + 210, 2 * 40));	
		}
		for(var i = 0; i < 8; i++){
			dientes.push(new DienteModel(31 + i, i * 25 + 210, 3 * 40));	
		}

		self.dientes = ko.observableArray(dientes);
	};

	vm = new ViewModel();
	
	//Inicializo SVG
    $('#odontograma').svg({
        settings:{ width: '620px', height: '250px' }
    });

	ko.applyBindings(vm);

	//TODO: Cargo el estado del odontograma
	renderSvg();



	var nombres     = new Array();
	nombres[1]      = new Array();
	nombres[1]['Z'] = 'DISTAL';
	nombres[1]['S'] = 'VESTIBULAR';
	nombres[1]['D'] = 'MESIAL';
	nombres[1]['I'] = 'PALATINA';
	nombres[1]['C'] = 'OCLUSAR';
	nombres[1]['X'] = 'DIENTE COMPLETO';

	nombres[2]      = new Array();
	nombres[2]['Z'] = 'MESIAL';
	nombres[2]['S'] = 'VESTIBULAR';
	nombres[2]['D'] = 'DISTAL';
	nombres[2]['I'] = 'PALATINA';
	nombres[2]['C'] = 'OCLUSAR';
	nombres[2]['X'] = 'DIENTE COMPLETO';

	nombres[3]      = new Array();
	nombres[3]['Z'] = 'MESIAL';
	nombres[3]['S'] = 'LINGUAL';
	nombres[3]['D'] = 'DISTAL';
	nombres[3]['I'] = 'VESTIBULAR';
	nombres[3]['C'] = 'OCLUSAR';
	nombres[3]['X'] = 'DIENTE COMPLETO';

	nombres[4]      = new Array();
	nombres[4]['Z'] = 'DISTAL';
	nombres[4]['S'] = 'LINGUAL';
	nombres[4]['D'] = 'MESIAL';
	nombres[4]['I'] = 'VESTIBULAR';
	nombres[4]['C'] = 'OCLUSAR';
	nombres[4]['X'] = 'DIENTE COMPLETO';

	function obtener_nombre( cara, diente )
	{
		var cuadrante = 0;
		if( (diente.id > 10 && diente.id < 20) || (diente.id > 47 && diente.id < 53) )
			cuadrante = 1;
		else
		if( (diente.id > 20 && diente.id < 30) || (diente.id > 60 && diente.id < 66) )
			cuadrante = 2;
		else
		if( (diente.id > 30 && diente.id < 40) || (diente.id > 70 && diente.id < 76) )
			cuadrante = 3;
		else
		if( (diente.id > 40 && diente.id < 50) || (diente.id > 77 && diente.id < 83) )
			cuadrante = 4;

		return nombres[cuadrante][cara];
	}


	//Cargo los tratamientos
	/* 
	 * Cambio: apunta al API y no a un archivo json
	 *------------------------------------------------------*/
	$.getJSON('http://localhost/odontograma/public/tratamientos/list', function(d){
	//$.getJSON('http://127.0.0.1:8000/tratamientos/list', function(d){
		for (var i = d.length - 1; i >= 0; i--) {
			var tratamiento = d[i];
			vm.tratamientosPosibles.push(tratamiento);
		};
	});
});
