# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class L10nSvEconomicActivity(models.Model):
    _name = 'l10n_sv.economic.activity'
    _description = 'Economic Activity'

    name = fields.Char('Activity', required=True, help='Economic Activity Name')
    code = fields.Char('Code', required=True, help='Economic Activity Code')
    sequence = fields.Integer()
    active = fields.Boolean(default=True)

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """ search in name, code and category"""
        args = args or []
        # search in name and code
        domain = args + ['|', ('name', operator, name), ('code', operator, name)]
        activities = self.search_fetch(
            domain, ['display_name'], limit=limit,
        )
        return [(activity.id, activity.display_name) for activity in activities]
