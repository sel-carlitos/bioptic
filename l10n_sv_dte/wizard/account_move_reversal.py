# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from datetime import datetime
import pytz
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    GENERATION_TYPE_SELECTION
)


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    @api.model
    def default_get(self, fields_list):
        results = super(AccountMoveReversal, self).default_get(fields_list)
        if 'move_ids' in results:
            source_move = self.env['account.move'].browse(results['move_ids'][0][2])
            if source_move.country_code in ["SV",]:
                invoices = source_move._l10n_sv_check_move_for_refund()
                results['move_ids'] = [Command.set(invoices.ids)]

        return results

    l10n_sv_fiscal_journal = fields.Boolean(related='journal_id.l10n_sv_fiscal_journal')
    l10n_sv_generation_type = fields.Selection(GENERATION_TYPE_SELECTION, string="Generation Type", default='2')
    l10n_sv_voucher_type_id = fields.Many2one('l10n_sv.voucher.type', 'Voucher Type', ondelete='cascade',
                                              compute='_compute_l10n_sv_document_type', readonly=False)

    @api.model
    def _reverse_type_map(self, move_type):
        match = {
            'entry': 'entry',
            'out_invoice': 'out_refund',
            'in_invoice': 'in_refund',
            'in_refund': 'in_invoice',
            'out_receipt': 'in_receipt',
            'in_receipt': 'out_receipt',
        }
        return match.get(move_type)

    @api.depends('move_ids')
    def _compute_l10n_sv_document_type(self):
        for record in self:
            refund = record.env['account.move'].new({
                'move_type': record._reverse_type_map(record.move_ids.move_type),
                'journal_id': record.move_ids.journal_id.id,
                'partner_id': record.move_ids.partner_id.id,
                'company_id': record.move_ids.company_id.id,
            })
            record.l10n_sv_voucher_type_id = refund.l10n_sv_voucher_type_id

    def _prepare_default_reversal(self, move):
        """ Set the default document type and number in the new revsersal move taking into account the ones selected in
        the wizard """
        res = super()._prepare_default_reversal(move)
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
