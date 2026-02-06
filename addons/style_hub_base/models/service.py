# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Service(models.Model):
    _name = 'stylehub.service'
    _description = 'Servicio de Peluquería'
    _order = 'name'

    name = fields.Char(
        string='Nombre del Servicio',
        required=True,
        help='Nombre del servicio de peluquería (ej: Corte de Hombre, Tinte Completo, Mechas Balayage)'
    )
    
    duration = fields.Float(
        string='Duración (horas)',
        required=True,
        default=0.5,
        help='Duración del servicio en horas (ej: 0.5 para 30 minutos, 2.5 para 2 horas y media)'
    )
    
    base_price = fields.Float(
        string='Precio Base',
        required=True,
        default=0.0,
        help='Precio estándar para este servicio. Puede modificarse por cita si es necesario.'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Detalles adicionales sobre el servicio'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Desmarcar para ocultar este servicio del catálogo'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        help='Moneda para los precios'
    )
    
    duration_display = fields.Char(
        string='Duración Mostrada',
        compute='_compute_duration_display',
        store=False
    )
    
    price_display = fields.Char(
        string='Precio Mostrado',
        compute='_compute_price_display',
        store=False
    )
    
    emoji = fields.Char(
        string='Emoji',
        compute='_compute_emoji',
        store=False
    )
    
    icon_class = fields.Char(
        string='Clase de Icono',
        compute='_compute_icon_class',
        store=False
    )

    @api.depends('duration')
    def _compute_duration_display(self):
        """Format duration as human-readable text"""
        for record in self:
            hours = int(record.duration)
            minutes = int((record.duration - hours) * 60)
            total_minutes = int(record.duration * 60)
            
            if record.duration == 1.0:
                record.duration_display = '60 minutos'
            elif hours == 0:
                record.duration_display = f'{total_minutes} minutos'
            elif minutes == 0:
                hour_text = 'hora' if hours == 1 else 'horas'
                record.duration_display = f'{hours} {hour_text}'
            else:
                hour_text = 'hora' if hours == 1 else 'horas'
                record.duration_display = f'{hours} {hour_text} y {minutes} minutos'
    
    @api.depends('base_price')
    def _compute_price_display(self):
        """Format price without decimals if it's a whole number"""
        for record in self:
            if record.base_price == int(record.base_price):
                record.price_display = f'{int(record.base_price)} €'
            else:
                record.price_display = f'{record.base_price:.2f} €'
    
    @api.depends('name')
    def _compute_emoji(self):
        """Assign emoji based on service name keywords"""
        for record in self:
            name_lower = record.name.lower()
            
            # Emojis por tipo de servicio
            if any(word in name_lower for word in ['corte', 'haircut', 'trim']):
                record.emoji = '✂️'
            elif any(word in name_lower for word in ['tinte', 'color', 'dye', 'teñir']):
                record.emoji = '🎨'
            elif any(word in name_lower for word in ['mechas', 'balayage', 'highlights']):
                record.emoji = '✨'
            elif any(word in name_lower for word in ['tratamiento', 'treatment', 'keratina', 'hidratante']):
                record.emoji = '💆'
            elif any(word in name_lower for word in ['peinado', 'styling', 'recogido', 'blow']):
                record.emoji = '💇'
            elif any(word in name_lower for word in ['barba', 'beard', 'afeitado']):
                record.emoji = '🧔'
            elif any(word in name_lower for word in ['extensiones', 'extensions']):
                record.emoji = '💁'
            elif any(word in name_lower for word in ['lavado', 'wash', 'shampoo']):
                record.emoji = '🚿'
            elif any(word in name_lower for word in ['infantil', 'niño', 'kid', 'child']):
                record.emoji = '👶'
            elif any(word in name_lower for word in ['retoque', 'raíz', 'root', 'touch']):
                record.emoji = '🔄'
            else:
                record.emoji = '💈'  # Default barber pole emoji
    
    @api.depends('name')
    def _compute_icon_class(self):
        """Assign Font Awesome icon based on service name keywords"""
        for record in self:
            name_lower = record.name.lower()
            
            # Font Awesome icons por tipo de servicio
            if any(word in name_lower for word in ['corte', 'haircut', 'trim']):
                record.icon_class = 'fa fa-scissors'
            elif any(word in name_lower for word in ['tinte', 'color', 'dye', 'teñir']):
                record.icon_class = 'fa fa-paint-brush'
            elif any(word in name_lower for word in ['mechas', 'balayage', 'highlights']):
                record.icon_class = 'fa fa-star'
            elif any(word in name_lower for word in ['tratamiento', 'treatment', 'keratina', 'hidratante']):
                record.icon_class = 'fa fa-heart'
            elif any(word in name_lower for word in ['peinado', 'styling', 'recogido', 'blow']):
                record.icon_class = 'fa fa-female'
            elif any(word in name_lower for word in ['barba', 'beard', 'afeitado']):
                record.icon_class = 'fa fa-user'
            elif any(word in name_lower for word in ['extensiones', 'extensions']):
                record.icon_class = 'fa fa-magic'
            elif any(word in name_lower for word in ['lavado', 'wash', 'shampoo']):
                record.icon_class = 'fa fa-tint'
            elif any(word in name_lower for word in ['infantil', 'niño', 'kid', 'child']):
                record.icon_class = 'fa fa-child'
            elif any(word in name_lower for word in ['retoque', 'raíz', 'root', 'touch']):
                record.icon_class = 'fa fa-refresh'
            else:
                record.icon_class = 'fa fa-cut'  # Default scissors icon

    @api.constrains('duration')
    def _check_duration(self):
        """Asegurar que la duración sea positiva"""
        for record in self:
            if record.duration <= 0:
                raise ValidationError('La duración debe ser mayor que 0.')

    @api.constrains('base_price')
    def _check_base_price(self):
        """Asegurar que el precio base no sea negativo"""
        for record in self:
            if record.base_price < 0:
                raise ValidationError('El precio base no puede ser negativo.')
