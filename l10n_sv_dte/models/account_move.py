# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    GENERATION_TYPE_SELECTION
)
from odoo.addons.l10n_sv_dte.wizard.l10n_sv_dte_move_cancel import (
    CANCELLATION_TYPE
)
import uuid
import pytz
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    l10_sv_dte_id = fields.Many2one('l10n_sv.dte.document', string='DTE Document', readonly=True, copy=False)
    l10n_sv_terminal_id = fields.Many2one('l10n_sv.terminal', string="Terminal", copy=False)
    l10n_sv_economic_activity_id = fields.Many2one('l10n_sv.economic.activity', string="Economic Activity")
    l10n_sv_voucher_type_id = fields.Many2one("l10n_sv.voucher.type", compute='_compute_l10n_sv_l10n_sv_voucher_type',
                                              store=True, string="Voucher Type", readonly=False, auto_join=True,
                                              index=True)
    l10n_sv_available_voucher_type_ids = fields.Many2many('l10n_sv.voucher.type',
                                                          compute='_compute_l10n_sv_available_document_types')
    l10n_sv_dte_situation = fields.Selection(
        [('1', 'Transmisión normal'),
         ('2', 'Transmisión por contingencia'),
         ],
        string="Status Voucher", required=True, default='1', help="CAT- 004: Tipo de Transmisión")
    l10n_sv_amount_discount = fields.Monetary(store=True, readonly=True, compute='_compute_amount')
    l10n_sv_dte_contingency_type = fields.Selection(
        [('1', 'No disponibilidad de sistema del MH'),
         ],
        string="Contingency Type", required=True, default='1', help="CAT- 005: Tipo de Contingencia")
    l10n_sv_is_exportation = fields.Boolean(string="Exportation Invoice", default=False)
    l10n_sv_document_number = fields.Char(string="Document Number", copy=False)
    l10n_sv_generation_code = fields.Char(string="Generation Code", related="l10_sv_dte_id.l10n_sv_generation_code")
    l10n_sv_dte_send_state = fields.Selection(related='l10_sv_dte_id.l10n_sv_dte_send_state', string='DTE Send State',
                                              tracking=True, store=True, copy=False, readonly=True)
    l10n_sv_fiscal_journal = fields.Boolean(related='journal_id.l10n_sv_fiscal_journal')
    l10n_sv_qr_code = fields.Binary(string="Code QR", readonly=True, related="l10_sv_dte_id.l10n_sv_qr_code")
    l10n_sv_electronic_stamp = fields.Text(string="Electronic Stamp", readonly=True, copy=False,
                                           related="l10_sv_dte_id.l10n_sv_electronic_stamp")
    # Exportation
    l10n_sv_type_item_to_import = fields.Selection([("1", "Bienes"),
                                                    ("2", "Servicios"),
                                                    ("3", "Ambos (Bienes y Servicios, incluye los dos inherente a los Productos o servicios)"),
                                                    ("4", "Otros tributos por ítem"),
                                                    ], string="Type Item to Import",
                                                   help="CAT- 011: Tipo de ítem")
    l10n_sv_tax_precinct = fields.Selection([("02", "Marítima de Acajutla"),
                                             ("03", "Aérea Monseñor Óscar Arnulfo Romero"),
                                             ], string="Tax Precinct", help="CAT- 027: Recinto fiscal")
    l10n_sv_regime = fields.Selection([("EX-1.1000.000", "Exportación Definitiva, Exportación Definitiva, Régimen Común"),
                                       ("EX-1.1040.000", "Exportación Definitiva, Exportación Definitiva Sustitución de Mercancías, Régimen Común"),
                                       ], string="Regime", help="CAT- 028: Régimen")

    # Reference
    l10n_sv_generation_type_ref = fields.Selection(GENERATION_TYPE_SELECTION, string="Generation Type Ref")
    l10n_sv_date_issue_ref = fields.Datetime(string="Fecha y hora de emision del DTE de referencia", copy=False)
    l10n_sv_generation_code_ref = fields.Char("Código de generación de referencia", copy=False,
                                              help='Codigo de generacion del DTE de referencia')

    # Annulation
    l10n_sv_annulation_generation_code = fields.Char(size=36, string="Annulation Generation Code")
    l10n_sv_cancellation_type = fields.Selection(CANCELLATION_TYPE, string="Cancellation Type")
    l10n_sv_cancellation_reason = fields.Text(string="Cancellation Reason")
    l10n_sv_responsible_annulation_id = fields.Many2one("res.users", string="Responsible for Annulation")

    # === COMPUTE METHODS ===#

    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for inv in self:
            if inv.is_invoice(include_receipts=False):
                line_total_discount = sum(
                    (line.price_unit * line.quantity * line.discount / 100) for line in inv.invoice_line_ids)
                total_discount = line_total_discount
                inv.l10n_sv_amount_discount = total_discount

    @api.depends('move_type', 'debit_origin_id', 'partner_id')
    def _compute_l10n_sv_l10n_sv_voucher_type(self):
        for rec in self.filtered(lambda x: x.move_type != 'entry'
                                           and x.company_id.country_id == self.env.ref("base.sv")):
            sequence = {
                'out_invoice': '03',
                'out_refund': '05',
                'in_refund': '05',
                'in_invoice': '14',
            }

            if rec.l10n_sv_is_exportation:
                code = '11'
            elif rec.debit_origin_id:
                code = "02"
            elif rec.partner_id and not rec.partner_id.vat and rec.move_type in ['out_invoice']:
                code = "01"
            else:
                code = sequence[rec.move_type]

            voucher_type_id = self.env['l10n_sv.voucher.type'].search([('code', '=', code)], limit=1)
            rec.l10n_sv_voucher_type_id = voucher_type_id.id and voucher_type_id[0].id or False

    @api.depends('journal_id', 'company_id', 'move_type')
    def _compute_l10n_sv_available_document_types(self):
        self.l10n_sv_available_voucher_type_ids = False
        for rec in self.filtered(lambda x: x.journal_id and x.company_id.country_id == self.env.ref("base.sv")):
            domain = []

            if rec.move_type in ['out_refund', 'in_refund']:
                internal_types = ['credit_note']
            else:
                internal_types = ['invoice', 'debit_note']

            domain.append(('internal_type', 'in', internal_types))
            if rec.journal_id.l10n_sv_fiscal_journal:
                if rec.move_type == 'out_invoice':
                    domain.append(('move_type', '=?', 'out_invoice'))
                elif rec.move_type == 'in_invoice':
                    domain.append(('move_type', '=?', 'in_invoice'))

            voucher_types = self.env["l10n_sv.voucher.type"].search(domain)
            rec.l10n_sv_available_voucher_type_ids = voucher_types

    # === BUSINESS METHODS ===#

    def _get_invoice_report_filename(self, extension='pdf'):
        """ Get the filename of the generated invoice report with extension file. """
        self.ensure_one()
        if self.l10n_sv_fiscal_journal and self.country_code in ['SV'] and self.l10_sv_dte_id:
            return self.l10_sv_dte_id.name

        return super()._get_invoice_report_filename(extension)

    def _get_report_base_filename(self):
        self.ensure_one()
        if self.country_code == 'SV' and self.l10n_sv_fiscal_journal:
            return self._get_invoice_report_filename()

        return super()._get_report_base_filename()

    def l10n_sv_create_document(self, terminal_id, recreate=False):
        if not self.l10_sv_dte_id or recreate:
            Document = self.env['l10n_sv.dte.document']
            default_data = (Document.with_context(force_economic_activity=self.l10n_sv_economic_activity_id.id).
                            default_get(['state', 'company_id', 'l10n_sv_dte_situation', 'ind_state',
                                         'l10n_sv_economic_activity_id']))

            hora_actual = datetime.now(pytz.timezone('UTC')).time()
            default_data.update(
                invoice_id=self.id,
                l10n_sv_terminal_id=terminal_id.id,
                l10n_sv_voucher_type_id=self.l10n_sv_voucher_type_id.id,
                partner_id=self.partner_id.id,
                company_id=self.company_id.id,
                currency_id=self.currency_id.id,
                name=self.l10n_sv_document_number,
                situation=self.l10n_sv_dte_situation,
                l10n_sv_generation_code=self.l10n_sv_generate_uuid(),
                l10n_sv_invoice_type=self.move_type,
                date_issue=datetime.combine(self.invoice_date, hora_actual),
            )
            default_data.update(self._l10n_sv_prepare_document_additional_values())
            doc_id = Document.create(default_data)
            self.l10_sv_dte_id = doc_id.id
            doc_id.action_gen_json()
            return doc_id

    def _l10n_sv_prepare_document_additional_values(self):
        """
            Prepare the dict of values to create the additional values a documents. This method may be
            overridden to implement custom document generation (making sure to call super() to establish
            a clean extension chain).
            """
        return {

        }

    def _post(self, soft=True):
        # Primero se llama al padre para q genere la fecha de vencimiento, consecutivos, etc.
        for inv in self.filtered(lambda x: x.move_type not in ('entry',)):
            if inv.country_code == 'SV' and inv.l10n_sv_fiscal_journal:
                if not inv.l10n_sv_terminal_id:
                    # Si no hay terminal en la factura, se establece la primera terminal activa en el sistema.
                    terminal_id = self.env["l10n_sv.terminal"].search([('company_id', '=', self.env.company.id),
                                                                       ('state', '=', 'active')], limit=1)

                    if not terminal_id:
                        raise ValidationError(_("There is not active Terminal"))
                    inv.l10n_sv_terminal_id = terminal_id

        res = super(AccountMove, self)._post(soft)

        for inv in res.filtered(lambda x: x.move_type not in ('entry',)):
            if inv.country_code == 'SV' and inv.l10n_sv_fiscal_journal:
                inv._l10n_sv_check_invoice_type_document_type()
                if inv.move_type in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']:
                    if not inv.l10n_sv_document_number:
                        inv.l10n_sv_document_number = inv.l10n_sv_terminal_id.gen_control_number(inv.l10n_sv_voucher_type_id)

                    if not inv.l10_sv_dte_id:
                        inv.l10n_sv_create_document(terminal_id=inv.l10n_sv_terminal_id)

        return res

    def l10n_sv_generate_uuid(self):
        self.ensure_one()
        uid = uuid.uuid4()

        # Convertir a cadena en mayúsculas, con guiones y llaves
        uid_formated = f"{str(uid).upper()}"
        return uid_formated

    @api.constrains("move_type", "l10n_sv_voucher_type_id")
    def _l10n_sv_check_invoice_type_document_type(self):
        # for rec in self.filtered('l10n_latam_document_type_id.internal_type'):
        #     internal_type = rec.l10n_latam_document_type_id.internal_type
        #     invoice_type = rec.move_type
        #     if internal_type in ['debit_note', 'invoice'] and invoice_type in ['out_refund', 'in_refund'] and \
        #             rec.l10n_latam_document_type_id.code != '99':
        #         raise ValidationError(_('You can not use a %s document type with a refund invoice', internal_type))
        #     elif internal_type == 'credit_note' and invoice_type in ['out_invoice', 'in_invoice']:
        #         raise ValidationError(_('You can not use a %s document type with a invoice', internal_type))

        for rec in self.filtered(
                lambda r: (r.company_id.country_id == self.env.ref("base.sv")
                           and r.l10n_sv_voucher_type_id)
        ):
            l10n_sv_voucher_type_id = rec.l10n_sv_voucher_type_id
            if rec.move_type in ("out_invoice", "out_refund"):
                if (
                        rec.amount_untaxed_signed >= 25000.00
                        and l10n_sv_voucher_type_id.code == '01'
                        and (not self.env["l10n_sv.dte.document"].get_document_number(rec.partner_id) or not rec.partner_id.l10n_sv_identification_id)
                ):
                    raise UserError(
                        _(
                            "If the invoice amount is greater than $25,000.00 "
                            "the customer should have a VAT and Identification Type to validate the invoice"
                        )
                    )

    def _l10n_sv_check_move_for_refund(self):
        failed_orders = self.filtered(lambda o: (o.l10n_sv_voucher_type_id
                                                 and o.l10n_sv_voucher_type_id.code not in ['03', '07']))
        if failed_orders:
            invoices_str = ", ".join(failed_orders.mapped('name'))
            raise UserError(_("Moves %s not eligible to Credit Note or Debit Note.", invoices_str))

        invoices = self
        return invoices

    def _l10n_sv_check_moves_for_send(self):
        """ Ensure the current records are eligible for sent to Hacienda.

                """
        failed_auth_moves = self.filtered(
            lambda o: (o.country_code == 'SV'
                       and (not o.company_id.l10n_sv_mh_auth_pass or not o.company_id.partner_id.nit)))
        if failed_auth_moves:
            invoices_str = ", ".join(failed_auth_moves.mapped('name'))
            raise UserError(_("Invoices %s not eligible to sent (Not exist credentials to auth).", invoices_str))

        invoices = self
        return invoices

    def _l10n_sv_check_move_for_annul(self):
        failed_orders = self.filtered(lambda o: o.state == 'cancel')
        if failed_orders:
            invoices_str = ", ".join(failed_orders.mapped('name'))
            raise UserError(_("Moves %s only cannot be cancelled as they are already in 'Cancelled' state.", invoices_str))

        invoices = self
        return invoices

    def _l10n_sv_invoice_annul_dte_try(self):
        records_sorted = self.sorted('id')
        moves = records_sorted._l10n_sv_check_move_for_annul()
        if len(moves.company_id) != 1:
            raise UserError(_("You can only process orders sharing the same company."))

        for move in moves:
            move._l10n_sv_annul_dte()

    def _l10n_sv_annul_dte(self):
        invoices = self._l10n_sv_check_moves_for_send()
        for move in invoices:
            if not move.l10n_sv_annulation_generation_code:
                move.l10n_sv_annulation_generation_code = move.l10n_sv_generate_uuid()

            l10_sv_dte_id = move.l10_sv_dte_id
            annulated = l10_sv_dte_id.action_annul_dte(l10n_sv_cancellation_type=self.l10n_sv_cancellation_type,
                                                       l10n_sv_cancellation_reason=self.l10n_sv_cancellation_reason,
                                                       l10n_sv_annulation_generation_code=self.l10n_sv_annulation_generation_code,
                                                       )

            if annulated:
                move.write(
                    {
                        "state": "cancel",
                    }
                )
                email_template = move.env.ref("l10n_sv_dte.email_template_dte_invalidated")
                if email_template:
                    email_template.send_mail(l10_sv_dte_id.id, force_send=True)
                    move._message_log(body=_("Email to invalidated DTE sent"))

    # ===== BUTTONS =====

    def button_draft(self):
        if self.country_code == 'SV':
            if self.l10_sv_dte_id and self.l10n_sv_dte_send_state in ['delivered_accepted', 'invalidated']:
                raise UserError("No puede establecer a borrador una factura enviada a Hacienda.")
            elif self.l10_sv_dte_id and self.l10n_sv_dte_send_state in ['not_sent']:
                self.l10_sv_dte_id.unlink()

            self.l10_sv_dte_id.unlink()

        res = super(AccountMove, self).button_draft()
        return res

    def action_send_to_hacienda(self):
        invoices = self._l10n_sv_check_moves_for_send()
        for move in invoices.filtered(lambda x: x.l10n_sv_dte_send_state == 'signed_pending'):  
            move.l10_sv_dte_id.action_send_to_hacienda()

    def l10n_sv_action_annul_dte_wizard(self):
        self.ensure_one()
        return {
            'name': _("Annul DTE"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'l10n_sv_dte.move.cancel',
            'target': 'new',
            'context': {'default_move_ids': [Command.set(self.ids)]},
        }

    def l10n_sv_action_delivery_note(self):
        action = self.env.ref('l10n_sv_dte.action_view_account_move_debit11')._get_action_dict()
        return action

    def l10n_sv_action_send_contingency(self):
        # self.l10n_sv_dte_situation = '2'
        if self.l10_sv_dte_id:
            self.l10_sv_dte_id.action_send_contingency(l10n_sv_dte_send_state='contingency')
