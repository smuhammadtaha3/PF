from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    # _inherit = 'sale.order.line'

    custom_discount = fields.Float(string='Discount (%)', default=0.0, help="Discount percentage for the product.")