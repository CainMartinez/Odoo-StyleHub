# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class Appointment(models.Model):
    _name = 'stylehub.appointment'
    _description = 'Hair Salon Appointment'
    _order = 'start_datetime desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        help='Client for this appointment'
    )
    
    stylist_id = fields.Many2one(
        'stylehub.stylist',
        string='Stylist',
        required=True,
        domain=[('active', '=', True)],
        help='Stylist assigned to this appointment'
    )
    
    start_datetime = fields.Datetime(
        string='Start Date & Time',
        required=True,
        help='When the appointment begins'
    )
    
    end_datetime = fields.Datetime(
        string='End Date & Time',
        compute='_compute_end_datetime',
        store=True,
        readonly=True,
        help='Automatically calculated based on service durations'
    )
    
    total_duration = fields.Float(
        string='Total Duration (hours)',
        compute='_compute_total_duration',
        store=True,
        help='Sum of all service durations'
    )
    
    line_ids = fields.One2many(
        'stylehub.appointment.line',
        'appointment_id',
        string='Services',
        help='Services included in this appointment'
    )
    
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
        help='Total amount to be paid'
    )
    
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        help='Current status of the appointment'
    )
    
    color = fields.Integer(
        string='Color',
        help='Color index for kanban view'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for pricing'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes or special requests'
    )

    @api.depends('customer_id', 'start_datetime')
    def _compute_display_name(self):
        """Generate a readable name for the appointment"""
        for record in self:
            if record.customer_id and record.start_datetime:
                date_str = fields.Datetime.to_string(record.start_datetime)
                record.display_name = f"{record.customer_id.name} - {date_str}"
            else:
                record.display_name = 'New Appointment'

    @api.depends('line_ids.duration')
    def _compute_total_duration(self):
        """Calculate total duration from all service lines"""
        for record in self:
            record.total_duration = sum(record.line_ids.mapped('duration'))

    @api.depends('start_datetime', 'total_duration')
    def _compute_end_datetime(self):
        """
        CRITICAL: Automatically calculate end time by adding total service duration
        to start time. This is the main pain point for the client!
        """
        for record in self:
            if record.start_datetime and record.total_duration:
                # Convert hours to timedelta and add to start time
                duration_delta = timedelta(hours=record.total_duration)
                record.end_datetime = record.start_datetime + duration_delta
            else:
                record.end_datetime = record.start_datetime

    @api.depends('line_ids.price')
    def _compute_total_price(self):
        """Calculate total price from all service lines"""
        for record in self:
            record.total_price = sum(record.line_ids.mapped('price'))

    @api.constrains('start_datetime', 'end_datetime', 'stylist_id', 'state')
    def _check_stylist_availability(self):
        """
        CRITICAL: Prevent overlapping appointments for the same stylist.
        This validation ensures we never double-book a stylist!
        """
        for record in self:
            # Only check for non-cancelled appointments
            if record.state == 'cancelled':
                continue
                
            if not record.start_datetime or not record.end_datetime:
                continue
            
            # Search for overlapping appointments with the same stylist
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
                    f"⛔ SCHEDULING CONFLICT!\n\n"
                    f"Stylist '{record.stylist_id.name}' is already booked during this time.\n\n"
                    f"Your appointment: {record.start_datetime} - {record.end_datetime}\n"
                    f"Conflicting appointment(s):\n" +
                    "\n".join([f"  • {apt.start_datetime} - {apt.end_datetime} ({apt.customer_id.name})" 
                              for apt in overlapping[:3]])
                )

    def action_confirm(self):
        """Confirm the appointment"""
        for record in self:
            if not record.line_ids:
                raise UserError('Cannot confirm an appointment without services!')
            record.state = 'confirmed'
        return True

    def action_mark_done(self):
        """Mark appointment as completed and update customer VIP status"""
        for record in self:
            record.state = 'done'
            # Trigger recomputation of customer's frequent_client status
            record.customer_id._compute_frequent_client()
        return True

    def action_cancel(self):
        """Cancel the appointment"""
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_draft(self):
        """Reset appointment to draft"""
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
