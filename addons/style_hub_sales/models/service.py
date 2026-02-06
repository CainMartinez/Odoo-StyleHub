# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ServiceSalesIntegration(models.Model):
    """
    Extends stylehub.service to integrate with product.template.
    Each service automatically creates and maintains a linked product.
    """
    _inherit = 'stylehub.service'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Related Product',
        readonly=True,
        ondelete='restrict',
        help='Product automatically created for this service'
    )
    
    product_variant_id = fields.Many2one(
        'product.product',
        string='Product Variant',
        related='product_tmpl_id.product_variant_id',
        readonly=True,
        help='Product variant for sale orders'
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to automatically generate a product.template for each service.
        """
        services = super().create(vals_list)
        
        for service in services:
            if not service.product_tmpl_id:
                # Create product template
                product_vals = {
                    'name': service.name,
                    'type': 'service',  # Tipo servicio, no bien material
                    'list_price': service.base_price,
                    'description_sale': service.description or '',
                    'categ_id': self.env.ref('product.product_category_all').id,
                    'invoice_policy': 'order',  # Facturar cantidades pedidas
                    'active': service.active,
                    'sale_ok': True,
                    'purchase_ok': False,
                    'uom_id': self.env.ref('uom.product_uom_unit').id,
                    'uom_po_id': self.env.ref('uom.product_uom_unit').id,
                }
                
                product = self.env['product.template'].create(product_vals)
                service.product_tmpl_id = product.id
        
        return services

    def write(self, vals):
        """
        Override write to sync changes to the linked product.
        """
        result = super().write(vals)
        
        # Sync changes to product
        for service in self:
            if service.product_tmpl_id:
                product_vals = {}
                
                if 'name' in vals:
                    product_vals['name'] = vals['name']
                if 'base_price' in vals:
                    product_vals['list_price'] = vals['base_price']
                if 'description' in vals:
                    product_vals['description_sale'] = vals['description'] or ''
                if 'active' in vals:
                    product_vals['active'] = vals['active']
                
                if product_vals:
                    service.product_tmpl_id.write(product_vals)
        
        return result

    def unlink(self):
        """
        Override unlink to handle product deletion.
        We keep the product but deactivate it to preserve sales history.
        """
        for service in self:
            if service.product_tmpl_id:
                # Deactivate product instead of deleting
                service.product_tmpl_id.write({'active': False})
        
        return super().unlink()

    def action_view_product(self):
        """
        Smart button action to view the related product.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Product',
            'res_model': 'product.template',
            'res_id': self.product_tmpl_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
