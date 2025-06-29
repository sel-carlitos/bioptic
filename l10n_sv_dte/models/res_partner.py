from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_sv_commercial_name = fields.Char("Commercial Name")
    l10n_sv_identification_id = fields.Many2one("l10n_sv.identification.type", string="Identification Type")
    l10n_sv_identification_code = fields.Char(related="l10n_sv_identification_id.code")
    dui = fields.Char(string="DUI")
    nit = fields.Char(string="NIT")

    # === Economic Activity fields === #

    l10n_sv_activity_id = fields.Many2one(
        comodel_name="l10n_sv.economic.activity",
        string="Default Economic Activity",
        context={
            'active_test': False
        }
    )
