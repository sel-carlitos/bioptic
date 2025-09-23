from odoo import models

class AccountDebitNote(models.TransientModel):
    _inherit = 'account.debit.note'

    def _prepare_default_values(self, move):
        res = super()._prepare_default_values(move)

        if self.country_code in ["SV"] and move.l10n_sv_fiscal_journal:
            res.update({"l10n_sv_date_issue_ref": move.invoice_date})
        return res
