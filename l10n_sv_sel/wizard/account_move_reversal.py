from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    def _prepare_default_reversal(self, move):
        """Set the default date_issue_ref in the new revsersal move taking into account the one selected in
        the wizard"""
        res = super()._prepare_default_reversal(move)
        if self.country_code in ["SV"] and move.l10n_sv_fiscal_journal:
            res.update({"l10n_sv_date_issue_ref": move.invoice_date})
        return res
