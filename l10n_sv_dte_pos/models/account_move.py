# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'pos.load.mixin']

    @api.model
    def _load_pos_data_domain(self, data):
        result = super()._load_pos_data_domain(data)
        if self.env.company.country_id.code == 'SV':
            return False
        return result

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        if self.env.company.country_id.code == 'SV':
            return ['l10n_sv_voucher_type_id', 'l10n_sv_document_number', 'l10n_sv_generation_code']
        return result

    def _l10n_sv_prepare_document_additional_values(self):
        # EXTENDS 'l10n_sv_dte'
        res = super()._l10n_sv_prepare_document_additional_values()
        if self.pos_order_ids:
            res['order_id'] = self.pos_order_ids[0].id

        return res
