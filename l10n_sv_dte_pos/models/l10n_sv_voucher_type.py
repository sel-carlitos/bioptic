# -*- coding: utf-8 -*-
from odoo import models, fields, api


class L10nSvVoucherType(models.Model):
    _name = 'l10n_sv.voucher.type'
    _inherit = ['l10n_sv.voucher.type', 'pos.load.mixin']

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        if self.env.company.country_id.code == 'SV':
            params += ['name']
        return params
