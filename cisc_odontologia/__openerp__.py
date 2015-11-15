# -*- encoding: utf-8 -*-
########################################################################
#
# @authors: Jairo Troncoso
# Copyright (C) 2015  CISC
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

{
    "name": "Facultad Piloto de Odontologia",
    "version": "1.0",
    "depends": ["base",
                "web",
                "disable_openerp_online",
                ],
                
    "author": "Jairo Troncoso jairom0704@gmail.com",
    "website" : "https://twitter.com/jairomt25",
    "category": "Partners",
    "complexity": "normal",
    "description": """
    This module provide :
    
    """,
    "init_xml": [],
    #'data': [,],
    'update_xml': [
                "data/data.xml",
                'static/src/xml/cisc_odontologia.xml',
                'views/document.xml',
                "views/medical_history.xml",
                "views/res_users_view.xml",
                "views/code_odontologico_view.xml",
                "wizard/wizard_diagnostico_view.xml",
                "views/patient_consultation.xml",
                "views/tratamiento_view.xml",
                "security/groups.xml",
                "security/ir.model.access.csv",     
                "security/security.xml"         
                   ],
    
    'demo_xml': [],
    
    
    'test': [],
    'installable': True,
    'auto_install': False,
}