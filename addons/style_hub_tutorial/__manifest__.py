# -*- coding: utf-8 -*-
{
    'name': 'StyleHub Tutorial',
    'version': '18.0.1.0.0',
    'summary': 'Tutorial interactivo para empleados de StyleHub',
    'description': """
        Wizard tutorial paso a paso que explica cómo utilizar el sistema StyleHub.
        
        Características:
        - 6 pasos educativos
        - Barra de progreso visual
        - Navegación fluida
        - Diseño moderno y responsive
        - Accesible desde el menú principal
    """,
    'author': 'Caín Martínez',
    'website': 'https://cain-dev.es',
    'license': 'LGPL-3',
    'category': 'Services/Tutorials',
    'depends': ['style_hub_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tutorial_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'style_hub_tutorial/static/src/css/tutorial.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
