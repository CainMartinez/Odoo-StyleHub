# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class Appointment(models.Model):
    _name = 'stylehub.appointment'
    _description = 'Cita de Peluquería'
    _order = 'start_datetime desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Nombre Mostrado',
        compute='_compute_display_name',
        store=True
    )
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        help='Cliente para esta cita'
    )
    
    stylist_id = fields.Many2one(
        'stylehub.stylist',
        string='Estilista',
        required=True,
        domain=[('active', '=', True)],
        help='Estilista asignado a esta cita'
    )
    
    start_datetime = fields.Datetime(
        string='Fecha y Hora de Inicio',
        required=True,
        help='Cuándo comienza la cita'
    )
    
    end_datetime = fields.Datetime(
        string='Fecha y Hora de Finalización',
        compute='_compute_end_datetime',
        store=True,
        readonly=True,
        help='Calculada automáticamente en base a la duración de los servicios'
    )
    
    total_duration = fields.Float(
        string='Duración Total (horas)',
        compute='_compute_total_duration',
        store=True,
        help='Suma de todas las duraciones de servicios'
    )
    
    line_ids = fields.One2many(
        'stylehub.appointment.line',
        'appointment_id',
        string='Servicios',
        help='Servicios incluidos en esta cita'
    )
    
    total_price = fields.Float(
        string='Precio Total',
        compute='_compute_total_price',
        store=True,
        help='Monto total a pagar'
    )
    
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('confirmed', 'Confirmada'),
            ('done', 'Realizada'),
            ('cancelled', 'Cancelada')
        ],
        string='Estado',
        default='draft',
        required=True,
        tracking=True,
        help='Estado actual de la cita'
    )
    
    color = fields.Integer(
        string='Color',
        help='Índice de color para la vista kanban'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        help='Moneda para los precios'
    )
    
    notes = fields.Text(
        string='Notas',
        help='Notas adicionales o solicitudes especiales'
    )

    @api.depends('customer_id', 'start_datetime')
    def _compute_display_name(self):
        """Generar un nombre legible para la cita"""
        for record in self:
            if record.customer_id and record.start_datetime:
                date_str = fields.Datetime.to_string(record.start_datetime)
                record.display_name = f"{record.customer_id.name} - {date_str}"
            else:
                record.display_name = 'Nueva Cita'

    @api.depends('line_ids.duration')
    def _compute_total_duration(self):
        """Calcular la duración total de todas las líneas de servicio"""
        for record in self:
            record.total_duration = sum(record.line_ids.mapped('duration'))

    @api.depends('start_datetime', 'total_duration')
    def _compute_end_datetime(self):
        """
        CRÍTICO: Calcular automáticamente la hora de finalización sumando la duración total
        del servicio a la hora de inicio. ¡Este es el punto principal de dolor para el cliente!
        """
        for record in self:
            if record.start_datetime and record.total_duration:
                # Convertir horas a timedelta y añadir a la hora de inicio
                duration_delta = timedelta(hours=record.total_duration)
                record.end_datetime = record.start_datetime + duration_delta
            else:
                record.end_datetime = record.start_datetime

    @api.depends('line_ids.price')
    def _compute_total_price(self):
        """Calcular el precio total de todas las líneas de servicio"""
        for record in self:
            record.total_price = sum(record.line_ids.mapped('price'))

    @api.constrains('start_datetime', 'end_datetime', 'stylist_id', 'state')
    def _check_stylist_availability(self):
        """
        CRÍTICO: Prevenir citas superpuestas para el mismo estilista.
        ¡Esta validación asegura que nunca reservemos dos veces a un estilista!
        """
        for record in self:
            # Solo verificar para citas no canceladas
            if record.state == 'cancelled':
                continue
                
            if not record.start_datetime or not record.end_datetime:
                continue
            
            # Buscar citas superpuestas con el mismo estilista
            overlapping = self.search([
                ('id', '!=', record.id),
                ('stylist_id', '=', record.stylist_id.id),
                ('state', '!=', 'cancelled'),
                '|',
                '&',
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
                '&',
                ('start_datetime', '>=', record.start_datetime),
                ('start_datetime', '<', record.end_datetime),
            ])
            
            if overlapping:
                raise ValidationError(
                    f"⛔ ¡CONFLICTO DE HORARIO!\n\n"
                    f"El estilista '{record.stylist_id.name}' ya tiene una reserva en este horario.\n\n"
                    f"Tu cita: {record.start_datetime} - {record.end_datetime}\n"
                    f"Cita(s) en conflicto:\n" +
                    "\n".join([f"  • {apt.start_datetime} - {apt.end_datetime} ({apt.customer_id.name})" 
                              for apt in overlapping[:3]])
                )

    def action_confirm(self):
        """Confirmar la cita"""
        for record in self:
            if not record.line_ids:
                raise UserError('¡No se puede confirmar una cita sin servicios!')
            record.state = 'confirmed'
        return True

    def action_mark_done(self):
        """Marcar cita como completada y actualizar el estado VIP del cliente"""
        for record in self:
            record.state = 'done'
            # Disparar recálculo del estado frequent_client del cliente
            record.customer_id._compute_frequent_client()
        return True

    def action_cancel(self):
        """Cancelar la cita"""
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_draft(self):
        """Restablecer cita a borrador"""
        self.write({'state': 'draft'})
        return True

    @api.model
    def _find_available_stylist(self, start_datetime, duration_hours):
        """
        Find an available stylist for a given time slot.
        Used by the web booking system for automatic assignment.
        
        :param start_datetime: datetime object for appointment start
        :param duration_hours: float representing total service duration
        :return: stylehub.stylist record or False
        """
        end_datetime = start_datetime + timedelta(hours=duration_hours)
        
        # Get all active stylists
        all_stylists = self.env['stylehub.stylist'].search([('active', '=', True)])
        
        for stylist in all_stylists:
            # Check if this stylist has any overlapping appointments
            overlapping = self.search([
                ('stylist_id', '=', stylist.id),
                ('state', 'in', ['draft', 'confirmed']),
                '|',
                '&',
                ('start_datetime', '<', end_datetime),
                ('end_datetime', '>', start_datetime),
                '&',
                ('start_datetime', '>=', start_datetime),
                ('start_datetime', '<', end_datetime),
            ], limit=1)
            
            # If no overlapping appointments, this stylist is available
            if not overlapping:
                return stylist
        
        # No available stylist found
        return False
