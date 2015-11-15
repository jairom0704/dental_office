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


class codeodontologicos(osv.Model):
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'codigo'], context)
        res = []
        for record in reads:
            name = record['name']
            codigo = record['codigo']
            name = codigo + '[' + name + ']'
            res.append((record['id'], name))
        return res
    
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            if not ids:
                name = name.split(' / ')[-1]
                ids = self.search(cr, uid, [('codigo', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    _name = 'codeodontologicos'
    
    _columns={
                'name': fields.char('Nombre', required=True),
                'activo': fields.boolean('Activo'),
                'aplicacara': fields.boolean('Aplica Cara'),
                'aplicadiente': fields.boolean('Aplica Diente'),
                'codigo': fields.char('Codigo', required=True),
                'descripcion': fields.char('Descripcion', required=False),
              }
    
    _rec_name='name'
    
    _defaults={
               'activo':True,
               'aplicacara':True,
               'aplicadiente':True
               }
    
codeodontologicos()

class odontogramadetails(osv.Model):
    _name =  'odontogramadetails'
    _description = 'odontograma detalle'
    
    def _default_responsable(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return user and user.id or False
    
    _columns={
                'consulta_id': fields.many2one('patient.consultation', 'Consulta', readonly=True),
                'secuencial': fields.char('N° Diag. Odontograma', readonly=True),
                'paciente_id':fields.many2one('medicalhistories', 'Historial Clinico', readonly=True),
                'responsable_id':fields.many2one('res.users', 'Responsable', readonly=True),
                'diagnostico_final': fields.text('Resultado Odontograma', readonly=True),
                'diagnostico_final_realizado': fields.text('Realizado', readonly=True),
                'diagnostico': fields.text('diagnostico'),
                'diagnostico_realizado': fields.text('diagnostico realizado', readonly=True),
                'created_at': fields.datetime('Fecha', readonly=True),
                'updated_at': fields.datetime('Fecha de actualización odontograma', readonly=True),
                'observacion': fields.text('OBSERVACIONES', states={'assigned': [('readonly', True)]}),
                'name': fields.related('paciente_id', 'name', type='char', relation='medicalhistories', string='Paciente', readonly=True, store=True),
                'cedula': fields.related('paciente_id', 'cedula', type='char', relation='medicalhistories', string='Cédula/RUC', readonly=True, store=True),
                'state': fields.selection([
                        ('draft', 'Borrador'),
                        ('assigned', 'Asignado al area'),
                        ], 'Estado', readonly=True),
                # indicadores de salud
                'p16': fields.boolean('16', states={'assigned': [('readonly', True)]}),
                'p11': fields.boolean('11', states={'assigned': [('readonly', True)]}),
                'p26': fields.boolean('26' ,states={'assigned': [('readonly', True)]}),
                'p36': fields.boolean('36' ,states={'assigned': [('readonly', True)]}),
                'p31': fields.boolean('31' ,states={'assigned': [('readonly', True)]}),
                'p46': fields.boolean('46' ,states={'assigned': [('readonly', True)]}),
                'p17': fields.boolean('17' ,states={'assigned': [('readonly', True)]}),
                'p21': fields.boolean('21' ,states={'assigned': [('readonly', True)]}),
                'p27': fields.boolean('27' ,states={'assigned': [('readonly', True)]}),
                'p37': fields.boolean('37' ,states={'assigned': [('readonly', True)]}),
                'p41': fields.boolean('41' ,states={'assigned': [('readonly', True)]}),
                'p47': fields.boolean('47' ,states={'assigned': [('readonly', True)]}),
                'p55': fields.boolean('55' ,states={'assigned': [('readonly', True)]}),
                'p51': fields.boolean('51' ,states={'assigned': [('readonly', True)]}),
                'p65': fields.boolean('65' ,states={'assigned': [('readonly', True)]}),
                'p75': fields.boolean('75' ,states={'assigned': [('readonly', True)]}),
                'p71': fields.boolean('71' ,states={'assigned': [('readonly', True)]}),
                'p86': fields.boolean('86' ,states={'assigned': [('readonly', True)]}),
                'total1': fields.integer('Total' ,states={'assigned': [('readonly', True)]}),
                'total2': fields.integer('Total' ,states={'assigned': [('readonly', True)]}),
                'total3': fields.integer('Total' ,states={'assigned': [('readonly', True)]}),
                'placa1': fields.integer('placa1' ,states={'assigned': [('readonly', True)]}),
                'placa2': fields.integer('placa2' ,states={'assigned': [('readonly', True)]}),
                'placa3': fields.integer('placa3' ,states={'assigned': [('readonly', True)]}),
                'placa4': fields.integer('placa4' ,states={'assigned': [('readonly', True)]}),
                'placa5': fields.integer('placa5' ,states={'assigned': [('readonly', True)]}),
                'placa6': fields.integer('placa6' ,states={'assigned': [('readonly', True)]}),
                'placat': fields.integer('Total' ,states={'assigned': [('readonly', True)]}),
                'placap': fields.integer('%' ,states={'assigned': [('readonly', True)]}),
                'calculo1': fields.integer('calculo1' ,states={'assigned': [('readonly', True)]}),
                'calculo2': fields.integer('calculo2' ,states={'assigned': [('readonly', True)]}),
                'calculo3': fields.integer('calculo3' ,states={'assigned': [('readonly', True)]}),
                'calculo4': fields.integer('calculo4' ,states={'assigned': [('readonly', True)]}),
                'calculo5': fields.integer('calculo5' ,states={'assigned': [('readonly', True)]}),
                'calculo6': fields.integer('calculo6' ,states={'assigned': [('readonly', True)]}),
                'calculot': fields.integer('Total' ,states={'assigned': [('readonly', True)]}),
                'calculop': fields.integer('%' ,states={'assigned': [('readonly', True)]}),
                'gin1': fields.integer('gin1' ,states={'assigned': [('readonly', True)]}),
                'gin2': fields.integer('gin2' ,states={'assigned': [('readonly', True)]}),
                'gin3': fields.integer('gin3' ,states={'assigned': [('readonly', True)]}),
                'gin4': fields.integer('gin4' ,states={'assigned': [('readonly', True)]}),
                'gin5': fields.integer('gin5' ,states={'assigned': [('readonly', True)]}),
                'gin6': fields.integer('gin6' ,states={'assigned': [('readonly', True)]}),
                'gint': fields.integer('total' ,states={'assigned': [('readonly', True)]}),
                'ginp': fields.integer('%' ,states={'assigned': [('readonly', True)]}),
                
              }
    
    _rec_name='secuencial'
    _order = 'secuencial desc'
    
    _defaults={
              'responsable_id':_default_responsable
              }  
    
    def change_draft(self, cr , uid, ids, context):
        if not context: context = {}
        for odo in self.browse(cr, uid , ids):
            if odo.consulta_id.state=='closed':
                raise osv.except_osv(_(u'Advertencia'), _(u'La consulta %s se encuentra en estado [CERRADA]. Favor proceda primero a cambiar a estado [EN PROCESO] la misma para pueda cambiar a borrador el diagnostico') % odo.consulta_id.number_consult)
            else:
                self.pool('patient.consultation').write(cr , uid , [odo.consulta_id.id], {'state':'open', 'specialty':''})  
                self.write(cr , uid , [odo.id], {'state':'draft','consulta_id':None})
        
    def write(self, cr, uid, ids, values, context=None):
        if not context: context = {}
        if ids:
            values['responsable_id'] = uid
        res = super(odontogramadetails, self).write(cr, uid, ids, values, context)
        return res
    
    def pz1_change(self, cr, uid, ids, p16=False, p11=False ,p26=False,
            p36=False, p31=False, p46=False, context=None):
        context = context or {}
        result={}
        totales1=0
        if p16:
            totales1 +=1
        if p11:
            totales1 +=1
        if p26:
            totales1 +=1
        if p36:
            totales1 +=1
        if p31:
            totales1 +=1
        if p46:
            totales1 +=1
        result['total1'] = totales1
        return {'value': result}
    
    def pz2_change(self, cr, uid, ids, p17=False, p21=False ,p27=False,
            p37=False, p41=False, p47=False, context=None):
        context = context or {}
        result={}
        totales2=0
        if p17:
            totales2 +=1
        if p21:
            totales2 +=1
        if p27:
            totales2 +=1
        if p37:
            totales2 +=1
        if p41:
            totales2 +=1
        if p47:
            totales2 +=1
        result['total2'] = totales2
        return {'value': result}
    
    def pz3_change(self, cr, uid, ids, p55=False, p51=False ,p65=False,
            p75=False, p71=False, p86=False, context=None):
        context = context or {}
        result={}
        totales3=0
        if p55:
            totales3 +=1
        if p51:
            totales3 +=1
        if p65:
            totales3 +=1
        if p75:
            totales3 +=1
        if p71:
            totales3 +=1
        if p86:
            totales3 +=1
        result['total3'] = totales3
        return {'value': result}
    
    def placa_change(self, cr, uid, ids, placa1=0, placa2=0 ,placa3=0,
            placa4=0, placa5=0, placa6=0, context=None):
        context = context or {}
        total=0
        warning = {}
        result={}
        if placa1:
            if placa1 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa1 }
                result['placa1'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if placa2:
            if placa2 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa2 }
                result['placa2'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if placa3:
            if placa3 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa3 }
                result['placa3'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if placa4:
            if placa4 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa4 }
                result['placa4'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if placa5:
            if placa5 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa5 }
                result['placa5'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if placa6:
            if placa6 >=4:
                warning = {'title': _('Placa 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % placa6 }
                result['placa6'] = 0
                result['placap'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        result['placap'] = float(total*100) / 6
        return {'value': result}
    
    def calculo_change(self, cr, uid, ids, calculo1=0, calculo2=0 ,calculo3=0,
            calculo4=0, calculo5=0, calculo6=0, context=None):
        context = context or {}
        result={}
        warning = {}
        total=0
        if calculo1:
            if calculo1 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo1 }
                result['calculo1'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        if calculo2:
            if calculo2 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo2 }
                result['calculo2'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        if calculo3:
            if calculo3 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo3 }
                result['calculo3'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        if calculo4:
            if calculo4 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo4 }
                result['calculo4'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        if calculo5:
            if calculo5 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo5 }
                result['calculo5'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        if calculo6:
            if calculo6 >=4:
                warning = {'title': _('Calculo 0-1-2-3 !'), 'message' : 'valor incorrecto %s' % calculo6 }
                result['calculo6'] = 0
                result['calculop'] = 0
                return {'value': result, 'warning': warning}
            total+=1
        result['calculop'] = float(total*100) / 6
        return {'value': result}
    
    def gingivitis_change(self, cr, uid, ids, gin1=0, gin2=0 ,gin3=0,
            gin4=0, gin5=0, gin6=0, context=None):
        context = context or {}
        result={}
        warning = {}
        total=0
        if gin1:
            if gin1 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin1 }
                result['gin1'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if gin2:
            if gin2 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin2 }
                result['gin2'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if gin3:
            if gin3 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin3 }
                result['gin3'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if gin4:
            if gin4 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin4 }
                result['gin4'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if gin5:
            if gin5 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin5 }
                result['gin5'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        if gin6:
            if gin6 >= 2:
                warning = {'title': _('Gingivitis 0-1 !'), 'message' : 'valor incorrecto %s' % gin6 }
                result['gin6'] = 0
                result['ginp'] = 0
                return {'value': result, 'warning': warning}
            total +=1
        result['ginp'] = float(total*100) / 6
        return {'value': result}
    
odontogramadetails()
