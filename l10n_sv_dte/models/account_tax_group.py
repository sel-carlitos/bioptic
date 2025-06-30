# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountTaxGroup(models.Model):

    _inherit = 'account.tax.group'

    l10n_sv_billing_indicator = fields.Selection(
        [
            ('not_applicable', 'Not Applicable'),
            ('taxable', 'Taxable'),
            ('exempt', 'Exempt'),
            ('tips', 'Tips'),
        ],
        string='Billing Indicator',
    )
