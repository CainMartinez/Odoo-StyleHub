# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Service(models.Model):
    _name = 'stylehub.service'
    _description = 'Hair Salon Service'
    _order = 'name'

    name = fields.Char(
        string='Service Name',
        required=True,
        help='Name of the hair salon service (e.g., Men\'s Haircut, Full Dye, Balayage Highlights)'
    )
    
    duration = fields.Float(
        string='Duration (hours)',
        required=True,
        default=0.5,
        help='Duration of the service in hours (e.g., 0.5 for 30 minutes, 2.5 for 2.5 hours)'
    )
    
    base_price = fields.Float(
        string='Base Price',
        required=True,
        default=0.0,
        help='Standard price for this service. Can be modified per appointment if needed.'
    )
    
    description = fields.Text(
        string='Description',
        help='Additional details about the service'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Uncheck to hide this service from the catalog'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for pricing'
    )

    @api.constrains('duration')
    def _check_duration(self):
        """Ensure duration is positive"""
        for record in self:
            if record.duration <= 0:
                raise ValidationError('Duration must be greater than 0.')

    @api.constrains('base_price')
    def _check_base_price(self):
        """Ensure base price is not negative"""
        for record in self:
            if record.base_price < 0:
                raise ValidationError('Base price cannot be negative.')
