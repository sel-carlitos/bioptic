from odoo import _, models, fields
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_sv_date_issue_ref = fields.Date(
        string="Fecha de emision del DTE de referencia",
        copy=False,
    )

    dte_reference_doc = fields.Char(
        string="Documento de referencia DTE",
        related='reversed_entry_id.l10_sv_dte_id.name',
        copy=False,
    )
    voucher_type_id_ref = fields.Many2one(
        'l10n_sv.voucher.type',
        string="Tipo de comprobante de referencia",
        related='reversed_entry_id.l10n_sv_voucher_type_id',
        copy=False,
    )
    dte_reference_doc_debit_note = fields.Char(
        string="Documento de referencia DTE ND",
        related='debit_origin_id.l10_sv_dte_id.name',
        copy=False,
    )
    voucher_type_id_ref_debit_note = fields.Many2one(
        'l10n_sv.voucher.type',
        string="Tipo de comprobante de referencia ND",
        related='debit_origin_id.l10n_sv_voucher_type_id',
        copy=False,
    )

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
