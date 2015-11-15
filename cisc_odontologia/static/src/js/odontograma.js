 openerp.cisc_odontologia = function (instance) {
    instance.web.client_actions.add('cisc.action', 'instance.cisc_odontologia.Action');
    instance.cisc_odontologia.Action = instance.web.Widget.extend({
        start: function () {
		var left = (screen.width/2)-(1650/2);
  		var top = (screen.height/2)-(650/2);
  		return window.open('http://localhost/odontograma/public/index.php', 'ODONTOGRAMA', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, 	copyhistory=no, width='+1350+', height='+450+', top='+top+', left='+left)
        }
    });
 };
