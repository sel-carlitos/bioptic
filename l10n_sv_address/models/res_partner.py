# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipality', domain="[('state_id', '=', state_id)]")

    @api.model
    def default_get(self, fields_list):
        """
        Overrides the default_get method to set country_id to the company's
        fiscal_country_id when creating a new partner.
        """
        res = super().default_get(fields_list)

        company = self.env.company 

        if company and company.account_fiscal_country_id:
            res['country_id'] = company.account_fiscal_country_id.id

        return res
