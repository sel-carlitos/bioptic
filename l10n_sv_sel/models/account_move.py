from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def unlink(self):
        for move in self:
            if move.journal_id.l10n_sv_fiscal_journal:
                if move.l10n_sv_dte_send_state and move.l10n_sv_dte_send_state != 'tosend':
                    raise UserError('Cannot delete a document sent to the tax authorities.')
            elif move.state != 'draft':
                raise UserError(_('Cannot delete an entry NOT in draft state.'))
        return super().unlink()


    def action_send_to_hacienda(self):
        invoices = self._l10n_sv_check_moves_for_send()
        for move in invoices:
            if (
                move.l10_sv_dte_id.invoice_id
                and move.l10_sv_dte_id.json_file
                and move.l10_sv_dte_id.l10n_sv_dte_send_state in ["signed_pending"]
            ):
                move.l10_sv_dte_id.action_send_to_hacienda()
