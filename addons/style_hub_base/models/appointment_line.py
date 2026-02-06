# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentLine(models.Model):
    _name = 'stylehub.appointment.line'
    _description = 'Línea de Servicio de Cita'
    _order = 'appointment_id, sequence, id'

    sequence = fields.Integer(
        string='Secuencia',
        default=10,
        help='Orden de los servicios en la cita'
    )
    
    appointment_id = fields.Many2one(
        'stylehub.appointment',
        string='Cita',
        required=True,
        ondelete='cascade',
        help='Cita relacionada'
    )
    
    service_id = fields.Many2one(
        'stylehub.service',
        string='Servicio',
        required=True,
        domain=[('active', '=', True)],
        help='Servicio a realizar'
    )
    
    duration = fields.Float(
        string='Duración (horas)',
        related='service_id.duration',
        store=True,
        readonly=True,
        help='Duración del servicio en horas'
    )
    
    price = fields.Float(
        string='Precio',
        required=True,
        default=0.0,
        help='Precio para este servicio. Por defecto es el precio base pero puede ajustarse.'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        related='appointment_id.currency_id',
        store=True,
        help='Moneda para los precios'
    )

    @api.onchange('service_id')
    def _onchange_service_id(self):
        """Auto-rellenar precio cuando se selecciona un servicio"""
        if self.service_id:
            self.price = self.service_id.base_price

    @api.constrains('price')
    def _check_price(self):
        """Asegurar que el precio no sea negativo"""
        for record in self:
            if record.price < 0:
                raise ValidationError('El precio no puede ser negativo.')
