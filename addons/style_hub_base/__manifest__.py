# -*- coding: utf-8 -*-
{
    'name': 'StyleHub',
    'version': '18.0.1.0.0',
    'summary': 'Sistema de gestión para salones de peluquería StyleHub',
    'author': 'Caín Martínez',
    'website': 'https://cain-dev.es',
    'license': 'LGPL-3',
    'category': 'Services/Appointments',
    'depends': ['base', 'contacts', 'website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/service_views.xml',
        'views/appointment_views.xml',
        'views/stylist_views.xml',
        'views/partner_views.xml',
        'views/menu_views.xml',
        'data/demo_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}