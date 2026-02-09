# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
import json
import pytz


class StyleHubWebsite(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def home(self, **kwargs):
        """Home page"""
        return request.render('style_hub_website.home_page_template')

    @http.route('/appointment/book', type='http', auth='public', website=True)
    def appointment_booking(self, **kwargs):
        """Main booking page"""
        services = request.env['stylehub.service'].sudo().search([('active', '=', True)])
        
        return request.render('style_hub_website.appointment_booking_template', {
            'services': services,
        })
    
    @http.route('/nuestros-servicios', type='http', auth='public', website=True)
    def our_services(self, **kwargs):
        """Services catalog page"""
        services = request.env['stylehub.service'].sudo().search([('active', '=', True)])
        
        return request.render('style_hub_website.our_services_template', {
            'services': services,
        })
    
    @http.route('/nuestro-equipo', type='http', auth='public', website=True)
    def our_team(self, **kwargs):
        """Our team page"""
        # Get CEO (admin user)
        ceo = request.env.ref('base.user_admin')
        
        # Get all active stylists
        stylists = request.env['stylehub.stylist'].sudo().search([])
        
        return request.render('style_hub_website.our_team_template', {
            'ceo': ceo,
            'stylists': stylists,
        })

    @http.route('/appointment/get_available_slots', type='json', auth='public', website=True)
    def get_available_slots(self, date, service_ids):
        """Get available time slots for a specific date and services"""
        try:
            # Obtener timezone del usuario o usar Europe/Madrid por defecto
            tz_name = request.env.context.get('tz') or request.env.user.tz or 'Europe/Madrid'
            user_tz = pytz.timezone(tz_name)
            
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            now = datetime.now(user_tz)
            is_today = appointment_date == now.date()
            
            # Calculate total duration
            services = request.env['stylehub.service'].sudo().browse(service_ids)
            total_duration = sum(services.mapped('duration'))
            
            # Business hours (9:00 - 20:00)
            start_hour = 9
            end_hour = 20
            slot_interval = 0.5  # 30 minutes
            
            available_slots = []
            current_time = start_hour
            
            while current_time + total_duration <= end_hour:
                # Crear datetime en timezone local
                slot_datetime_naive = datetime.combine(appointment_date, datetime.min.time())
                slot_datetime_naive = slot_datetime_naive.replace(hour=int(current_time), 
                                                                  minute=int((current_time % 1) * 60))
                slot_datetime_local = user_tz.localize(slot_datetime_naive)
                
                # Si es hoy, solo mostrar horarios futuros (al menos 30 min de adelanto)
                if is_today and slot_datetime_local <= now + timedelta(minutes=30):
                    current_time += slot_interval
                    continue
                
                # Convertir a UTC para verificar disponibilidad
                slot_datetime_utc = slot_datetime_local.astimezone(pytz.UTC).replace(tzinfo=None)
                
                # Check if any stylist is available
                stylist = request.env['stylehub.appointment'].sudo()._find_available_stylist(
                    slot_datetime_utc, total_duration
                )
                
                if stylist:
                    hours = int(current_time)
                    minutes = int((current_time % 1) * 60)
                    available_slots.append({
                        'time': f"{hours:02d}:{minutes:02d}",
                        'datetime': slot_datetime_utc.strftime('%Y-%m-%d %H:%M:%S')  # Enviar en UTC
                    })
                
                current_time += slot_interval
            
            return {'slots': available_slots}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/appointment/create', type='json', auth='user', website=True)
    def create_appointment(self, **kwargs):
        """Create appointment from website"""
        try:
            # La fecha viene en UTC desde el frontend, ya está correcta
            start_datetime = datetime.strptime(kwargs.get('start_datetime'), '%Y-%m-%d %H:%M:%S')
            service_ids = kwargs.get('service_ids', [])
            notes = kwargs.get('notes', '')
            
            # Get current user as customer
            customer = request.env.user.partner_id
            
            # Calculate total duration
            services = request.env['stylehub.service'].sudo().browse(service_ids)
            total_duration = sum(services.mapped('duration'))
            
            # Find available stylist
            stylist = request.env['stylehub.appointment'].sudo()._find_available_stylist(
                start_datetime, total_duration
            )
            
            if not stylist:
                return {
                    'error': 'No hay estilistas disponibles para esta fecha y hora. Por favor, seleccione otro horario.'
                }
            
            # Create appointment
            appointment = request.env['stylehub.appointment'].sudo().create({
                'customer_id': customer.id,
                'stylist_id': stylist.id,
                'start_datetime': start_datetime,
                'notes': notes,
                'state': 'draft',
            })
            
            # Create service lines
            for service in services:
                request.env['stylehub.appointment.line'].sudo().create({
                    'appointment_id': appointment.id,
                    'service_id': service.id,
                    'price': service.base_price,
                })
            
            # Auto-confirm
            appointment.action_confirm()
            
            return {
                'success': True,
                'appointment_id': appointment.id,
                'stylist_name': stylist.name,
                'message': f'Cita confirmada con {stylist.name} el {start_datetime.strftime("%d/%m/%Y a las %H:%M")}'
            }
            
        except Exception as e:
            return {'error': str(e)}

    @http.route('/my/appointments', type='http', auth='user', website=True)
    def my_appointments(self, **kwargs):
        """Customer portal - My appointments"""
        customer = request.env.user.partner_id
        appointments = request.env['stylehub.appointment'].search([
            ('customer_id', '=', customer.id)
        ], order='start_datetime desc')
        
        return request.render('style_hub_website.portal_my_appointments', {
            'appointments': appointments,
        })

    @http.route('/my/appointments/<int:appointment_id>', type='http', auth='user', website=True)
    def appointment_detail(self, appointment_id, **kwargs):
        """Appointment detail page"""
        appointment = request.env['stylehub.appointment'].browse(appointment_id)
        
        # Check if user owns this appointment
        if appointment.customer_id != request.env.user.partner_id:
            return request.redirect('/my/appointments')
        
        return request.render('style_hub_website.portal_appointment_detail', {
            'appointment': appointment,
        })

    @http.route('/my/appointments/<int:appointment_id>/cancel', type='http', auth='user', website=True)
    def cancel_appointment(self, appointment_id, **kwargs):
        """Cancel appointment from portal"""
        appointment = request.env['stylehub.appointment'].browse(appointment_id)
        
        # Check ownership and state
        if appointment.customer_id == request.env.user.partner_id and appointment.state in ['draft', 'confirmed']:
            appointment.sudo().action_cancel()
        
        return request.redirect('/my/appointments')
