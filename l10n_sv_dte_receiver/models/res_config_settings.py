# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_sv_create_product_from_xml = fields.Boolean(default=False,
                                                     config_parameter='l10n_sv_dte_receiver.l10n_sv_create_product_from_xml')