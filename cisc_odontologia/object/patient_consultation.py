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


class odontograma_url(osv.osv):
    
    _name='odontograma.url'
    _columns={'color': fields.integer('Color Index'),
               'name': fields.char('Odontograma' ,readonly=True),
              }
    _rec_name = 'name'
odontograma_url()


class patient_consultation(osv.Model):
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'cedula', 'number_consult'], context)
        res = []
        for record in reads:
            name = record['name']
            cedula = record['cedula']
            number = record['number_consult']
            if cedula:
                name = cedula + '/' + name
            if record['number_consult']:
                name = '%s [%s]' % (record['number_consult'], name)
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
            ids = self.search(cr, uid, [('number_consult', operator, name)] + args, limit=limit, context=context)
            if not ids:
                name = name.split(' / ')[-1]
                ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
                if not ids:
                    name = name.split(' / ')[-1]
                    ids = self.search(cr, uid, [('cedula', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    def _nota_acumulada(self, cr, uid, ids, field_name, arg=None, context=None):
        res={}
        if context is None:
            context = {}
        for pati in self.browse(cr, uid, ids, context=context):
            acum=0
            if pati.tratamiento_ids:
                for trata in pati.tratamiento_ids:
                    if trata.nota:
                        acum += trata.nota
                #res[pati.id]=acum
                res[pati.id] = {'nota_acum': acum}
        return res
    
    def _get_tratamiento(self, cr, uid, ids, context=None):
        result = {}
        for trata in self.pool.get('tratamiento').browse(cr, uid, ids, context=context):
            result[trata.consulta_id.id] = True
        return result.keys()
    
    _name = 'patient.consultation'
    
    _columns={
    'color': fields.integer('Color Index'),
    'number_consult':fields.char('N° Consulta', size=64,readonly=True), 
    'name': fields.related('medical_history_id', 'name', type='char', relation='medicalhistories', string='Paciente', readonly=True, store=True),
    'cedula': fields.related('medical_history_id', 'cedula', type='char', relation='medicalhistories', string='Cédula/RUC', readonly=True, store=True),
    'motive': fields.text('Motivo de la consulta',states={'closed': [('readonly', True)]}),
    'problem': fields.char('Causa del problema' ,states={'closed': [('readonly', True)]}),
    'problem_detail': fields.text('Causa del problema' ,states={'closed': [('readonly', True)]}),
    'date_consult': fields.date('Fecha de consulta', states={'closed': [('readonly', True)]}),
    'medical_history_id': fields.many2one('medicalhistories', 'Historia Clinica', required=True),
    'student_id': fields.many2one('res.users', 'Estudiante', required=False, domain=[('student','=',True),('is_normal','=',False)],states={'closed': [('readonly', True)]}),
    'teaching_id': fields.many2one('res.users', 'Docente', required=False, domain=[('teaching','=',True),('is_normal','=',False)],states={'closed': [('readonly', True)]}),
    'state': fields.selection([
            ('open', 'Abierta'),
            ('in_process', 'En proceso'),
            ('closed', 'Cerrada'),
            ], 'Estado', readonly=True),
    #mas información examenes
  'presion': fields.char('PRESIÓN ARTERIAL' ,states={'closed': [('readonly', True)]}),
  'frecuencia': fields.integer('FRECUENCIA CARDIACA/minutos' ,states={'closed': [('readonly', True)]}),
  'temperatura': fields.integer('TEMPERATURA °C'),
  'frecuencia2': fields.integer('FRECUENCIA RESPIRATORIA/minutos' ,states={'closed': [('readonly', True)]}),
  'note2': fields.char('informacion adicional' ,states={'closed': [('readonly', True)]}),
  'labios': fields.boolean('1. Labios' ,states={'closed': [('readonly', True)]}),
  'mejillas': fields.boolean('2. MEJILLAS' ,states={'closed': [('readonly', True)]}),
  'maxilar': fields.boolean('3. MAXILAR SUPERIOR' ,states={'closed': [('readonly', True)]}),
  'maxilar2': fields.boolean('4. MAXILAR INFERIOR' ,states={'closed': [('readonly', True)]}),
  'lengua': fields.boolean('5. LENGUA' ,states={'closed': [('readonly', True)]}),
  'paladar': fields.boolean('6. PALADAR' ,states={'closed': [('readonly', True)]}),
  'piso': fields.boolean('7. PISO' ,states={'closed': [('readonly', True)]}),
  'carrillo': fields.boolean('8. CARRILLOS' ,states={'closed': [('readonly', True)]}),
  'gland': fields.boolean('9. GLANDULAS SALIVALES' ,states={'closed': [('readonly', True)]}),
  'oro': fields.boolean('10. ORO FARINGE' ,states={'closed': [('readonly', True)]}),
  'atm': fields.boolean('11. A.T.M' ,states={'closed': [('readonly', True)]}),
  'ganglios': fields.boolean('12. GANGLIOS' ,states={'closed': [('readonly', True)]}),
  'note3': fields.char('informacion adicional' ,states={'closed': [('readonly', True)]}),
  'diagnostico_ids': fields.one2many('odontogramadetails', 'consulta_id', 'Diágnosticos', readonly=True),
  'specialty':fields.selection([
                  ('clinica','Clinica Integral'),
                  ('operatoriapb','Operatoria PB'),
                  ('cirugiapb','Cirugía PB'),
                  ('odontopediatria','Odontopediatria'),
                  ('ortodoncia','Ortodoncia'),
                   ('operatoriapb','Operatoria PA'),
                  ('cirugiapa','Cirugía PA'),
                   ],    'Especialidad',  select=True,states={'closed': [('readonly', True)]}),
  #Tratamiento
  'planes': fields.text('planes' ,states={'closed': [('readonly', True)]}),
  'tratamiento_ids': fields.one2many('tratamiento', 'consulta_id', 'Tratamientos' , required=True,states={'closed': [('readonly', True)]}),
  'nota_acum' : fields.function(_nota_acumulada, string='Nota acumulada', digits=(16, 2),
                                   store={
                'patient.consultation': (lambda self, cr, uid, ids, c={}: ids, ['tratamiento_ids'], 5),
                'tratamiento': (_get_tratamiento, ['nota'], 5),
            }, multi='sums', help="Nota acumulada de los tratamientos."),
  }
    
    _order = 'number_consult desc'
    _rec_name='number_consult'
    
    _defaults = {
        'date_consult': fields.date.context_today,
        'number_consult': lambda obj, cr, uid, context: '/',
        'state':'open',
        'color': 0
           }

    
    
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        user_obj = self.pool.get('res.users')
        partner_obj = self.pool.get('res.partner')
        if vals.get('number_consult', '/') == '/':
            vals['number_consult'] = self.pool.get('ir.sequence').get(cr, uid, 'patient.consultation') or '/'
            if vals.get('student_id'):
                #try:
                    company = self.pool.get('res.company').read(cr, uid, uid, ['email'])
                    user_student = user_obj.read(cr , uid , vals.get('student_id') ,['partner_id'], context=None)
                    partner_student = partner_obj.read(cr , uid , user_student['partner_id'][0],['name', 'email'] ,context=None)
                    if partner_student['email']:
                        if vals.has_key('specialty'):
                            specialty = vals.get('specialty')
                        else:
                            specialty = 'Sin Especialidad definida'
                        #self._send_notification(cr, uid, [0], partner_student['email'], company['email'], context = {
                        #                'subject':"""Asignación de Consulta""" ,
                        #                'body':"""Estudiante %s, <br/>
                        #                 Le informamos que ha sido asignado para atender la Consulta %s en la Especialidad de %s """ % (partner_student['name'], vals['number_consult'], specialty)
                        #                })
                #except Exception, e:
                #    print str(e)
            if vals.get('teaching_id'):
                try:
                    company = self.pool.get('res.company').read(cr, uid, uid, ['email'])
                    user_teaching = user_obj.read(cr , uid , vals.get('teaching_id') ,['partner_id'], context=None)
                    partner_teaching = partner_obj.read(cr , uid , user_teaching['partner_id'][0],['name', 'email'] ,context=None)
                    if partner_teaching['email']:
                        if vals.has_key('specialty'):
                            specialty = vals.get('specialty')
                        else:
                            specialty = 'Sin Especialidad definida'
                        #self._send_notification(cr, uid, [0], partner_teaching['email'], company['email'], context = {
                        #                'subject':"""Asignación de Consulta""" ,
                        #                'body':"""Docente %s, <br/>
                        #                 Le informamos que ha sido asignado para atender la Consulta %s en la Especialidad de %s """ % (partner_teaching['name'], vals['number_consult'], specialty)
                        #                })
                except Exception, e:
                        print str(e)
        return super(patient_consultation, self).create(cr, uid, vals, context=None)

    def closed(self, cr , uid, ids, context):
        if not context: context = {}
        self.write(cr , uid , ids, {'state':'closed'})
        
    def change_in_process(self, cr , uid, ids, context):
        if not context: context = {}
        consult= self.browse(cr, uid, ids[0])
        if consult.tratamiento_ids:
            for trata in consult.tratamiento_ids:
                if trata.statet =='realizado':
                    raise osv.except_osv(_('Advertencia!'), _('NO PUEDE CAMBIAR A PROCESO LA CONSULTA , DEBIDO A QUE TIENES TRATAMIENTOS YA REALIZADOS!!!'))
        self.write(cr , uid , ids, {'state':'in_process'})
        
    
    def write(self, cr, uid, ids, values, context=None):
        if not context: context = {}
        user_obj = self.pool.get('res.users')
        partner_obj = self.pool.get('res.partner')
        if ids:
            if values.has_key('specialty'):
                specialty = values.get('specialty')
            else:
                specialty = 'Sin Especialidad definida'
            company = self.pool.get('res.company').read(cr, uid, uid, ['email'])
            patient = self.read(cr, uid , ids[0], ['number_consult', 'specialty', 'medical_history_id'], context=None)
            if values.get('student_id'): 
                #try:
                    user_student = user_obj.read(cr , uid , values.get('student_id') ,['partner_id'], context=None)
                    partner_student = partner_obj.read(cr , uid , user_student['partner_id'][0],['name', 'email'] ,context=None)
                    if partner_student['email']:
                        self._send_notification(cr, uid, [0], partner_student['email'], company['email'], context = {
                                    'subject':"""Asignación de Consulta""" ,
                                    'body':"""Estudiante %s, <br/>
                                     Le informamos que ha sido asignado para atender la Consulta %s en la Especialidad de %s  """ % (partner_student['name'], patient['number_consult'], specialty)
                                        })
                #except Exception, e:
                #    print str(e)
            if values.get('teaching_id'):
                #try:
                    user_teaching = user_obj.read(cr , uid , values.get('teaching_id') ,['partner_id'], context=None)
                    partner_teaching = partner_obj.read(cr , uid , user_teaching['partner_id'][0],['name', 'email'] ,context=None)
                    if partner_teaching['email']:
                        self._send_notification(cr, uid, [0], partner_teaching['email'], company['email'], context = {
                                        'subject':"""Asignación de Consulta""" ,
                                        'body':"""Docente %s, <br/>
                                        Le informamos que ha sido asignado para atender la Consulta %s en la Especialidad de %s """ % (partner_teaching['name'], patient['number_consult'], specialty)
                                        })
                #except Exception, e:
                #    print str(e)
                        
        return super(patient_consultation, self).write(cr, uid, ids, values, context)
    

    def _send_notification(self, cr, uid, ids, email_to, email_from,  context = None):     
        if not context: context={}
        email_to = [email_to]

        #email_from = [email_from]
        ir_mail_server = self.pool.get('ir.mail_server')
        msg = ir_mail_server.build_email(
                email_from = u"Facultad piloto de Odontología <%s>" % email_from,
                email_to = email_to,
                subject = context.get('subject'),
                body= context.get('body'),
                subtype = 'html',
                subtype_alternative = 'plain')
        msg['Return-Path'] = msg['From']
        res = ir_mail_server.send_email(cr, uid, msg, mail_server_id=None, context=context)        

                
patient_consultation()

class tratamiento(osv.Model):
    
    _name = 'tratamiento'
    
    _columns={
                'consulta_id': fields.many2one('patient.consultation', 'Consulta', readonly=True),
                'sesion':fields.integer('Sesión', required=True),
                'date': fields.date('Fecha', required=True),
                'nota':fields.float('NOTA', digits=(16, 2), readonly=True),
                'nota_temp':fields.float('NOTA', digits=(16, 2)),
                'studentl_id': fields.related('consulta_id', 'student_id', type='many2one', relation='res.users', string='Estudiante', readonly=True, store=True),
                'teaching_id': fields.related('consulta_id', 'teaching_id', type='many2one', relation='res.users', string='Docente', readonly=True, store=True),
                'diag':fields.char('Diagnostico y complicaciones', size=250, required=True, ),
                'diagnostico_id': fields.many2one('codeodontologicos', 'Procedimientos' , required=True,),
                'prescripcion':fields.char('Prescripciones', size=250, required=True,),
                'motivo':fields.text('Motivo cancelación', size=250),
                'name': fields.related('consulta_id', 'name', type='char', relation='patient.consultation', string='Paciente', readonly=True, store=True),
                'cedula': fields.related('consulta_id', 'cedula', type='char', relation='patient.consultation', string='Cédula/RUC', readonly=True, store=True),
                'statet':fields.selection([
                  ('planificado','Planificado'),
                  ('realizado','Realizado'),
                  ('cancelado','Cancelado'),
                   ],    'Estado',  readonly=True),
              'specialtyl': fields.related('consulta_id','specialty', type='selection', selection=[
                ('clinica','Clinica Integral'),
                  ('operatoriapb','Operatoria PB'),
                  ('cirugiapb','Cirugía PB'),
                  ('odontopediatria','Odontopediatria'),
                  ('ortodoncia','Ortodoncia'),
                   ('operatoriapb','Operatoria PA'),
                  ('cirugiapa','Cirugía PA'),
            ], string='Especialidad', readonly=True, store=True),
              'confirmar':fields.boolean('Confirmar', size=250),
              }  
      
    _defaults={
               'statet':'planificado',
               'confirmar':False
               #'sesion': lambda obj, cr, uid, context: 1,
               }
    
    def realizado(self, cr , uid, ids, context):
        if not context: context = {}
        self.write(cr , uid , ids, {'statet':'realizado'}) 
    
    def cancelado(self, cr , uid, ids, context):
        if not context: context = {}
        trata = self.browse(cr , uid, ids[0])
        if not trata.motivo:
            raise osv.except_osv(_('Advertencia!'), _('DEBE INGRESAR EL MOTIVO DE LA CANCELACIÓN DEL TRATAMIENTO!!!'))
        else:
            self.write(cr , uid , [ids[0]], {'statet':'cancelado'}) 
    
    def cambiarplanificado(self, cr , uid, ids, context):
        if not context: context = {}
        self.write(cr , uid , ids, {'statet':'planificado', 'motivo':''})
        
    def confirmarnota(self, cr , uid, ids, context):
        if not context: context = {}
        trata = self.browse(cr , uid, ids[0])
        if trata.nota_temp:
            if trata.nota_temp < 0 or trata.nota_temp > 10:
                raise osv.except_osv(_('Advertencia!'), _('Valor incorrecto de la nota , el rango es 0 -10 !!!'))
            self.write(cr , uid , [trata.id], {'confirmar':True, 'nota':float(trata.nota_temp)})
        
    #def create(self, cr, uid, vals, context=None):
    #    if context is None:
    #        context = {}
    #    if vals.get('sesion', '**') == '**':
    #        print True
    #    return super(tratamiento, self).create(cr, uid, vals, context=None)
    
tratamiento() 

