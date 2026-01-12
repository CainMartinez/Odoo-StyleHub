# -*- coding: utf-8 -*-
{
    'name': 'StyleHub',
    'version': '18.0.1.0.0',
    'summary': 'Hair Salon Management System',
    'description': """
        Complete hair salon management system for StyleHub.
        Features:
        - Service catalog with pricing and duration
        - Stylist management
        - Appointment scheduling with automatic end time calculation
        - Overlap prevention for stylist availability
        - VIP client detection
        - Calendar and Kanban views
    """,
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