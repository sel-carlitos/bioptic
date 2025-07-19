# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from odoo.addons.l10n_sv_dte.wizard.l10n_sv_dte_move_cancel import (
    CANCELLATION_TYPE
)
from datetime import datetime
import pytz


class PosOrder(models.Model):
    _inherit = "pos.order"

    l10_sv_dte_id = fields.Many2one(related="account_move.l10_sv_dte_id", string='DTE Document', copy=False)
    invoice_type = fields.Char(string="Invoice Type")
    l10n_sv_generation_code = fields.Char(related="account_move.l10n_sv_generation_code", string="Generation Code")
    l10n_sv_document_number = fields.Char(related="account_move.l10n_sv_document_number", string="Document Number")
    origin_dte = fields.Char(related="account_move.l10n_sv_generation_code_ref", string="Modifies")
    l10n_sv_voucher_type_id = fields.Many2one(related="account_move.l10n_sv_voucher_type_id", store=True)
    l10n_sv_dte_send_state = fields.Selection(related="account_move.l10n_sv_dte_send_state", string="DTE Send State")

    # QR
    QR_code = fields.Binary(related="l10_sv_dte_id.l10n_sv_qr_code", string="Code QR")

    # Annulation
    l10n_sv_annulation_generation_code = fields.Char(size=36, string="Annulation Generation Code")
    l10n_sv_cancellation_type = fields.Selection(CANCELLATION_TYPE, string="Cancellation Type")
    l10n_sv_cancellation_reason = fields.Text(string="Cancellation Reason")

    @api.depends("pos_reference", "l10n_latam_document_number")
    def _compute_new_display_name(self):
        for record in self:
            record.display_name = "%s - %s" % (record.pos_reference, record.l10n_sv_document_number)

    def _prepare_invoice_vals(self):
        result = super(PosOrder, self)._prepare_invoice_vals()
        if self.session_id.company_id.country_id.code == 'SV' and self.config_id.invoice_journal_id.l10n_sv_fiscal_journal:
            terminal_id = self.session_id.config_id.l10n_sv_terminal_id
            if not terminal_id:
                return False

            result["l10n_sv_terminal_id"] = terminal_id.id
            if result['move_type'] == 'out_refund':
                now_utc = datetime.now(pytz.timezone('UTC'))
                result["l10n_sv_date_issue_ref"] = now_utc.strftime("%Y-%m-%d %H:%M:%S")

            if self.amount_total >= 0:
                if self.invoice_type == 'factura':
                    result.update({
                        'l10n_sv_voucher_type_id': self.env.ref('l10n_sv_dte.voucher_03').id,
                    })
                elif self.invoice_type == 'consumo':
                    result.update({
                        'l10n_sv_voucher_type_id': self.env.ref('l10n_sv_dte.voucher_01').id,
                    })
            else:
                # Document type for refunds
                result.update({
                    'l10n_sv_voucher_type_id': self.env.ref('l10n_sv_dte.voucher_05').id,
                })

        return result

    def _create_invoice(self, move_vals):
        move = super()._create_invoice(move_vals)
        if self.env.company.country_code == 'SV':
            if move.reversed_entry_id:
                reversed_move_id = self.env['account.move'].browse(move.reversed_entry_id.id)
                invoices = reversed_move_id._l10n_sv_check_move_for_refund()
                move.l10n_sv_generation_code_ref = invoices.l10n_sv_document_number

        return move

    def _refund(self):
        """
        Create a copy of order  for refund order.
        Este metodo es llamadao desde el bton refund del backend.
        """

        res = super(PosOrder, self)._refund()
        if self.env.company.country_code == 'SV':
            reversed_move_id = self.env['account.move'].browse(self.account_move.id)
            invoices = reversed_move_id._l10n_sv_check_move_for_refund()
            return invoices

        return res

    def _l10n_sv_check_order_for_annul(self):
        failed_orders = self.filtered(lambda o: o.state == 'cancel')
        if failed_orders:
            invoices_str = ", ".join(failed_orders.mapped('name'))
            raise UserError(_("Orders %s only cannot be cancelled as they are already in 'Cancelled' state.", invoices_str))

        invoices = self
        return invoices

    def _l10n_sv_invoice_pos_annul_dte_try(self):
        records_sorted = self.sorted('id')
        orders = records_sorted._l10n_sv_check_order_for_annul()

        if len(orders.company_id) != 1:
            raise UserError(_("You can only process orders sharing the same company."))

        for order in orders:
            order._l10n_sv_annul_dte()

    def _l10n_sv_check_documents_for_send(self):
        """ Ensure the current records are eligible for sent to Hacienda.

                """
        failed_moves = self.filtered(
            lambda o: (not o.company_id.l10n_sv_mh_auth_pass or not o.company_id.l10n_sv_mh_auth_user)
                      and o.country_code == 'SV')
        if failed_moves:
            invoices_str = ", ".join(failed_moves.mapped('name'))
            raise UserError(_("Invoices %s not eligible to sent .", invoices_str))

        invoices = self
        return invoices

    def _l10n_sv_annul_dte(self):
        orders = self._l10n_sv_check_documents_for_send()
        for order in orders:
            if not order.l10n_sv_annulation_generation_code:
                order.l10n_sv_annulation_generation_code = order.account_move.l10n_sv_generate_uuid()

            l10_sv_dte_id = order.l10_sv_dte_id
            annulated = l10_sv_dte_id.action_annul_dte(l10n_sv_cancellation_type=order.l10n_sv_cancellation_type,
                                                       l10n_sv_cancellation_reason=order.l10n_sv_cancellation_reason,
                                                       l10n_sv_annulation_generation_code=order.l10n_sv_annulation_generation_code,
                                                       )

            if annulated:
                order.write(
                    {
                        "state": "cancel",
                    }
                )
                email_template = order.env.ref("l10n_sv_dte.email_template_dte_invalidated")
                if email_template:
                    email_template.send_mail(l10_sv_dte_id.id, force_send=True)

    def l10n_sv_action_annul_dte_wizard(self):
        self.ensure_one()
        return {
            'name': _("Annul DTE"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'l10n_sv_dte.move.cancel',
            'target': 'new',
            'context': {'default_pos_order_ids': [Command.set(self.ids)]},
        }
