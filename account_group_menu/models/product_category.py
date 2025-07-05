from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category with Archive/Unarchive'

    active = fields.Boolean(
        string='Active',
        default=True,
        help="Set to false to archive the product category."
    )
