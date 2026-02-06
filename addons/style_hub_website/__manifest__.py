# -*- coding: utf-8 -*-
{
    'name': 'StyleHub Website',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Módulo Web StyleHub para Odoo',
    'author': 'StyleHub',
    'depends': [
        'style_hub_base',
        'website',
        'portal',
    ],
    'data': [
        'views/home.xml',
        'views/services.xml',
        'views/team.xml',
        'views/booking.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'style_hub_website/static/src/css/home.css',
            'style_hub_website/static/src/css/booking.css',
            'style_hub_website/static/src/css/services.css',
            'style_hub_website/static/src/css/team.css',
            'style_hub_website/static/src/js/booking.js',
            'style_hub_website/static/src/js/services.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
