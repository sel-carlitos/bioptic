from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    def _get_l10n_sv_billing_indicator_selection(self):
        from odoo import _
        return [
            ('not_applicable', _('Not Applicable')),
            ('taxable', _('Taxable')),
            ('taxable10', _('Taxable 10')),
            ('taxable13', _('Taxable 13')),
        ]

    l10n_sv_billing_indicator = fields.Selection(
        selection=_get_l10n_sv_billing_indicator_selection,
        string='Billing Indicator'
    )
