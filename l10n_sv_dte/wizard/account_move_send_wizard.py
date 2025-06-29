# -*- coding: utf-8 -*-

from odoo import models


class AccountMoveSendWizard(models.TransientModel):
    _inherit = 'account.move.send.wizard'

    def action_send_and_print(self, allow_fallback_pdf=False):
        # EXTENDS account - to mark the DTE l10n_sv_state_mail as sent .

        res = super().action_send_and_print(allow_fallback_pdf=allow_fallback_pdf)
        if res:
            move = self.move_id
            if move.country_code in ['SV'] and move.l10n_sv_fiscal_journal:
                if move.l10_sv_dte_id and move.l10_sv_dte_id.l10n_sv_dte_send_state == 'delivered_accepted':
                    move.l10_sv_dte_id.l10n_sv_state_mail = 'sent'
