# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    appointment_count = fields.Integer(
        string='Total de Citas',
        compute='_compute_appointment_stats',
        store=False,
        help='Número total de citas para este cliente'
    )
    
    completed_appointment_count = fields.Integer(
        string='Citas Completadas',
        compute='_compute_appointment_stats',
        store=False,
        help='Número de citas completadas'
    )
    
    frequent_client = fields.Boolean(
        string='Cliente Frecuente',
        compute='_compute_frequent_client',
        store=True,
        help='Marcado automáticamente como VIP si el cliente tiene más de 5 citas completadas'
    )

    def _compute_appointment_stats(self):
        """Calcular estadísticas de citas para cada cliente"""
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
        LÓGICA VIP CRÍTICA: Marcar automáticamente como cliente frecuente si tiene más de 5 citas completadas.
        ¡Esto asegura que nuestros mejores clientes reciban trato especial!
        """
        for record in self:
            # Recalcular citas completadas
            completed_count = self.env['stylehub.appointment'].search_count([
                ('customer_id', '=', record.id),
                ('state', '=', 'done')
            ])
            record.frequent_client = completed_count > 5
