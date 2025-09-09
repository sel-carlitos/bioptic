# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from odoo.addons.l10n_cr_invoice.hacienda_api import HaciendaApi
from odoo.addons.l10n_cr_invoice.hacienda_api import HACIENDA_RESOLUTION_URL
from .MR_doc import MR_DOC
import base64
import tempfile
import subprocess
import logging
_logger = logging.getLogger(__name__)

MR_STATE_MAP = {
    "Accepted": "accepted",
    "Reject": "reject",
}


class AccountMove(models.Model):
    _inherit = "account.move"

    supplier_economic_activity_id = fields.Many2one('ce.economic.activity', string="Supplier Economic Activity",
                                                    ondelete="restrict")

    # === BUSINESS METHODS ===#
    def _l10n_cr_action_gen_xml_MR(self):
        self.ensure_one()
        ceconfig = self.company_id.setting_id or self.company_id.parent_id.setting_id
        terminal_id = self.env['ce.terminal'].search([('company_id', '=', self.company_id.id)], limit=1)
        if not terminal_id:
            raise ValidationError(_("There is not active Terminal"))

        state_inv_supplier_dict = dict(self._fields['state_inv_supplier'].selection)
        mr_doc = MR_DOC(state_inv_supplier=self.state_inv_supplier,
                        xml_amount_total=self.xml_amount_total,
                        xml_amount_tax=self.xml_amount_tax,
                        partner_id=self.partner_id,
                        company_id=self.company_id,
                        ref=self.ref,
                        economic_activity_id=self.economic_activity_id)
        cedoc = mr_doc.gen_mr_doc(terminal_id, state_inv_supplier_dict)
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(b'<?xml version="1.0" encoding="utf-8"?>')
        cedoc.export(file, 0, namespacedef_="", pretty_print=False)
        file.write(b'\n')
        file.close()
        xml_name = "{}.xml".format('MR-%s' % (cedoc.get_NumeroConsecutivoReceptor()))
        args = 'mv ' + file.name
        args = args.split()
        signed_filename = "/tmp/" + xml_name
        args.append(signed_filename)
        subprocess.run(args)
        xml_f = open(signed_filename, 'rb')
        xml_file = xml_f.read()
        xml_encoded = bytes(xml_file)
        hacienda_api = HaciendaApi(ceconfig)
        xml_signed = hacienda_api.generate_signature(xml_encoded, HACIENDA_RESOLUTION_URL)
        _logger.info("##### MR FIRMADO: " + signed_filename)
        consecutive = cedoc.get_NumeroConsecutivoReceptor()
        subprocess.call(['rm', '-f', signed_filename])
        self.write({'xml_mh_file': base64.b64encode(xml_signed), 'xml_mh_file_name': xml_name})
        xml_f.close()
        return (self.xml_mh_file, consecutive)

    def _l10n_cr_get_hacienda_status(self):
        company_id = self.company_id
        ceconfig = company_id.setting_id or self.company_id.parent_id.setting_id
        hacienda_api = HaciendaApi(ceconfig)
        get_json = hacienda_api.getHaciendaStatus(self.l10n_cr_document_number)
        return get_json

    # ===== BUTTONS =====

    def action_consultatrackids(self):
        company_id = self.company_id
        ceconfig_id = company_id.setting_id or company_id.parent_id.setting_id
        if not ceconfig_id:
            action = self.env.ref("base.action_res_company_form")
            msg = _("Must be selected an Environment in a Company.")
            raise RedirectWarning(msg, action.id, _("Go to Setting"))

        vals = self._l10n_cr_get_hacienda_status()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'sticky': True,
                'message': "%s" % vals,
            }
        }

    def action_send_response_mr(self):
        """Envia la CONFIRMACIÓN DE ACEPTACIÓN O RECHAZO DE LOS DOCUMENTOS ELECTRÓNICOS
        POR PARTE DEL OBLIGADO TRIBUTARIO."""

        company_id = self.company_id
        ceconfig_id = company_id.setting_id or company_id.parent_id.setting_id
        if not ceconfig_id:
            action = self.env.ref("base.action_res_company_form")
            msg = _("Must be selected an Environment in a Company.")
            raise RedirectWarning(msg, action.id, _("Go to Setting"))

        now = fields.Datetime.context_timestamp(
            self.with_context(tz="America/Costa_Rica"),
            fields.Datetime.now(),
        )
        data_sent = {'date': now.strftime("%Y-%m-%dT%H:%M:%S-06:00"),
                     'name': self.l10n_cr_document_number,
                     'em_ident': self.partner_id.identification_id.code,
                     'em_vat': self.partner_id.vat,
                     'rec_ident': self.company_id.partner_id.identification_id.code,
                     'rec_vat': self.company_id.partner_id.vat,
                     }
        xml_signed, consecutive = self._l10n_cr_action_gen_xml_MR()
        data_sent['consecutivo'] = consecutive
        ceconfig = company_id.setting_id
        hacienda_api = HaciendaApi(ceconfig)

        try:
            post_json = hacienda_api.postMR(data_sent, xml_signed)
            response_status = post_json.get('status')
            response_text = post_json.get('text')
            if 200 <= response_status <= 299:
                self.write({'l10n_cr_mh_send_state': MR_STATE_MAP.get(response_text)})
                return True
            elif response_status == 400:
                response_text = response_text
                _logger.error(response_text)
                self.message_post(subject='Error', body=response_text)
                return False
            if response_status == 401:
                _logger.error("Service Unauthorized")
                return False
        except Exception as e:
            _logger.error(e)
            raise UserError("Error")

    def create_PO(self):
        PurchaseOrder = self.env['purchase.order']
        purchase_order_vals = {
            'priority': '0',
            'partner_id': self.partner_id.id,
            'partner_ref': self.partner_id.ref,
            'currency_id': self.currency_id.id,
            'date_order': self.invoice_date,
            'date_planned': self.invoice_date,
            'notes': '<p><br></p>',
            'user_id': self.env.user.id,
            'company_id': self.env.company.id,
            'picking_type_id': 1,
        }
        order_id = PurchaseOrder.create(purchase_order_vals)

        for r in self.invoice_line_ids:
            if not r.product_id:
                pp = self.env['product.product']
                s = pp.search([('name', '=', r.name)], limit=1)
                if len(s) == 1:
                    product_id = s.id
                    product_name = s.name
                else:
                    raise UserError('Producto "%s" no existe en el sistema, por favor creelo o asocielo con uno existente antes de continuar.' % r.name)
            else:
                product_id = r.product_id.id
                product_name = r.product_id.name

            e = {
                'order_id': order_id.id,
                'product_id': product_id,
                'name': product_name,
                'date_planned': self.invoice_date,
                'product_qty': r.quantity,
                'qty_received_manual': r.quantity,
                'product_uom': r.product_uom_id.id,
                'price_unit': r.price_unit,
                'taxes_id': r.tax_ids,
                'discount': r.discount or 0,

            }
            self.env['purchase.order.line'].create(e)

        return {
            'name': _('Pedidos de compra'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': order_id.id,
        }
