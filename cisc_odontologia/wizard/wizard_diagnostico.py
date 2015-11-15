# -*- encoding: utf-8 -*-
########################################################################
#
# @authors: Jairo Troncoso
# Copyright (C) 2015 Odontologia
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This module is GPLv3 or newer and incompatible
# with OpenERP SA "AGPL + Private Use License"!
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see http://www.gnu.org/licenses.
########################################################################
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime, timedelta
import time


class wizard_diagnostico(osv.osv_memory):
    
    _name='wizard.diagnostico'
    _columns={
                'specialty':fields.selection([
                  ('clinica','Clinica Integral'),
                  ('operatoriapb','Operatoria PB'),
                  ('cirugiapb','Cirugía PB'),
                  ('odontopediatria','Odontopediatria'),
                  ('ortodoncia','Ortodoncia'),
                   ('operatoriapb','Operatoria PA'),
                  ('cirugiapa','Cirugía PA'),
                   ],    'Especialidad',  select=True, required=True),
               'student_id': fields.many2one('res.users', 'Estudiante', required=False, domain=[('student','=',True)]),
               'teaching_id': fields.many2one('res.users', 'Docente', required=False, domain=[('teaching','=',True)]),
               'paciente_id':fields.many2one('medicalhistories', 'Historial Clinico', readonly=True),
               'name': fields.char('Paciente' ,readonly=True),
               'consulta_id':fields.many2one('patient.consultation', 'Consulta', required=True, domain=[('state','=','open')]),
              }
    
    def default_get(self, cr, uid, fields_list, context=None):
        if not context:
            context={}
        consulta=[]
        values = super(wizard_diagnostico, self).default_get(cr, uid, fields_list, context)
        odontograma = self.pool.get('odontogramadetails').browse(cr , uid , context.get('active_id'))
        consulta_ids = self.pool.get('patient.consultation').search(cr, uid, [('medical_history_id','=',odontograma.paciente_id.id),('state','=','open')])
        if not consulta_ids:
            raise osv.except_osv(_(u'Advertencia'), _(u'No existe consultas en estado [ABIERTA] asociada a la historial clinico %s, por favor verifique!!!') % odontograma.paciente_id.number)
        else:
            values['consulta_id']= consulta_ids[0]
            values['line_ids']= consulta
            values['paciente_id']= odontograma.paciente_id.id
            values['name']= odontograma.name
        return values 
    
    
    def process(self, cr , uid, ids, context=None):
        if not context: context={}
        wizard = self.browse(cr ,uid , ids[0])
        if wizard.consulta_id:
            if wizard.consulta_id.medical_history_id.id != wizard.paciente_id.id:
                raise osv.except_osv(_(u'Advertencia'), _(u'La consulta seleccionada no corresponde al paciente %s')% wizard.name)
            else:
               self.pool.get('patient.consultation').write(cr , uid ,[wizard.consulta_id.id],{'student_id':wizard.student_id.id or None,'teaching_id':wizard.teaching_id.id or None,'specialty':wizard.specialty,'state':'in_process'})
               self.pool.get('odontogramadetails').write(cr , uid , [context.get('active_id')],{'consulta_id':wizard.consulta_id.id, 'state':'assigned'}) 
        return True
    
wizard_diagnostico() 

