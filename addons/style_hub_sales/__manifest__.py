# -*- coding: utf-8 -*-
{
    'name': 'StyleHub Sales Integration',
    'version': '18.0.1.0.0',
    'summary': 'Integración entre StyleHub y Odoo Ventas/Productos',
    'author': 'Caín Martínez',
    'website': 'https://cain-dev.es',
    'license': 'LGPL-3',
    'category': 'Sales/Sales',
    'depends': [
        'style_hub_base',
        'sale_management',
        'product',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/appointment_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
