# -*- coding: utf-8 -*-
from odoo import api, models, fields


class Municipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipality'
    _order = 'dte_code'

    name = fields.Char('Name', required=True)
    dte_code = fields.Char('Code', help='El código del municipio', size=2, required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=', country_id)]")

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, dte_code)', '¡El código del municipio debe ser único por provincia!')
    ]

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
