# -*- coding: utf-8 -*-
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('sv', 'account.tax')
    def _get_sv_edi_account_tax(self):
        return self._parse_csv('sv', 'account.tax', module='l10n_sv_dte')

    @template('sv', 'account.tax.group')
    def _get_sv_edi_account_tax_group(self):
        return self._parse_csv('sv', 'account.tax.group', module='l10n_sv_dte')
