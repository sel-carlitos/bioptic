# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DTEDocument(models.Model):
	_inherit = "l10n_sv.dte.document"

	order_id = fields.Many2one('pos.order', string="Order POS", readonly=True)
