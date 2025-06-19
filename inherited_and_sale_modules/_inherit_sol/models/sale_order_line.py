from odoo import models, fields, api, exceptions

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_discount = fields.Float(string='Custom Discount (%)', default=0.0)
    custom_discount_amount = fields.Float(string='Custom Discount Amount', compute='_compute_custom_discount_amount', store=True)

    @api.depends('price_unit', 'product_uom_qty', 'custom_discount')
    def _compute_custom_discount_amount(self):
        for line in self:
            line.custom_discount_amount = (line.price_unit * line.product_uom_qty) * (line.custom_discount / 100)