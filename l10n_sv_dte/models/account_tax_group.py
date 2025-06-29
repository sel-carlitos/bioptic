# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountTaxGroup(models.Model):

    _inherit = 'account.tax.group'

    l10n_sv_billing_indicator = fields.Selection([
        ('not_applicable', _('Not Applicable')),
        ('taxable', _('Taxable')),
        ('exempt', _('Exempt')),
        ('tips', _('Tips')),
    ], string='Billing Indicator')
