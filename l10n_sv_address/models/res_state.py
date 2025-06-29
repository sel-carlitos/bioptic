# -*- coding: utf-8 -*-
from odoo import models, fields, api


class State(models.Model):
    _inherit = 'res.country.state'

    dte_code = fields.Char(string="DTE code", size=2)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """ search in name, code and category"""
        args = args or []
        # search in name and code
        domain = args + ['|', ('name', operator, name), ('dte_code', operator, name)]
        activities = self.search_fetch(
            domain, ['display_name'], limit=limit,
        )
        return [(activity.id, activity.display_name) for activity in activities]
