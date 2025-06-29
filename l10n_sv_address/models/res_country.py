# -*- coding: utf-8 -*-
from odoo import api, models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    dte_code = fields.Char('Code', help='Código del pais', size=4)

