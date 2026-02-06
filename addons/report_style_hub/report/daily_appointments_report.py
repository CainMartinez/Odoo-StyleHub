# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import datetime


class DailyAppointmentsReport(models.AbstractModel):
    _name = 'report.report_style_hub.report_daily_appointments_document'
    _description = 'Informe de Citas Diarias'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Sobrescribir para proveer valores personalizados al template del reporte.
        """
        # Obtener IDs desde data si están disponibles, sino usar docids
        appointment_ids = data.get('appointment_ids', []) if data else docids
        
        docs = self.env['stylehub.appointment'].browse(appointment_ids)
        
        # Obtener fecha del reporte desde data o usar la fecha de la primera cita
        if data and data.get('report_date'):
            report_date_value = data.get('report_date')
            # Convertir string a objeto date si es necesario
            if isinstance(report_date_value, str):
                report_date_obj = fields.Date.from_string(report_date_value)
            else:
                report_date_obj = report_date_value
            # Formatear fecha en español
            days_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            months_es = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            day_name = days_es[report_date_obj.weekday()]
            month_name = months_es[report_date_obj.month]
            report_date = f"{day_name}, {report_date_obj.day} de {month_name} de {report_date_obj.year}"
            
            # Nombre del archivo: Citas-dia-mes-año
            file_name = f"Citas-{report_date_obj.day:02d}-{report_date_obj.month:02d}-{report_date_obj.year}"
        elif docs:
            report_date_obj = docs[0].start_datetime.date()
            days_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            months_es = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            day_name = days_es[report_date_obj.weekday()]
            month_name = months_es[report_date_obj.month]
            report_date = f"{day_name}, {report_date_obj.day} de {month_name} de {report_date_obj.year}"
            
            # Nombre del archivo: Citas-dia-mes-año
            file_name = f"Citas-{report_date_obj.day:02d}-{report_date_obj.month:02d}-{report_date_obj.year}"
        else:
            report_date = None
            file_name = "Citas"
        
        result = {
            'doc_ids': appointment_ids,
            'doc_model': 'stylehub.appointment',
            'docs': docs,
            'report_date': report_date,
            'file_name': file_name,
        }
        return result
