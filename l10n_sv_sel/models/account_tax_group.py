from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    def _get_l10n_sv_tax_code(self):
        """Return the list of IVA taxes rates and codes required by Hacienda."""
        return [
            ('20', 'Impuesto al Valor Agregado 13%'),
            ('C3', 'Impuesto al Valor Agregado (exportaciones) 0%'),
            ('59', 'Turismo: por alojamiento (5%)'),
            ('71', 'Turismo: salida del país por vía aérea $7.00'),
            ('D1', 'FOVIAL ($0.20 Ctvs. por galón)'),
            ('C8', 'COTRANS ($0.10 Ctvs. por galón)'),
            ('D5', 'Otras tasas casos especiales'),
            ('D4', 'Otros impuestos casos especiales'),
        ]

    l10n_sv_code = fields.Selection(
        string='Código de impuesto',
        selection='_get_l10n_sv_tax_code',
        help='CAT- 15: Código de tributos',
    )
