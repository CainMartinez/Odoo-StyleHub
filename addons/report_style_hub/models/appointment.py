# -*- coding: utf-8 -*-

from odoo import models


class StylehubAppointment(models.Model):
    _inherit = 'stylehub.appointment'
    
    # No se necesitan métodos adicionales - el wizard maneja la generación del reporte
