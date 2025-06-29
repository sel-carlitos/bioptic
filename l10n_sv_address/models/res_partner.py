# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipality', domain="[('state_id', '=', state_id)]")
