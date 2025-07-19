# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, Command


class L10nSvDteCancel(models.TransientModel):
    """
    This wizard will cancel the all the selected invoices.
    If in the journal, the option allow cancelling entry is not selected then
    it will give warning message.
    """

    _inherit = "l10n_sv_dte.move.cancel"

    pos_order_ids = fields.Many2many(comodel_name='pos.order')

    @api.model
    def default_get(self, fields_list):
        # EXTENDS 'l10n_sv_dte'
        results = super().default_get(fields_list)

        if 'pos_order_ids' in results:
            source_orders = self.env['pos.order'].browse(results['pos_order_ids'][0][2])
            invoices = source_orders._l10n_sv_check_order_for_annul()
            results['pos_order_ids'] = [Command.set(invoices.ids)]

        return results

    def move_cancel(self):
        # EXTENDS 'l10n_sv_dte'
        self.ensure_one()
        if self.pos_order_ids:
            for order in self.pos_order_ids:
                order.write(
                    {
                        "l10n_sv_cancellation_type": self.l10n_sv_cancellation_type,
                        "l10n_sv_cancellation_reason": self.reason,
                    }
                )
                order._l10n_sv_invoice_pos_annul_dte_try()
        else:
            super().move_cancel()
