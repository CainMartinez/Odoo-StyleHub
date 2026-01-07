# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    appointment_count = fields.Integer(
        string='Total Appointments',
        compute='_compute_appointment_stats',
        store=False,
        help='Total number of appointments for this customer'
    )
    
    completed_appointment_count = fields.Integer(
        string='Completed Appointments',
        compute='_compute_appointment_stats',
        store=False,
        help='Number of completed appointments'
    )
    
    frequent_client = fields.Boolean(
        string='Frequent Client',
        compute='_compute_frequent_client',
        store=True,
        help='Automatically marked as VIP if customer has more than 5 completed appointments'
    )

    def _compute_appointment_stats(self):
        """Calculate appointment statistics for each customer"""
        for record in self:
            appointments = self.env['stylehub.appointment'].search([
                ('customer_id', '=', record.id)
            ])
            record.appointment_count = len(appointments)
            record.completed_appointment_count = len(
                appointments.filtered(lambda a: a.state == 'done')
            )

    @api.depends('completed_appointment_count')
    def _compute_frequent_client(self):
        """
        CRITICAL VIP LOGIC: Automatically mark as frequent client if more than 5 completed appointments.
        This ensures our best customers get special treatment!
        """
        for record in self:
            # Recalculate completed appointments
            completed_count = self.env['stylehub.appointment'].search_count([
                ('customer_id', '=', record.id),
                ('state', '=', 'done')
            ])
            record.frequent_client = completed_count > 5
