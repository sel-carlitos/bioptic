# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class L10nSvVoucherType(models.Model):
    _name = "l10n_sv.voucher.type"
    _description = "Voucher Type"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    internal_type = fields.Selection(
        [('invoice', 'Invoices'), ('debit_note', 'Debit Notes'), ('credit_note', 'Credit Notes')], index=True,
        help='Analog to odoo account.move.move_type but with more options allowing to identify the kind of document we are'
             ' working with. (not only related to account.move, could be for documents of other models like stock.picking)')
    move_type = fields.Selection(
        selection=[
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Vendor Bill'),
            ('mh', 'Ministerio Hacienda'),
        ],
        string='Type',
    )

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"
