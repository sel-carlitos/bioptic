from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    l10n_sv_billing_indicator = fields.Selection(
        [
            ('not_applicable', 'Not Applicable'),
            ('taxable', 'Taxable'),
            ('taxable13', 'Taxable 13'),
            ('tips', 'Tips'),
        ],
        string='Billing Indicator',
    )
