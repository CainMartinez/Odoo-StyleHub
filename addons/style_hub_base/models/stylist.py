# -*- coding: utf-8 -*-

from odoo import models, fields


class Stylist(models.Model):
    _name = 'stylehub.stylist'
    _description = 'Hair Salon Stylist'
    _order = 'name'

    name = fields.Char(
        string='Stylist Name',
        required=True,
        help='Name of the stylist/employee'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Uncheck if the stylist is no longer working at the salon'
    )
    
    email = fields.Char(
        string='Email',
        help='Contact email for the stylist'
    )
    
    phone = fields.Char(
        string='Phone',
        help='Contact phone number'
    )
    
    appointment_count = fields.Integer(
        string='Total Appointments',
        compute='_compute_appointment_count',
        store=False,
        help='Total number of appointments assigned to this stylist'
    )

    def _compute_appointment_count(self):
        """Count appointments for each stylist"""
        for record in self:
            record.appointment_count = self.env['stylehub.appointment'].search_count([
                ('stylist_id', '=', record.id)
            ])
