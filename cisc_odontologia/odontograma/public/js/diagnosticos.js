/*


 Manejo de diágnosticos
 -----------------------
	clases:
		Paciente
		Diagnosticos

	Eventos:
		buscar paciente
		grabar diagnostico
------------------------------------------------------*/

/*var ROOT_PATH = '../public/';*/
	ROOT_PATH = '../public';

/*
==================================================================
 PACIENTES
  - buscar: realiza la busqueda de un paciente por cedula o nombre
  - mostrar_informacion: muestra la informacion del paciente y la expone publicamente
	para poder utilizarla
==================================================================
*/	
	var Paciente = {
		buscar: function()
			{
				var q        = $('#q').val();
				var endpoint = "con_nombre/";


				if( $.isNumeric( q ) )
					endpoint ="con_cedula/";


				$.ajax({
					type : "GET",
					url  : ROOT_PATH+"paciente/"+endpoint+q,
					success: Paciente.mostrar_informacion
				});
			},

		/*------------------------------------------------------*/

		mostrar_informacion: function( data )
			{
				$("#form_paciente_id" 		).val( data[0].id 		);
				$("#form_paciente_nombre" 	).html( data[0].name 	);
				$("#form_paciente_cedula" 	).html( data[0].cedula 	);
				//$("#form_paciente_telefono"	).html( data[0].telefono );
				$("#form_paciente_number" 	).html( data[0].number 	);

				$(".requiere_id_paciente").show();
				Diagnostico.recuperar_historial();
			}
	};


	
	
/*
==================================================================
 DIAGNOSTICOS
	- grabar: grabar nuevos diagnosticos del odontograma o 
		actualizar los ya existentes
	- grabado: actualiza el historial con la nueva informacion grabada
	- recuperar_historial: devuelve los 10 ultimos diagnosticos que se
		le haya realizado al paciente oredenados cronologicamente.
	- visualizar: añade los datos de un diagnostico a la lista de tratamientos
		seleccionados y renderiza el odontograma con la nueva informacion.
	- mostrar_historial: escribe el listado de los 10 ultimos diagnosticos
		en el combo box de historial.
==================================================================
*/
	var Diagnostico =
	{
		grabar: function( data, id )
		{
			var endpoint = "save";

			if( id !== '' )
			{
				data["id"] = id;
				endpoint = "update";
			}

			$.ajax({
				type : "POST",
				url  : ROOT_PATH+"diagnostico/"+endpoint,
				data : data,
				success: Diagnostico.grabado
			});
		},
		/*------------------------------------------------------*/

		grabado: function( data )
		{
			Diagnostico.recuperar_historial();
		},
		/*------------------------------------------------------*/


		recuperar_historial: function()
		{
			$.ajax({
				type    : "GET",
				url     : ROOT_PATH+"diagnostico/view/"+$('#form_paciente_id').val(),
				success : Diagnostico.mostrar_historial
			});
		},
		/*------------------------------------------------------*/


		visualizar: function ( data )
		{
			vm.tratamientosAplicados([]);
			vm.tratamientosRealizados([]);
			$('#observaciones').val('');
			var id = null;
			

			if( data !== null && typeof data !== 'undefined')
			{
				id = data.id;
				var d = JSON.parse(data.diagnostico);
				for (var i = d.length - 1; i >= 0; i--) {
					var tratamiento = d[i];
					vm.tratamientosAplicados.push(tratamiento);
				};

				console.log(d);
				var r = JSON.parse(data.diagnostico_realizado);
				console.log(r);
				for (var i = r.length - 1; i >= 0; i--) {
					var tratamiento = r[i];
					vm.tratamientosRealizados.push(tratamiento);
				};


				$('#observaciones').val(data.observacion);
			}


			$('#form_diagnostico_id').val(id);
			render_odontograma();
		},
		/*------------------------------------------------------*/


		mostrar_historial: function ( data )
		{
			vm.historialDiagnosticos([]);
			for (var i = 0; i < data.length; i++) {
				vm.historialDiagnosticos.push(data[i])
			};

			vm.tratamientosAplicados([]);
			vm.tratamientosRealizados([]);
			vm.diagnosticoSeleccionado();
			render_odontograma();
		},
		/*------------------------------------------------------*/
	 };


	
/*
==================================================================
 EVENTOS
==================================================================
*/

	/* 
	 * Busco los datos de un paciente
	 *------------------------------------------------------*/
	$("#form_buscar_paciente").submit(function()
	{
		Paciente.buscar();
		$(this).get(0).reset();
		return false;
	});


	/* 
	 * Grabo o actualizo los cambios en el diagnostico
	 *------------------------------------------------------*/
	$("#grabar").click(function()
	{
		var id                       = $('#form_diagnostico_id').val();
		var tratamientos             = ko.contextFor($('#diagnostico_listado').get(0)).$data.tratamientosAplicados();
		var tratamientos_realizados  = ko.contextFor($('#diagnostico_hecho_listado').get(0)).$data.tratamientosRealizados();
		var diagnostico_por_realizar = String( $('#diagnostico_listado').text() ).replace(/(?:\r\n|\r|\t|  |\n)/g, '').replace(/(?:\| Eliminar)/g,', ');
		var diagnostico_realizado    = String( $('#diagnostico_hecho_listado').text() ).replace(/(?:\r\n|\r|\t|  |\n)/g, '').replace(/(?:\| Eliminar)/g,', ');

		
		if( tratamientos_realizados.length == 0)
                {
			if ( tratamientos.length == 0)
				{
					alert('DEBES GUARDAR AL MENOS UN REGISTRO!!');
		                        return;
				}
                }


		/*if( !tratamientos.length)
		{
			alert('Por lo menos una de las piezas dentales debe tener un tratamiento para poder guardar el odontograma');
			return;
		}*/

		var data  = {
			paciente_id                 : $("#form_paciente_id").val(),
			diagnostico                 : JSON.stringify(tratamientos),
			diagnostico_realizado       : JSON.stringify(tratamientos_realizados),
			diagnostico_final           : diagnostico_por_realizar,
			diagnostico_final_realizado : diagnostico_realizado,
			observacion                 : $('#observaciones').val()
		}
		
		Diagnostico.grabar( data, id );
		return false;
	});


	/*------------------------------------------------------*/
	$(".requiere_id_paciente").hide();



/*
==================================================================
 BINDING KNOCKOUT SELECT2
 	- permite la busqueda dentro del combo box de codigos CIE
==================================================================
*/
	ko.bindingHandlers.select2 = {
		init: function(el, valueAccessor, allBindingsAccessor, viewModel)
		{
			ko.utils.domNodeDisposal.addDisposeCallback(el, function() {
				$(el).select2('destroy');
			});

			var allBindings = allBindingsAccessor(),
				select2 = ko.utils.unwrapObservable(allBindings.select2);

			$(el).select2(select2);
		},
		update: function (el, valueAccessor, allBindingsAccessor, viewModel)
		{
			var allBindings = allBindingsAccessor();

			if ("value" in allBindings) {
				if (allBindings.select2.multiple && allBindings.value().constructor != Array) {                
					$(el).select2("val", allBindings.value().split(","));
				}
				else {
					$(el).select2("val", allBindings.value());
				}
			} else if ("selectedOptions" in allBindings) {
				var converted = [];
				var textAccessor = function(value) { return value; };
				if ("optionsText" in allBindings) {
					textAccessor = function(value) {
						var valueAccessor = function (item) { return item; }
						if ("optionsValue" in allBindings) {
							valueAccessor = function (item) { return item[allBindings.optionsValue]; }
						}
						var items = $.grep(allBindings.options(), function (e) { return valueAccessor(e) == value});
						if (items.length == 0 || items.length > 1) {
							return "UNKNOWN";
						}
						return items[0][allBindings.optionsText];
					}
				}
				$.each(allBindings.selectedOptions(), function (key, value) {
					converted.push({id: value, text: textAccessor(value)});
				});
				$(el).select2("data", converted);
			}
		}
	};
 /*----------------------------------------------------------------------*/
 
