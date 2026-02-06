# -*- coding: utf-8 -*-
{
    'name': 'StyleHub Reports',
    'version': '18.0.1.0.0',
    'summary': 'Reporting module for StyleHub appointments and services',
    'author': 'Caín Martínez',
    'website': 'https://cain-dev.es',
    'license': 'LGPL-3',
    'category': 'Services/Reports',
    'depends': ['style_hub_base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/daily_appointments_wizard_views.xml',
        'report/daily_appointments_report.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
