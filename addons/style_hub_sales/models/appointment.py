# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError


class AppointmentSalesIntegration(models.Model):
    """
    Extends stylehub.appointment to integrate with sale.order.
    When an appointment is marked as 'Done', automatically creates a sale order and invoice.
    """
    _inherit = 'stylehub.appointment'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        readonly=True,
        copy=False,
        help='Sale order generated when appointment is completed'
    )
    
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        copy=False,
        help='Invoice generated from the sale order'
    )
    
    sale_order_state = fields.Selection(
        related='sale_order_id.state',
        string='SO Status',
        readonly=True
    )

    def action_mark_done(self):
        """
        Override action_mark_done to create sale order and invoice when completing appointment.
        """
        result = super().action_mark_done()
        
        for appointment in self:
            if appointment.state == 'done' and not appointment.sale_order_id:
                # Create sale order
                sale_order = appointment._create_sale_order()
                appointment.sale_order_id = sale_order.id
                
                # Create and post invoice
                if sale_order:
                    invoice = appointment._create_invoice(sale_order)
                    if invoice:
                        appointment.invoice_id = invoice.id
        
        return result

    def _create_sale_order(self):
        """
        Create a sale order for the appointment with all services.
        """
        self.ensure_one()
        
        if not self.line_ids:
            raise UserError('Cannot create sale order: No services in appointment.')
        
        # Check if services have linked products
        services_without_product = self.line_ids.filtered(lambda l: not l.service_id.product_variant_id)
        if services_without_product:
            raise UserError(
                'Cannot create sale order: The following services do not have linked products:\n'
                + '\n'.join(services_without_product.mapped('service_id.name'))
            )
        
        # Create sale order
        sale_vals = {
            'partner_id': self.customer_id.id,
            'date_order': self.start_datetime,
            'origin': f'Appointment: {self.display_name}',
            'note': self.notes or '',
        }
        
        sale_order = self.env['sale.order'].create(sale_vals)
        
        # Create sale order lines
        for line in self.line_ids:
            line_vals = {
                'order_id': sale_order.id,
                'product_id': line.service_id.product_variant_id.id,
                'product_uom_qty': 1,
                'price_unit': line.price,
                'name': line.service_id.name,
            }
            self.env['sale.order.line'].create(line_vals)
        
        # Confirm the sale order
        sale_order.action_confirm()
        
        return sale_order

    def _create_invoice(self, sale_order):
        """
        Create and post invoice from sale order.
        """
        self.ensure_one()
        
        if not sale_order:
            return False
        
        # Create invoice
        invoices = sale_order._create_invoices()
        
        if invoices:
            invoice = invoices[0]
            # Post the invoice
            invoice.action_post()
            return invoice
        
        return False

    def action_view_sale_order(self):
        """
        Smart button to view related sale order.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_invoice(self):
        """
        Smart button to view related invoice.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
