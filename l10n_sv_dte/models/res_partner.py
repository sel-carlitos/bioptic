from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_sv_commercial_name = fields.Char("Commercial Name")
    l10n_sv_identification_id = fields.Many2one("l10n_sv.identification.type", string="Identification Type")
    l10n_sv_available_identification_ids = fields.Many2many('l10n_sv.identification.type',
                                                            compute='_compute_l10n_sv_available_identification_ids')
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

    @api.depends('company_type', 'company_id')
    def _compute_l10n_sv_available_identification_ids(self):
        self.l10n_sv_available_identification_ids = False
        for partner in self.filtered(lambda x: 'SV' in x.fiscal_country_codes):
            domain = []

            if partner.company_type == 'person':
                domain.append(('code', 'in', ['04', '13', '37']))
            else:
                domain.append(('code', 'in', ['36', '37']))

            identification_type = self.env["l10n_sv.identification.type"].search(domain)
            partner.l10n_sv_available_identification_ids = identification_type
