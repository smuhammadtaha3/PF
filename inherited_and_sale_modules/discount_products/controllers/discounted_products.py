from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class DiscountedProductsController(WebsiteSale):
    @http.route('/shop/discounted_products', type='http', auth="public", website=True)
    def shop_discounted(self, **kwargs):
        """
        Render the discounted products on a custom page.
        """
        products = http.request.env['product.template'].search([('custom_discount', '>', 0)])
        
        return http.request.render('discount_products.products_discounted', {
            'products': products,
        })