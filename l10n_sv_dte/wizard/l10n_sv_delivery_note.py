# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command
from datetime import datetime

from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    CANCELLATION_TYPE
)
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    GENERATION_TYPE_SELECTION
)
import pytz


class L10nSvDeliveryNoteWizard(models.TransientModel):
    """
    Account move reversal wizard, it cancel an account move by reversing it.
    """
    _name = 'l10n_sv.delivery.note.wizard'
    _description = 'Delivery Note'
    _check_company_auto = True

    move_ids = fields.Many2many(comodel_name='account.move')
    new_move_ids = fields.Many2many('account.move', 'account_move_delivery_note_new_move', 'reversal_id', 'new_move_id')
    l10n_sv_cancellation_type = fields.Selection(CANCELLATION_TYPE,
                                                 string="Cancellation Type",
                                                 default="1",
                                                 copy=False,
                                                 required=True,
                                                 )
    l10n_sv_generation_type = fields.Selection(GENERATION_TYPE_SELECTION, string="Generation Type", default='2')
    reason = fields.Text(string="Reason for Cancellation",
                         help="This reason will be printed in the cancellation document.",
                         )
    company_id = fields.Many2one('res.company', required=True, readonly=True)
    # available_journal_ids = fields.Many2many('account.journal', compute='_compute_available_journal_ids')
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        required=True,
        compute='_compute_journal_id',
        readonly=False,
        store=True,
        check_company=True,
        help='If empty, uses the journal of the journal entry to be reversed.',
    )
    l10n_sv_voucher_type_id = fields.Many2one('l10n_sv.voucher.type', 'Voucher Type', ondelete='cascade',
                                              compute='_compute_l10n_sv_document_type', readonly=False)
    date = fields.Date(string='Reversal date', default=fields.Date.context_today)
    currency_id = fields.Many2one('res.currency', compute="_compute_from_moves")
    move_type = fields.Char(compute="_compute_from_moves")

    @api.depends('move_ids')
    def _compute_l10n_sv_document_type(self):
        for record in self:
            nre = self.env["l10n_sv.voucher.type"].search([('code', '=', '04')])
            record.l10n_sv_voucher_type_id = nre[0]

    @api.depends('move_ids')
    def _compute_journal_id(self):
        for record in self:
            if record.journal_id:
                record.journal_id = record.journal_id
            else:
                journals = record.move_ids.journal_id.filtered(lambda x: x.active)
                record.journal_id = journals[0] if journals else None

    @api.depends('move_ids')
    def _compute_from_moves(self):
        for record in self:
            move_ids = record.move_ids._origin
            # record.residual = len(move_ids) == 1 and move_ids.amount_residual or 0
            record.currency_id = len(move_ids.currency_id) == 1 and move_ids.currency_id or False
            record.move_type = move_ids.move_type if len(move_ids) == 1 else (any(
                move.move_type in ('in_invoice', 'out_invoice') for move in move_ids) and 'some_invoice' or False)

    @api.model
    def default_get(self, fields_list):
        res = super(L10nSvDeliveryNoteWizard, self).default_get(fields_list)
        move_ids = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get(
            'active_model') == 'account.move' else self.env['account.move']

        if len(move_ids.company_id) > 1:
            raise UserError(_("All selected moves for reversal must belong to the same company."))

        if any(move.state != "posted" for move in move_ids):
            raise UserError(_('You can only reverse posted moves.'))
        if 'company_id' in fields_list:
            res['company_id'] = move_ids.company_id.id or self.env.company.id
        if 'move_ids' in fields_list:
            res['move_ids'] = [(6, 0, move_ids.ids)]
        return res

    def _prepare_default_reversal(self, move):
        reverse_date = self.date
        now_utc = datetime.now(pytz.timezone('UTC'))
        mixed_payment_term = move.invoice_payment_term_id.id if move.invoice_payment_term_id.early_pay_discount_computation == 'mixed' else None
        return {
            'ref': _('Reversal of: %(move_name)s, %(reason)s', move_name=move.name, reason=self.reason)
            if self.reason
            else _('Reversal of: %s', move.name),
            'date': reverse_date,
            'invoice_date_due': reverse_date,
            'invoice_date': move.is_invoice(include_receipts=True) and (self.date or move.date) or False,
            'journal_id': self.journal_id.id,
            'invoice_payment_term_id': mixed_payment_term,
            'invoice_user_id': move.invoice_user_id.id,
            'auto_post': 'at_date' if reverse_date > fields.Date.context_today(self) else 'no',
            'l10n_sv_voucher_type_id': self.l10n_sv_voucher_type_id.id,
            'l10n_sv_generation_type_ref': self.l10n_sv_generation_type,
            'l10n_sv_date_issue_ref': now_utc.strftime("%Y-%m-%d %H:%M:%S"),
            'l10n_sv_generation_code_ref': move.l10_sv_dte_id.l10n_sv_generation_code,
            'l10n_sv_terminal_id': move.l10n_sv_terminal_id.id,
        }

    def reverse_moves(self, is_modify=False):
        self.ensure_one()
        moves = self.move_ids

        # Create default values.
        partners = moves.company_id.partner_id + moves.commercial_partner_id

        bank_ids = self.env['res.partner.bank'].search([
            ('partner_id', 'in', partners.ids),
            ('company_id', 'in', moves.company_id.ids + [False]),
        ], order='sequence DESC')
        partner_to_bank = {bank.partner_id: bank for bank in bank_ids}
        default_values_list = []
        for move in moves:
            if move.is_outbound():
                partner = move.company_id.partner_id
            else:
                partner = move.commercial_partner_id
            default_values_list.append({
                'partner_bank_id': partner_to_bank.get(partner, self.env['res.partner.bank']).id,
                **self._prepare_default_reversal(move),
            })

        batches = [
            [self.env['account.move'], [], True],  # Moves to be cancelled by the reverses.
            [self.env['account.move'], [], False],  # Others.
        ]
        for move, default_vals in zip(moves, default_values_list):
            is_auto_post = default_vals.get('auto_post') != 'no'
            is_cancel_needed = not is_auto_post and (is_modify or self.move_type == 'entry')
            batch_index = 0 if is_cancel_needed else 1
            batches[batch_index][0] |= move
            batches[batch_index][1].append(default_vals)

        # Handle reverse method.
        moves_to_redirect = self.env['account.move']
        for moves, default_values_list, is_cancel_needed in batches:
            new_moves = moves._reverse_moves(default_values_list, cancel=is_cancel_needed)
            moves._message_log_batch(
                bodies={move.id: _('This entry has been %s', reverse._get_html_link(title=_("reversed"))) for
                        move, reverse in zip(moves, new_moves)}
            )

            if is_modify:
                moves_vals_list = []
                for move in moves.with_context(include_business_fields=True):
                    data = move.copy_data(self._modify_default_reverse_values(move))[0]
                    data['line_ids'] = [line for line in data['line_ids'] if
                                        line[2]['display_type'] in ('product', 'line_section', 'line_note')]
                    moves_vals_list.append(data)
                new_moves = self.env['account.move'].create(moves_vals_list)

            moves_to_redirect |= new_moves

        self.new_move_ids = moves_to_redirect

        # Create action.
        action = {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(moves_to_redirect) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': moves_to_redirect.id,
                'context': {'default_move_type': moves_to_redirect.move_type},
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', moves_to_redirect.ids)],
            })
            if len(set(moves_to_redirect.mapped('move_type'))) == 1:
                action['context'] = {'default_move_type': moves_to_redirect.mapped('move_type').pop()}
        return action

    def refund_moves(self):
        return self.reverse_moves(is_modify=False)

    # def move_cancel(self):
    #     self.ensure_one()
    #     for move in self.move_ids:
    #         move.write(
    #             {
    #                 # "state": "cancel",
    #                 "l10n_sv_cancellation_type": self.l10n_sv_cancellation_type,
    #                 "l10n_sv_cancellation_reason": self.reason,
    #             }
    #         )
    #         move._l10n_sv_invoice_pos_annul_dte_try()
