# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import models, fields, api
from odoo.fields import Command
from datetime import date


class AccountMove(models.Model):
    _inherit = 'account.move'

    def create_sale_order(self):
        if not self.invoice_date:
            self.invoice_date = date.today()
        if self.invoice_date:
            sale_order = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'state': 'draft',
                'date_order': self.invoice_date,
                'payment_term_id': self.invoice_payment_term_id.id,
                'order_line': [(0, 0, {
                    'product_id': invoice_line.product_id.id or False,
                    'name': invoice_line.name or "",
                    'product_uom_qty': invoice_line.quantity or 0.00,
                    'price_unit': invoice_line.price_unit,
                    'product_uom': invoice_line.product_uom_id.id or False,
                    'tax_id': invoice_line.tax_ids,
                    'invoice_lines': [Command.link(invoice_line.id)],
                })for invoice_line in self.invoice_line_ids],
            })

            return {
                'name': 'Sale Order',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': sale_order.id,
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'target': 'current',
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
