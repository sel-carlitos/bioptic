# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from datetime import datetime
import pytz
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    GENERATION_TYPE_SELECTION
)


class AccountDebitNote(models.TransientModel):
    _inherit = "account.debit.note"

    l10n_sv_fiscal_journal = fields.Boolean(related='journal_id.l10n_sv_fiscal_journal')
    l10n_sv_generation_type = fields.Selection(GENERATION_TYPE_SELECTION, string="Generation Type", default='2')
    l10n_sv_voucher_type_id = fields.Many2one('l10n_sv.voucher.type', 'Voucher Type', ondelete='cascade',
                                              compute='_compute_l10n_sv_document_type', readonly=False)

    @api.depends('move_ids')
    def _compute_l10n_sv_document_type(self):
        for record in self:
            voucher_type = self.env["l10n_sv.voucher.type"].search([('internal_type', '=', 'debit_note')])
            record.l10n_sv_voucher_type_id = voucher_type[0]

    def _prepare_default_values(self, move):
        res = super(AccountDebitNote, self)._prepare_default_values(move)
        if self.country_code in ['SV'] and move.l10n_sv_fiscal_journal:
            now_utc = datetime.now(pytz.timezone('UTC'))
            res.update({
                'l10n_sv_voucher_type_id': self.l10n_sv_voucher_type_id.id,
                'l10n_sv_generation_type_ref': self.l10n_sv_generation_type,
                'l10n_sv_date_issue_ref': now_utc.strftime("%Y-%m-%d %H:%M:%S"),
                'l10n_sv_generation_code_ref': move.l10_sv_dte_id.l10n_sv_generation_code,
                'l10n_sv_terminal_id': move.l10n_sv_terminal_id.id,
            })

        return res
