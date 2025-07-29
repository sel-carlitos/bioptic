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
