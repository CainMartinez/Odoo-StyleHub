# -*- coding: utf-8 -*-

from odoo import models, fields


class Stylist(models.Model):
    _name = 'stylehub.stylist'
    _description = 'Estilista de Peluquería'
    _order = 'name'

    name = fields.Char(
        string='Nombre del Estilista',
        required=True,
        help='Nombre del estilista/empleado'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Desmarcar si el estilista ya no trabaja en el salón'
    )
    
    email = fields.Char(
        string='Correo Electrónico',
        help='Correo de contacto del estilista'
    )
    
    phone = fields.Char(
        string='Teléfono',
        help='Número de teléfono de contacto'
    )
    
    appointment_count = fields.Integer(
        string='Total de Citas',
        compute='_compute_appointment_count',
        store=False,
        help='Número total de citas asignadas a este estilista'
    )

    def _compute_appointment_count(self):
        """Contar citas para cada estilista"""
        for record in self:
            record.appointment_count = self.env['stylehub.appointment'].search_count([
                ('stylist_id', '=', record.id)
            ])
