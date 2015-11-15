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
from openerp import SUPERUSER_ID

class res_users(osv.Model):
    
    _inherit = 'res.users'
    
    
    _columns={
                'student': fields.boolean('estudiante'),
                'teaching': fields.boolean('docente'),
                'is_normal': fields.boolean('normal'),
                'code': fields.integer('Codigo estudiantil'),
                'cedula': fields.char('Cédula', readonly=False),
                'groups_id': fields.many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', 'Groups'),
                'company_id': fields.many2one('res.company', 'Company', required=True,
            help='The company this user is currently working for.', context={'user_preference': True}),
              'company_ids':fields.many2many('res.company','res_company_users_rel','user_id','cid','Companies'),
              }
    
    def _get_company(self,cr, uid, context=None, uid2=False):
        if not uid2:
            uid2 = uid
        user = self.pool.get('res.users').read(cr, uid, uid2, ['company_id'], context)
        company_id = user.get('company_id', False)
        return company_id and company_id[0] or False

    def _get_companies(self, cr, uid, context=None):
        c = self._get_company(cr, uid, context)
        if c:
            return [c]
        return False

    def _get_menu(self,cr, uid, context=None):
        dataobj = self.pool.get('ir.model.data')
        try:
            model, res_id = dataobj.get_object_reference(cr, uid, 'base', 'action_menu_admin')
            if model != 'ir.actions.act_window':
                return False
            return res_id
        except ValueError:
            return False

    def _get_group(self,cr, uid, context=None):
        dataobj = self.pool.get('ir.model.data')
        result = []
        try:
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_user')
            result.append(group_id)
            dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', 'group_partner_manager')
            result.append(group_id)
            if context.get('student'):
                dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'cisc_odontologia', 'login_students')
                result.append(group_id)
            elif context.get('teaching'):
                dummy,group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'cisc_odontologia', 'login_teaching')
                result.append(group_id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result
    
    def _get_default_image(self, cr, uid, context=None):
        return self.pool['res.partner']._get_default_image(cr, uid, False, colorize=True, context=context)
    
    _defaults = {
        'password': '',
        'active': True,
        'customer': False,
        'company_id': _get_company,
        'company_ids': _get_companies,
        'groups_id': _get_group,
        'image': _get_default_image,
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        if not context:
            context={}
        values = super(res_users, self).default_get(cr, uid, fields_list, context)
        if context.get('student'):
            values['student']= True
        elif context.get('teaching'):
            values['teaching']= True
        elif context.get('is_normal'):
            values['is_normal']= True
        return values 
    
    def create(self, cr, uid, vals, context=None):
        if context is None: context = {}
        #if context.get('student'):
        verification_data = self.pool.get('medicalhistories').check_ced(vals.get('cedula', ''))
        if vals.get('cedula', False) and not verification_data.get('valid'):
            raise osv.except_osv(_(u'Verificación Cédula/RUC'), _(u'La Cédula %s no es válido, por favor verifique!!!') % vals.get('cedula')) 
        #if context.get('student') or context.get('is_normal') or context.get('teaching'):
        #    vals['password'] ='12345678'
        return super(res_users, self).create(cr, uid, vals, context=None)
    
    
    def write(self, cr, uid, ids, values, context=None):
        if not context: context = {}
        #if ids and context.get('student'):
        verification_data = self.pool.get('medicalhistories').check_ced(values.get('cedula', ''))
        if values.get('cedula', False) and not verification_data.get('valid'):
            raise osv.except_osv(_(u'Verificación Cédula/RUC'), _(u'La Cédula %s no es válido, por favor verifique!!!') % values.get('cedula'))
        #if ids and (context.get('student') or context.get('teaching')):
        #    values['password'] = '12345678'
        res = super(res_users, self).write(cr, uid, ids, values, context)
        return res
    
    
    def action_reset_password(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        #res_partner = self.pool.get('res.partner')
        #partner_ids = [user.partner_id.id for user in self.browse(cr, uid, ids, context)]
        #res_partner.signup_prepare(cr, uid, partner_ids, signup_type="reset", expiration=now(days=+1), context=context)

        if not context:
            context = {}

        # send email to users with their signup url
        template = False
        if context.get('create_user'):
            try:
                # get_object() raises ValueError if record does not exist
                self.write(cr, uid, ids, {'password':'12345678'})
                template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup', 'set_password_email')
            except ValueError:
                pass
        if not bool(template):
            self.write(cr, uid, ids, {'password':'12345678'})
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup', 'reset_password_email')
        assert template._name == 'email.template'

        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise osv.except_osv(_("Cannot send email: user has no email address."), user.name)
            self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, force_send=True, raise_exception=True, context=context)
    
        
    
res_users()