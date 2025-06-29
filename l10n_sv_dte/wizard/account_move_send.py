# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveSend(models.AbstractModel):
    _inherit = 'account.move.send'

    # -------------------------------------------------------------------------
    # ATTACHMENTS
    # -------------------------------------------------------------------------

    @api.model
    def _get_invoice_extra_attachments(self, move):
        """
                :returns: object (ir.attachment)
                """
        # EXTENDS 'account'

        # we require these to be downloadable for a better UX. It was also said that the xml and pdf files are
        # important files that needs to be shared with the customer.

        attachments = super()._get_invoice_extra_attachments(move)
        if move.country_code in ['SV'] and move.l10n_sv_fiscal_journal:
            if move.l10_sv_dte_id and move.l10_sv_dte_id.json_file and move.l10_sv_dte_id.l10n_sv_dte_send_state == 'delivered_accepted':
                doc = move.l10_sv_dte_id
                ir_attachment = self.env['ir.attachment'].sudo()
                attachment_vals = {'name': str(doc.json_file_name),
                                   'datas': doc.json_file,
                                   'res_id': move.id,
                                   'res_model': "account.move",
                                   'type': 'binary',
                                   'res_field': 'json_file',
                                   }
                att = ir_attachment.create(attachment_vals)
                attachments |= att

        return attachments
