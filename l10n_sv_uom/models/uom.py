# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class UOM(models.Model):
    _inherit = "uom.uom"

    dte_code = fields.Char(string="DTE Code", size=2, help="Hacienda Code")
