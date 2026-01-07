# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentLine(models.Model):
    _name = 'stylehub.appointment.line'
    _description = 'Appointment Service Line'
    _order = 'appointment_id, sequence, id'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of services in the appointment'
    )
    
    appointment_id = fields.Many2one(
        'stylehub.appointment',
        string='Appointment',
        required=True,
        ondelete='cascade',
        help='Related appointment'
    )
    
    service_id = fields.Many2one(
        'stylehub.service',
        string='Service',
        required=True,
        domain=[('active', '=', True)],
        help='Service to be performed'
    )
    
    duration = fields.Float(
        string='Duration (hours)',
        related='service_id.duration',
        store=True,
        readonly=True,
        help='Duration of the service in hours'
    )
    
    price = fields.Float(
        string='Price',
        required=True,
        default=0.0,
        help='Price for this service. Defaults to base price but can be adjusted.'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        related='appointment_id.currency_id',
        store=True,
        help='Currency for pricing'
    )

    @api.onchange('service_id')
    def _onchange_service_id(self):
        """Auto-fill price when service is selected"""
        if self.service_id:
            self.price = self.service_id.base_price

    @api.constrains('price')
    def _check_price(self):
        """Ensure price is not negative"""
        for record in self:
            if record.price < 0:
                raise ValidationError('Price cannot be negative.')
