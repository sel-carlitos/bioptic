# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PosConfig(models.Model):
    _inherit = "pos.config"

    l10n_sv_terminal_id = fields.Many2one('l10n_sv.terminal', string="Terminal", help="Terminal o Punto de venta.")
    l10n_sv_fiscal_journal = fields.Boolean(
        string='Fiscal POS',
        related='invoice_journal_id.l10n_sv_fiscal_journal',
    )
    default_partner_id = fields.Many2one("res.partner",
                                         string="Default Customer",
                                         help=u"Este cliente se usará por defecto como cliente de consumo"
                                              " para las facturas de consumo o final en el POS")
    only_invoice = fields.Boolean(string="Only Invoice", default=False)

    @api.onchange("only_invoice")
    def onchange_only_invoice(self):
        default_partner = self.env.ref("l10n_sv_dte_pos.default_partner_on_pos", raise_if_not_found=False)
        if self.only_invoice and default_partner:
            self.default_partner_id = default_partner.id
        else:
            self.default_partner_id = False

    def open_ui(self):
        """Open the pos interface with config_id as an extra argument.

        In vanilla PoS each user can only have one active session, therefore it was not needed to pass the config_id
        on opening a session. It is also possible to login to sessions created by other users.

        :returns: dict
        """
        self.ensure_one()
        if not self.l10n_sv_terminal_id and self.l10n_sv_fiscal_journal:
            raise UserError(_("Not found terminal for this TPV."))

        return super().open_ui()
