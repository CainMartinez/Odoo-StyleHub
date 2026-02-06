# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DailyAppointmentsWizard(models.TransientModel):
    _name = 'report.daily.appointments.wizard'
    _description = 'Asistente de Informe de Citas Diarias'

    report_date = fields.Date(
        string='Fecha del Informe',
        required=True,
        default=fields.Date.context_today
    )

    def action_print_report(self):
        """
        Generar el informe de citas diarias para la fecha seleccionada.
        """
        all_appointments = self.env['stylehub.appointment'].search([], order='start_datetime asc')
        
        appointments = all_appointments.filtered(
            lambda apt: apt.start_datetime and apt.start_datetime.date() == self.report_date
        )
        
        if not appointments:
            raise models.UserError(_('No se encontraron citas para la fecha %s') % self.report_date)
        
        # Retornar acción de reporte pasando los IDs en data
        return {
            'type': 'ir.actions.report',
            'report_name': 'report_style_hub.report_daily_appointments_document',
            'report_type': 'qweb-pdf',
            'data': {
                'report_date': self.report_date.strftime('%Y-%m-%d'),
                'appointment_ids': appointments.ids,
            },
            'context': {
                'report_filename': f'Citas-{self.report_date.day:02d}-{self.report_date.month:02d}-{self.report_date.year}'
            }
        }
