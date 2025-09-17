from odoo import api, models, fields, Command
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import (
    CANCELLATION_TYPE
)


class L10nSvDteCancel(models.TransientModel):
    """
    This wizard will cancel the all the selected invoices.
    If in the journal, the option allow cancelling entry is not selected then
    it will give warning message.
    """

    _name = "l10n_sv_dte.move.cancel"
    _description = "Cancel the Selected Invoice"

    move_ids = fields.Many2many(comodel_name='account.move')
    l10n_sv_cancellation_type = fields.Selection(CANCELLATION_TYPE,
                                                 string="Cancellation Type",
                                                 default="2",
                                                 copy=False,
                                                 required=True,
                                                 )
    reason = fields.Text(string="Reason for Cancellation", default="Rescindir de la operación realizada",
                         help="This reason will be printed in the cancellation document.",
                         )
    l10n_sv_responsible_annulation_id = fields.Many2one("res.users", string="Responsible for Annulation",
                                                        default=lambda self: self.env.user)

    @api.model
    def default_get(self, fields_list):
        # EXTENDS 'base'
        results = super().default_get(fields_list)

        if 'move_ids' in results:
            source_invoices = self.env['account.move'].browse(results['move_ids'][0][2])
            invoices = source_invoices._l10n_sv_check_move_for_annul()
            results['move_ids'] = [Command.set(invoices.ids)]

        return results

    def move_cancel(self):
        self.ensure_one()
        for move in self.move_ids:
            move.write(
                {
                    "l10n_sv_cancellation_type": self.l10n_sv_cancellation_type,
                    "l10n_sv_cancellation_reason": self.reason,
                    "l10n_sv_responsible_annulation_id": self.l10n_sv_responsible_annulation_id.id,
                }
            )
            move._l10n_sv_invoice_annul_dte_try()
