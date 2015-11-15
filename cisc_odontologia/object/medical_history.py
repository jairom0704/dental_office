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
import datetime
import dateutil

class medicalhistories(osv.Model):
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'cedula', 'number'], context)
        res = []
        for record in reads:
            name = record['name']
            cedula = record['cedula']
            number = record['number']
            if cedula:
                name = cedula + '/' + name
            if record['number']:
                name = '%s [%s]' % (record['number'], name)
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
                ids = self.search(cr, uid, [('cedula', operator, name)] + args, limit=limit, context=context)
                if not ids:
                    name = name.split(' / ')[-1]
                    ids = self.search(cr, uid, [('number', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    
    
    def verifica_cedula(self,ced):
        try:
            valores = [ int(ced[x]) * (2 - x % 2) for x in range(9) ]
            suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
            veri = 10 - (suma - (10*(suma/10)))
            if int(ced[9]) == int(str(veri)[-1:]):
                return True
            else:
                return False
        except:
            return False
        
    def verifica_ruc_spub(self,ruc):
        try: 
            if (int(ruc[0]+ruc[1]))<23:
                prueba1=True
            else:
                prueba1=False
            
            if (int(ruc[2])==6):
                prueba2=True
            else:
                prueba2=False    
        
            val0=int(ruc[0])*3
            val1=int(ruc[1])*2
            val2=int(ruc[2])*7
            val3=int(ruc[3])*6
            val4=int(ruc[4])*5
            val5=int(ruc[5])*4
            val6=int(ruc[6])*3
            val7=int(ruc[7])*2
         
            tot=val0+val1+val2+val3+val4+val5+val6+val7
            veri=tot-((tot/11))*11
         
            if(veri==0):
                if((int(ruc[8]))== 0):
                    prueba3=True
                else:
                    prueba3=False
            else:
                if((int(ruc[8]))==(11-veri)):
                    prueba3=True
                else:
                    prueba3=False
        
            if((int(ruc[9]))+(int(ruc[10]))+(int(ruc[11]))+(int(ruc[12]))>0):
                prueba4=True
            else:
                prueba4=False
        
            if(prueba1 and prueba2 and prueba3 and prueba4):
                 return True
            else: 
                return False
        except:
            return False


    def verifica_ruc_pnat(self,ruc):
        try:
            if (int(ruc[0]+ruc[1]))<23:
                prueba1=True
            else:
                prueba1=False
            
            if (int(ruc[2])<6):
                prueba2=True
            else:
                prueba2=False    
        
            valores = [ int(ruc[x]) * (2 - x % 2) for x in range(9) ]
            suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
            veri = 10 - (suma - (10*(suma/10)))
            if int(ruc[9]) == int(str(veri)[-1:]):
                prueba3= True
            else:
                prueba3= False
                
            if((int(ruc[10]))+(int(ruc[11]))+(int(ruc[12]))>0):
                prueba4=True
            else:
                prueba4=False
        
            if(prueba1 and prueba2 and prueba3 and prueba4):
                return True
            else: 
                return False
        except:
            return False
        
    def verifica_id_cons_final(self,id):
        b=True
        try:
            for n in id:
                if int(n) != 9:
                    b=False
            return b
        except:
            return False
        
    def verifica_ruc_spri(self,ruc):
        try:
            if (int(ruc[0]+ruc[1]))<24:
                 prueba1=True
            else:
                 prueba1=False
            
            if (int(ruc[2])==9):
                 prueba2=True
            else:
                 prueba2=False    
        
            val0=int(ruc[0])*4
            val1=int(ruc[1])*3
            val2=int(ruc[2])*2
            val3=int(ruc[3])*7
            val4=int(ruc[4])*6
            val5=int(ruc[5])*5
            val6=int(ruc[6])*4
            val7=int(ruc[7])*3
            val8=int(ruc[8])*2
         
            tot=val0+val1+val2+val3+val4+val5+val6+val7+val8
            veri=tot-((tot/11))*11
         
            if(veri==0):
                if((int(ruc[9]))== 0):
                    prueba3=True
                else:
                    prueba3=False
            else:
                if((int(ruc[9]))==(11-veri)):
                    prueba3=True
                else:
                    prueba3=False
        
            if((int(ruc[10]))+(int(ruc[11]))+(int(ruc[12]))>0):
                prueba4=True
            else:
                prueba4=False
        
            if(prueba1 and prueba2 and prueba3 and prueba4):
                return True
            else: 
                return False
        except:
            return False
        
    _name = 'medicalhistories'
    
    _columns={
    'name':fields.char('Nombres', size=255, required=True, readonly=False),
    'cedula':fields.char('Cédula/RUC', size=14, required=True, readonly=False),
    'type_ref':fields.char('Tipo de Identificación', size=64),
    'number':fields.char('N° Historia Clinica', size=64, required=True, readonly=False), 
    'sex':fields.selection([
                              ('male','MASCULINO'),
                               ('female','FEMENINO'),   
                               ],'Sexo',required=True, readonly=False ),
    'age': fields.integer('Edad/años', readonly=True),
    'note': fields.text('Notas adicionales'),
    'date_registration': fields.datetime('Fecha de registro', readonly=True),
    'consultation_ids': fields.one2many('patient.consultation', 'medical_history_id', 'Consultas odontologicas', readonly=True),
    'fecha_nacimiento': fields.date('Fecha de nacimiento', required=True), 
    'alergia_antibiotico': fields.boolean('1. Alergia Antibiotico'),
    'alergia_anestesia': fields.boolean('2. Alergia Anestesia'),
    'hemorragias': fields.boolean('3. Hemorragias'),
    'sida': fields.boolean('4. VIH/SIDA' ),
    'tuberculosis': fields.boolean('5. Tuberculosis'),
    'asma': fields.boolean('6. Asma'),
    'diabetes': fields.boolean('7. Diabetes'),
    'hipertension': fields.boolean('8. Hipertensión'),
    'cardiaca': fields.boolean('9. Enf. Cardiaca'),
    'otros': fields.boolean('10. Otros'),
    'note1': fields.char('informacion adicional'),
          }
    
    _sql_constraints = [('cedula_uniq','unique(cedula)', _(u'El valor de CEDULA / RUC debe ser único, este valor ya existe'))]
    
    _order = 'number desc'
    _rec_name='number'
    
    _defaults = {
        'date_registration': fields.datetime.now,
        'number': lambda obj, cr, uid, context: '/',
           }
    
    
    def edad(self,fecha_nacimiento):
        ahora = datetime.datetime.utcnow()
        fecha_nacimiento= datetime.datetime.strptime(fecha_nacimiento,"%Y-%m-%d")
        edad = dateutil.relativedelta.relativedelta(ahora, fecha_nacimiento)
        edad = edad.years
        return edad

    def check_ced(self, ced_ruc):
        if ced_ruc:
            type_identification = ''
            valid = False
            for i in ced_ruc:
                try:
                    int(i)
                except:
                    return {
                    'type_ref' : type_identification,
                    'valid': valid
                    }
            if(len(ced_ruc)==13):
                #Se verifica que el cliente es una compañia privada
                if(int(ced_ruc[2])==9):
                    if self.verifica_ruc_spri(ced_ruc):
                        valid = True
                        type_identification='ruc'
                    elif self.verifica_id_cons_final(ced_ruc):
                        valid = True
                        type_identification='consumidor'
                #Se verifica que sea una empresa estatal
                elif(int(ced_ruc[2])==6) and self.verifica_ruc_spub(ced_ruc):
                    valid = True
                    type_identification='ruc'
                #Se verifica que el ruc sea de una persona natural
                elif(int(ced_ruc[2])<6) and self.verifica_ruc_pnat(ced_ruc):
                    valid = True
                    type_identification='ruc'
            #Se verifica el número de cedula
            elif(len(ced_ruc)==10) and self.verifica_cedula(ced_ruc):
                valid = True
                type_identification='cedula'
            return {
                    'type_ref' : type_identification,
                    'valid': valid
                    }
        else:
            return True
        
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        verification_data = self.check_ced(vals.get('cedula', ''))
        if vals.get('cedula', False) and verification_data.get('valid'):
            vals['type_ref'] = verification_data.get('type_ref', None)
        elif vals.get('ref', False) and not verification_data.get('valid'):
            raise osv.except_osv(_(u'Verificación Cédula/RUC'), _(u'La Cédula/RUC %s no es válido, por favor verifique!!!') % vals.get('cedula'))
        if vals.get('number', '/') == '/':
            vals['number'] = self.pool.get('ir.sequence').get(cr, uid, 'medical.history') or '/'
        if vals.get('fecha_nacimiento'):
            vals['age']= self.edad(vals.get('fecha_nacimiento'))
        return super(medicalhistories, self).create(cr, uid, vals, context=None)
    
    
    def write(self, cr, uid, ids, values, context=None):
        if not context: context = {}
        if ids:
            if values.get('fecha_nacimiento'):
                values['age'] = self.edad(values.get('fecha_nacimiento'))
            verification_data = self.check_ced(values.get('cedula', ''))
            if values.get('cedula', False) and verification_data.get('valid'):
                values['type_ref'] = verification_data.get('type_ref', None)
            elif values.get('cedula', False) and not verification_data.get('valid'):
                raise osv.except_osv(_(u'Verificación Cédula/RUC'), _(u'La Cédula/RUC %s no es válido, por favor verifique!!!') % values.get('cedula'))
        res = super(medicalhistories, self).write(cr, uid, ids, values, context)
        return res
    
     
medicalhistories()