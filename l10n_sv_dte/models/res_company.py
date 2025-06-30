# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_sv_establishment_type = fields.Selection(
        [
            ("01", "Sucursal / Agencia"),
            ("02", "Casa matriz"),
            ("04", "Bodega"),
            ("07", "Predio y/o patio"),
            ("20", "Otro")
        ],
        string="Establishment Type",
    )
    l10n_sv_economic_activity_ids = fields.Many2many('l10n_sv.economic.activity', string="Economic Activities")
    l10n_sv_country_code = fields.Char(related="account_fiscal_country_id.code", search='_search_country_code',
                                       string="Country Id", readonly=True, store=True)
    l10n_sv_signer_route = fields.Char()
    l10n_sv_mh_auth_user = fields.Char(string="Usuario de API")
    l10n_sv_mh_auth_pass = fields.Char(string="Password de API")
    l10n_sv_mh_private_pass = fields.Char(string="Password Private")
    l10n_sv_dte_mh_test_env = fields.Boolean(
        string='PAC test environment',
        help='Enable the usage of test credentials',
        default=False)

    @api.model
    def _search_country_code(self, operator, operand):
        return [('country_id.code', operator, operand)]

    def action_view_economic_activity(self):
        self.ensure_one()
        action = self.env.ref("l10n_sv_dte.action_res_caecr").read()[0]
        if self.l10n_sv_economic_activity_ids:
            action["views"] = [
                (self.env.ref("l10n_sv_dte.view_res_caecr_tree").id, "list"),
                (self.env.ref("l10n_sv_dte.view_res_caecr_form").id, "form"),
            ]
            action["domain"] = [('id', 'in', self.l10n_sv_economic_activity_ids.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action
