# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from ..hacienda_api import HaciendaApi
from odoo.exceptions import ValidationError
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_sv_economic_activity_ids = fields.Many2many("l10n_sv.economic.activity")
    l10n_sv_mh_auth_user = fields.Char(related="company_id.l10n_sv_mh_auth_user", readonly=False)
    l10n_sv_mh_auth_pass = fields.Char(related="company_id.l10n_sv_mh_auth_pass", readonly=False)
    l10n_sv_signer_route = fields.Char(related="company_id.l10n_sv_signer_route", readonly=False)
    l10n_sv_signer_private_pass = fields.Char(related="company_id.l10n_sv_mh_private_pass", readonly=False)
    l10n_sv_dte_mh_test_env = fields.Boolean(related='company_id.l10n_sv_dte_mh_test_env', readonly=False)

    def l10n_sv_dte_action_verify(self):
        self.ensure_one()
        hacienda_api = HaciendaApi(company_id=self.company_id)
        try:
            kernel = hacienda_api._get_auth1()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'info',
                    'sticky': False,
                    'message': "%s" % kernel,
                }
            }

        except requests.exceptions.MissingSchema:
            raise ValidationError(_("Wrong external service URL"))

        except requests.exceptions.ConnectionError:
            raise ValidationError(_("Check you connection"))
