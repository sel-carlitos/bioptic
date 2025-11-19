from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    type_operation_line = fields.Selection(
        selection=[
            ("no_sujeto", "No Sujeto"),
            ("exento", "Exento"),
            ("gravado", "Gravado"),
            ("iva_retenido", "IVA Retenido"),
            ("otros", "Otros"),
        ],
        default="gravado",
        help="Tipo de operación para líneas de impuestos en documentos fiscales en El Salvador.",
    )
