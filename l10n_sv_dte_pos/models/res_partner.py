# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        if self.env.company.country_id.code == 'SV':
            params += ['l10n_sv_identification_id']
        return params
