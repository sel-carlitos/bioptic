# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from ..hacienda_api import HaciendaApi
from odoo.addons.l10n_sv_dte.models.account_tax import (
    SV_TAXES
)
from odoo.addons.l10n_sv_dte.hacienda_api import (
    DTE_VOUCHER_TYPE_VERSION_MAP
)
from collections import defaultdict
from . import FE
from . import CCFE
from . import NCE
from . import NDE
from . import FEXE
from . import FSEE
from . import CDE
from . import NRE
from . import CRE
from . import ANDTE
from . import CODTE
from datetime import datetime, timedelta
import tempfile
import logging
import subprocess
import base64
import pyqrcode
from werkzeug import urls
import json
import pytz

_logger = logging.getLogger(__name__)
L10N_SV_DATE_FORMAT = '%Y-%m-%d'
L10N_SV_HOUR_FORMAT = '%H:%M:%S'
L10N_SV_INCOTERMS_MAP = {"01": "EXW-En fabrica",
                         "02": "FCA-Libre transportista",
                         "03": "CPT-Transporte pagado hasta",
                         "04": "CIP-Transporte y seguro pagado hasta",
                         "05": "DAP-Entrega en el lugar"}
DTE_STATE_MAP = {
    "PROCESADO": "delivered_accepted",
    "RECHAZADO": "delivered_refused",
    "INVALIDADO": "invalidated",
}
GENERATION_TYPE_SELECTION = [('1', 'Físico'), ('2', 'Electrónico')]
CANCELLATION_TYPE = [('1', 'Error en la Información del Documento Tributario Electrónico a invalidar'),
                     ('2', 'Rescindir de la operación realizada'),
                     ('3', 'Otro'),
                     ]
TYPE_INVOICE = [
        ('out_invoice', 'Cliente'),
        ('in_invoice', 'Proveedor'),
        ('out_refund', 'Reembolso Cliente'),
        ('in_refund', 'Reembolso Proveedor'),
        ('out_ticket', 'Ticket Cliente'),
        ('in_ticket', 'Ticket Proveedor'),
    ]


def _get_l10n_sv_dte_send_state(self):
    """Returns actual invoice ECF sending status

    - to_send: default state.
    - invalid: sent ecf didn't pass XSD validation.
    - contingency: DGII unreachable by external service. Odoo should send it later
      until delivered accepted state is received.
    - delivered_accepted: expected state that indicate everything is ok with ecf
      issuing.
    - delivered_refused: ecf rejected by DGII.
    - not_sent: Odoo have not connection.
    - signed_pending: ECF was signed but API could not reach DGII. May be resend
      later.

    """
    return [
        ("to_send", "Not sent"),
        ("invalid", "Sent, but invalid"),
        ("contingency", "Contingency"),
        ("delivered_accepted", _("Delivered and accepted")),
        ("delivered_refused", _("Delivered and refused")),
        ("invalidated", _("Invalidated")),
        ("signed_pending", _("Signed and pending")),
    ]


class DTEDocument(models.Model):
    _name = 'l10n_sv.dte.document'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Electronic Voucher Document'
    _order = "id desc"

    name = fields.Char()
    l10n_sv_generation_code = fields.Char(size=36, string="Generation Code")
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='cascade', readonly=True,
                                 required=True, index=True)
    l10n_sv_dte_send_state = fields.Selection(string="DTE Send State", copy=False, required=True, readonly=True,
                                              selection=_get_l10n_sv_dte_send_state, default="to_send",
                                              index=True, tracking=True)
    l10n_sv_state_mail = fields.Selection(
        selection=[('not_sent', 'No enviado'),
                   ('sent', 'Enviado'),
                   ('not_mail', 'Sin Correo')], string="Email State", default='not_sent', copy=False)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one("res.currency", readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    json_file = fields.Binary("JSON File Simple", attachment=True,
                              help="This field holds the JSON file generated and signed by system")
    json_file1 = fields.Binary("JSON File Complete", attachment=True,
                               help="This field holds the JSON file generated and signed by system")
    json_file_name = fields.Char("Name of JSON file")
    currency_id = fields.Many2one('res.currency', string='Currency')
    json_amount_tax = fields.Float('Amount Total Tax')
    json_amount_total = fields.Float('Amount Total Document')
    json_mr_file = fields.Binary(string="Archivo JSON MR", attachment=True, copy=False)
    json_mr_file_name = fields.Char(string="Nombre Archivo JSON MR", copy=False)
    date_issue = fields.Datetime(copy=False)
    l10n_sv_terminal_id = fields.Many2one('l10n_sv.terminal', string="Terminal", copy=False)
    l10n_sv_economic_activity_id = fields.Many2one('l10n_sv.economic.activity', string="Economic Activity")
    l10n_sv_voucher_type_id = fields.Many2one("l10n_sv.voucher.type", compute='_compute_voucher_type', store=True,
                                              string="Voucher Type", readonly=False, auto_join=True, index=True)
    l10n_sv_receipt_stamp = fields.Text(string="Receipt Stamp", copy=False, readonly=True)
    situation = fields.Char(string="Status Voucher", required=True, copy=False, readonly=True)
    message_detail = fields.Text(string="Message Detail", copy=False)
    response_status_code = fields.Text()
    json_signed = fields.Text(copy=False)
    l10n_sv_invoice_type = fields.Selection(selection=TYPE_INVOICE, string="Internal Type", copy=False, readonly=True)

    # QR
    l10n_sv_qr_code = fields.Binary(string="Code QR", readonly=True, copy=False)
    l10n_sv_electronic_stamp = fields.Text(string="Electronic Stamp", copy=False, readonly=True)

    # Annulation
    l10n_sv_annulation_generation_code = fields.Char(size=36, string="Annulation Generation Code")
    json_andte_file = fields.Binary(attachment=True, string="Annulation Files",
                                    help="This field holds the XML file generated and signed by system")
    json_andte_file_name = fields.Char("Name of XML Commercial Approval Files")
    json_andte_signed = fields.Text(copy=False)
    l10n_sv_cancellation_type = fields.Selection(CANCELLATION_TYPE, string="Cancellation Type",
                                                 help="CAT- 024: Tipo de Invalidación")
    l10n_sv_cancellation_reason = fields.Text(string="Cancellation Reason")
    andte_dgii_message_ids = fields.Many2many('l10n_sv.dte.andte.message.detail', string='Annulation Documents')

    # Contingency
    json_codte_file = fields.Binary(attachment=True, string="Contingency File",
                                    help="This field holds the XML file generated and signed by system")
    json_codte_file_name = fields.Char("Name of XML Commercial Approval File")
    json_codte_signed = fields.Text(copy=False)
    codte_dgii_message_ids = fields.Many2many('l10n_sv.dte.codte.message.detail', string='Contingency Documents')

    # ===== BUTTONS =====
    def action_gen_json(self):
        self.ensure_one()
        if self.json_file_name:
            raise ValidationError(_('Error XML file already generated and cannot be modified'))

        if not len(self.invoice_id.invoice_line_ids):
            raise ValidationError("Debe ir al menos una línea de pedido de venta.")

        if len(self.invoice_id.invoice_line_ids) == 0:
            # Order is amount == 0 and no lines in it,
            # let's not create an XML for it
            return False

        company_id = self.company_id
        if not company_id.l10n_sv_signer_route or not company_id.l10n_sv_mh_private_pass:
            raise UserError(_("Must be selected credentials to signer in a Company."))

        if not company_id.l10n_sv_economic_activity_ids:
            raise UserError(_("Not exist Economic Activity for this company."))

        cedoc = self._gen_dte_doc()
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(b"{")
        cedoc.export(file, 0, namespacedef_="", pretty_print=True)
        file.write(b'\n')
        file.close()
        return self.sign_doc(file.name)

    def sign_doc(self, filename):
        dte_name = self.name
        args = 'mv ' + filename
        args = args.split()
        signed_filename = "/tmp/{}.json".format(dte_name)
        args.append(signed_filename)
        subprocess.run(args)
        xml_f1 = open(signed_filename, 'r', encoding="utf-8")
        json_file1 = xml_f1.read()
        xml_f = open(signed_filename, 'rb')
        json_file = xml_f.read()
        hacienda_api = HaciendaApi(company_id=self.company_id)
        subprocess.call(['rm', '-f', signed_filename])
        json_encoded = bytes(json_file)
        json_dict = json.loads(json_file1)
        response_json = hacienda_api.generate_signature(json_dict)
        if response_json.get('status') == 'OK':
            signed_file = response_json.get('body')
            if signed_file:
                json_signed = signed_file
                _logger.info("##### DTE FIRMADO: " + signed_filename)

                self.write({"json_file": base64.b64encode(json_encoded),
                            "json_file_name": "{}.json".format(dte_name),
                            "json_signed": json_signed,
                            "l10n_sv_dte_send_state": 'signed_pending',
                            })

                if self.json_file and self.json_signed:
                    json_file1 = self._complete_json_file1(firmaElectronica=self.json_signed)
                    self.write({"json_file1": base64.b64encode(json_file1)})

                self._generate_barcode()

            else:
                raise UserError('Error al firmar. Compruebe las credenciales.')
        elif response_json.get('status') == 'ERROR':
            raise UserError(str(response_json.get('body')))

        xml_f.close()
        return True

    def action_send_to_hacienda(self):
        documents = self._l10n_sv_check_documents_for_send()
        for document in documents.filtered(lambda x: x.l10n_sv_dte_send_state == 'signed_pending'):
            document._send_to_hacienda()

    def action_request_state_to_hacienda(self):
        company_id = self.company_id
        if not company_id.l10n_sv_mh_auth_pass or not company_id.partner_id.nit:
            return

        hacienda_api = HaciendaApi(company_id=self.company_id)
        response = hacienda_api.consulta_dte(self)
        if response.status_code == 200:
            response_json = response.json()
            document_vals = {
                'l10n_sv_dte_send_state': DTE_STATE_MAP[response_json['estado']],
            }
            self.write(document_vals)
        elif response.status_code == 400:
            raise UserError(str(response.text))
        elif response.status_code == 404:
            raise UserError(str(response.text))

    def action_consultatrackids(self):
        company_id = self.company_id
        if not company_id.l10n_sv_mh_auth_pass or not company_id.partner_id.nit:
            return

        hacienda_api = HaciendaApi(company_id=company_id)
        response = hacienda_api.consulta_dte(self)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'sticky': True,
                'message': "%s" % response.text,
            }
        }

    def _complete_json_file1(self, **args):
        if not self.json_file1:
            json_dict = json.loads(base64.b64decode(self.json_file))
            json_new = json.dumps(json_dict, indent=4)
            json_file1 = json_new.encode("utf-8")
            self.write({"json_file1": base64.b64encode(json_file1)})

        bytes_result = base64.b64decode(self.json_file1)
        json_dict = json.loads(bytes_result)
        json_dict.update(args)
        json_new = json.dumps(json_dict, indent=4)
        json_file1 = json_new.encode("utf-8")
        return json_file1

    # def prueba_json(self):  # TODO: Eliminar esto.
    #     for rec in self:
    #         if not rec.json_file1:
    #             json_file1 = self._complete_json_file1(firmaElectronica=self.json_signed)
    #             self.write({"json_file1": base64.b64encode(json_file1),
    #                         })
    #
    #         aa = rec._complete_json_file1(selloRecibido=rec.l10n_sv_receipt_stamp)
    #         rec.write({"json_file1": base64.b64encode(aa)})

    # === BUSINESS METHODS ===#

    def _send_to_hacienda(self):
        if not self.json_file:
            self.action_gen_json()

        self.invoice_id._message_log(body=_("Sello Electronico: %s", self.invoice_id.l10n_sv_electronic_stamp))
        hacienda_api = HaciendaApi(company_id=self.company_id)
        response = hacienda_api.recepcion_dte(self)
        self.response_status_code = response.status_code
        if response.status_code == 200:
            response_json = response.json()
            json_file1 = self._complete_json_file1(selloRecibido=response_json['selloRecibido'])

            document_vals = {
                'l10n_sv_dte_send_state': DTE_STATE_MAP[response_json['estado']],
                'l10n_sv_receipt_stamp': response_json['selloRecibido'],
                'json_mr_file_name': 'MH_%s.json' % self.name,
                'json_mr_file': base64.b64encode((json.dumps(response_json)).encode('utf-8')),
                'message_detail': self._prepare_msg_DTE_vals(response_json),
                "json_file1": base64.b64encode(json_file1),
            }
            self.write(document_vals)
            self.invoice_id._message_log(body=_("Receipt Stamp: %s", response_json['selloRecibido']))
        elif response.status_code == 400:
            response_json = response.json()
            document_vals = {
                'l10n_sv_dte_send_state': DTE_STATE_MAP[response_json['estado']],
                'json_mr_file_name': 'MH_%s.json' % self.name,
                'json_mr_file': base64.b64encode((json.dumps(response_json)).encode('utf-8')),
                'message_detail': self._prepare_msg_DTE_vals(response_json),
            }
            self.write(document_vals)

    def _gen_dte_doc(self):
        """ Retorna el elemento raiz de un documento electronico.

            :returns: obj del tipo de documento electronico.
            """
        l10n_sv_voucher_type = self.l10n_sv_voucher_type_id.code
        if l10n_sv_voucher_type == '01':
            """Factura Electrónica"""
            classdoc = FE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.FacturaElectronica(identificacion=identification,
                                                emisor=sender,
                                                receptor=receiver,
                                                )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            return cedoc
        elif l10n_sv_voucher_type == '03':
            """Comprobante de Crédito Fiscal Electrónico"""
            classdoc = CCFE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.ComprobanteCreditoFiscalElectronico(identificacion=identification,
                                                                 emisor=sender,
                                                                 receptor=receiver,
                                                                 )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            return cedoc
        elif l10n_sv_voucher_type == '04':
            """Nota de Remisión Electrónica"""
            classdoc = NRE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.NotaRemisionElectronica(identificacion=identification,
                                                     emisor=sender,
                                                     receptor=receiver,
                                                     )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            self._add_related_document(cedoc, classdoc)
            return cedoc
        elif l10n_sv_voucher_type == '05':
            """Nota de Crédito Electrónica"""
            classdoc = NCE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.NotaCreditoElectronica(identificacion=identification,
                                                    emisor=sender,
                                                    receptor=receiver,
                                                    )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            self._add_related_document(cedoc, classdoc)
            return cedoc
        elif l10n_sv_voucher_type == '06':
            """Nota de Débito Electrónica"""
            classdoc = NDE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.NotaDebitoElectronica(identificacion=identification,
                                                   emisor=sender,
                                                   receptor=receiver,
                                                   )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            self._add_related_document(cedoc, classdoc)
            return cedoc
        elif l10n_sv_voucher_type == '07':
            """Comprobante de Retencion Electronico"""
            classdoc = CRE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.ComprobanteretencionElectronico(identificacion=identification,
                                                             emisor=sender,
                                                             receptor=receiver,
                                                             )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            return cedoc
        elif l10n_sv_voucher_type == '11':
            """Factura de Exportación"""
            classdoc = FEXE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.FacturaExportacion(identificacion=identification,
                                                emisor=sender,
                                                receptor=receiver,
                                                )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            return cedoc
        elif l10n_sv_voucher_type == '14':
            """Factura Sujeto Excluido Electrónico"""
            classdoc = FSEE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.FacturaSujetoExcluidoElectronico(identificacion=identification,
                                                              emisor=sender,
                                                              receptor=receiver,
                                                              )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            return cedoc
        elif l10n_sv_voucher_type == '15':
            """Comprobante de Donación Electrónica"""
            classdoc = CDE
            identification = self.get_identification(classdoc)
            sender = self.get_sender(classdoc)
            receiver = self.get_receiver(classdoc)
            cedoc = classdoc.ComprobanteDonacionElectronica(identificacion=identification,
                                                            emisor=sender,
                                                            receptor=receiver,
                                                            )

            if self.invoice_id:
                self._gen_body_document_and_summary(cedoc, classdoc)

            self._add_other_document(cedoc, classdoc)
            return cedoc
        else:
            pass

    def get_identification(self, classdoc):
        company_id = self.company_id
        env = '00' if company_id.l10n_sv_dte_mh_test_env else '01'
        create_date = self._str_to_datetime(self.date_issue)
        l10n_sv_voucher_type = self.l10n_sv_voucher_type_id.code
        identification = classdoc.Identificacion(version=DTE_VOUCHER_TYPE_VERSION_MAP[l10n_sv_voucher_type],
                                                 ambiente=env,
                                                 tipoDTE=l10n_sv_voucher_type,
                                                 numeroControl=self.name,
                                                 codigoGeneracion=self.l10n_sv_generation_code,
                                                 fecEmi=create_date.strftime(L10N_SV_DATE_FORMAT),
                                                 horEmi=create_date.strftime(L10N_SV_HOUR_FORMAT),
                                                 tipoModelo=1,
                                                 tipoOperacion=int(self.situation),
                                                 tipoMoneda=self.currency_id.name,
                                                 )
        # if self.situation == 2:
        #     # Contingency
        #     identification.set_tipoContingencia("1")
        #     identification.set_motivoContin("MH")

        return identification

    def get_sender(self, classdoc):
        """Retorna la instancia de un emisor

            :param object classdoc: Clase del tipo de documento.
            """

        l10n_sv_voucher_type = self.l10n_sv_voucher_type_id.code
        if not self.company_id.vat:
            raise ValidationError(_('Your company has not defined an RNC.'))
        if not self.company_id.name:
            raise ValidationError(_('Your company has not defined an Name.'))
        if not self.company_id.street or not len(str(self.company_id.street).strip()):
            action = self.env.ref("base.action_res_company_form")
            msg = _('Your company has not defined a street.')
            raise RedirectWarning(msg, action.id, _("Go to Companies"))

        partner_id = self.company_id.partner_id
        if not partner_id.nit:
            raise ValidationError(_('Your company has not defined an NIT.'))

        if self.company_id.country_id == self.env.ref("base.sv"):
            company_id = self.company_id
            if not partner_id.state_id:
                raise ValidationError(_('The province of company must be required.'))
            if company_id.state_id:
                if not partner_id.state_id.dte_code:
                    raise ValidationError('La Provincia seleccionada no tiene codigo para Hacienda, favor corregir!')
            if not partner_id.res_municipality_id:
                raise ValidationError(_('The municipality of company must be required.'))
            if partner_id.res_municipality_id:
                if not partner_id.res_municipality_id.dte_code:
                    raise ValidationError('El municipio seleccionada no tiene codigo para Hacienda, favor corregir!')

        if not partner_id.l10n_sv_identification_id:
            raise ValidationError(_('Your company has not defined an Identification Type.'))
        if l10n_sv_voucher_type != '14' and not partner_id.l10n_sv_commercial_name:
            raise ValidationError(_('Your company has not defined Commercial Name.'))

        address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                     municipio=partner_id.res_municipality_id.dte_code,
                                     complemento=partner_id.street,
                                     )
        sender = classdoc.Emisor(nrc=company_id.vat.replace("-", ""),
                                 nombre=self.limit(self.company_id.name, 150),
                                 codActividad=self.company_id.l10n_sv_economic_activity_ids[0].code,
                                 descActividad=self.limit(self.company_id.l10n_sv_economic_activity_ids[0].name, 150),
                                 telefono=self.company_id.phone or self.company_id.mobile,
                                 direccion=address,
                                 )

        if l10n_sv_voucher_type not in ['05', '06', '07']:
            sender.set_codEstable(self.l10n_sv_terminal_id.location_id.code)
            sender.set_codPuntoVenta(self.l10n_sv_terminal_id.code)
        if l10n_sv_voucher_type != '15':
            sender.set_nit(partner_id.nit.replace("-", ""))
        if l10n_sv_voucher_type != '14':
            sender.set_nombreComercial(self.limit(partner_id.l10n_sv_commercial_name or '', 150))
            sender.set_tipoEstablecimiento(self.company_id.l10n_sv_establishment_type)
        if l10n_sv_voucher_type == '11':
            if not self.invoice_id.l10n_sv_type_item_to_import:
                raise ValidationError('Debe definir el tipo de item a importar.')
            sender.set_tipoItemExpor(self.invoice_id.l10n_sv_type_item_to_import)
            if not self.invoice_id.l10n_sv_tax_precinct:
                raise ValidationError('Debe definir un recinto fiscal.')
            sender.set_recintoFiscal(self.invoice_id.l10n_sv_tax_precinct)
            if not self.invoice_id.l10n_sv_regime:
                raise ValidationError('Debe definir el régimen aduanero.')
            sender.set_regimen(self.invoice_id.l10n_sv_regime)
        if l10n_sv_voucher_type == '15':
            document_number = self.get_document_number(partner_id)
            sender.set_tipoDocumento(partner_id.l10n_sv_identification_id.code)
            sender.set_numDocumento(document_number)
        if not self.company_id.email:
            raise ValidationError(_('Your company has not defined an email which is mandatory'))
        if len(self.company_id.email) > 100:
            raise ValidationError("El correo de la empresa excede del Largo maximo %s" % 80)

        sender.set_correo(self.company_id.email)
        return sender

    def get_receiver(self, classdoc):
        """Logica y validaciones del comprador de tipo de documento.

            :param object classdoc: Clase del tipo de documento.
            :returns: obj del comprador del tipo de documento electronico.
            """

        if not self.partner_id:
            return None

        def validate_and_dpa():
            if self.partner_id.country_id == self.env.ref("base.sv"):
                if not partner_id.state_id:
                    raise ValidationError(_('The province of partner must be required.'))
                if self.partner_id.state_id:
                    if not self.partner_id.state_id.dte_code:
                        raise ValidationError('La Provincia seleccionada no tiene codigo para DGII, favor corregir!')
                if not partner_id.res_municipality_id:
                    raise ValidationError(_('The municipality of partner must be required.'))
                if self.partner_id.res_municipality_id:
                    if not self.partner_id.res_municipality_id.dte_code:
                        raise ValidationError('El municipio seleccionada no tiene codigo para DGII, favor corregir!')

        l10n_sv_voucher_type = self.l10n_sv_voucher_type_id.code
        partner_id = self.partner_id
        if l10n_sv_voucher_type == "01":
            """Factura Electrónica"""
            if not self.partner_id.name:
                raise ValidationError(_('The partner has not defined a name'))

            document_number = self.get_document_number(partner_id)
            receptor = classdoc.Receptor(nombre=self.limit(self.partner_id.name, 150),
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         numDocumento=document_number,
                                         )
            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            if address.get_departamento() and address.get_municipio() and address.get_complemento():
                receptor.set_direccion(address)
            if partner_id.phone or partner_id.mobile:
                receptor.set_telefono(partner_id.phone or partner_id.mobile)
            if partner_id.email:
                receptor.set_correo(partner_id.email)

            return receptor
        elif l10n_sv_voucher_type == "03":
            """Comprobante de Crédito Fiscal Electrónico"""

            if not partner_id.vat:
                raise ValidationError(_('Debe especificar VAT.'))
            if not partner_id.street or not len(str(partner_id.street).strip()):
                raise ValidationError(_('The contact has not defined a street.'))
            if not (partner_id.phone or partner_id.mobile):
                raise ValidationError(_('The contact has not defined a phone.'))
            if not partner_id.l10n_sv_activity_id:
                raise ValidationError('El contacto no tiene actividad económica definida.')
            if not partner_id.email:
                raise ValidationError(_('The contact has not defined an email which is mandatory'))

            validate_and_dpa()
            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            document_number = self.get_document_number(partner_id)
            receiver = classdoc.Receptor(nit=document_number,
                                         nrc=self.partner_id.vat.replace("-", ""),
                                         nombre=self.limit(self.partner_id.name, 150),
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         )
            return receiver
        elif l10n_sv_voucher_type == "04":
            """Nota de Remisión Electrónica"""

            if not partner_id.vat:
                raise ValidationError(_('Debe especificar VAT.'))

            document_number = self.get_document_number(partner_id)
            if not document_number:
                raise ValidationError(_('Debe especificar un numero de identificación.'))

            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            receiver = classdoc.Receptor(nrc=self.partner_id.vat.replace("-", ""),
                                         nombre=self.limit(self.partner_id.name, 150),
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         numDocumento=document_number,
                                         bienTitulo="12",
                                         )
            return receiver
        elif l10n_sv_voucher_type in ["05", "06"]:
            """Nota de Crédito"""

            if not partner_id.vat:
                raise ValidationError(_('Debe especificar VAT.'))
            if not partner_id.nit:
                raise ValidationError(_('Debe especificar NIT.'))

            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            document_number = self.get_document_number(partner_id)
            receiver = classdoc.Receptor(nit=document_number,
                                         nrc=self.partner_id.vat.replace("-", ""),
                                         nombre=self.limit(self.partner_id.name, 150),
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         )
            return receiver
        elif l10n_sv_voucher_type == "07":
            """Comprobante de Retencion Electronico"""

            if not partner_id.street or not len(str(partner_id.street).strip()):
                raise ValidationError(_('The contact has not defined a street.'))

            document_number = self.get_document_number(partner_id)
            if not document_number:
                raise ValidationError(_('Debe especificar un numero de identificación.'))

            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            receiver = classdoc.Receptor(nrc=self.partner_id.vat.replace("-", ""),
                                         nombre=self.limit(self.partner_id.name, 150),
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         numDocumento=document_number,
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         )
            return receiver
        elif l10n_sv_voucher_type == "11":
            """Factura de Exportación"""

            if not partner_id.country_id:
                raise ValidationError(_('The country of partner must be required.'))
            if not partner_id.country_id.dte_code:
                raise ValidationError('El pais del contacto no tiene codigo para Hacienda.')

            document_number = self.get_document_number(partner_id)
            if not document_number:
                raise ValidationError(_('Debe especificar un numero de identificación.'))

            receiver = classdoc.Receptor(nombre=self.limit(self.partner_id.name, 150),
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         numDocumento=document_number,
                                         codPais=partner_id.country_id.dte_code,
                                         nombrePais=partner_id.country_id.name,
                                         complemento=partner_id.street,
                                         tipoPersona=1,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         )
            return receiver
        elif l10n_sv_voucher_type == "14":
            """Factura Sujeto Excluido Electrónico"""

            document_number = self.get_document_number(partner_id)
            if not document_number:
                raise ValidationError(_('Debe especificar un numero de identificación.'))
            if not partner_id.street or not len(str(partner_id.street).strip()):
                raise ValidationError(_('The contact has not defined a street.'))

            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            receiver = classdoc.Receptor(nombre=self.limit(self.partner_id.name, 150),
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         numDocumento=document_number,
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         )
            return receiver
        elif l10n_sv_voucher_type == "15":
            """Comprobante de Donación Electrónica"""

            document_number = self.get_document_number(partner_id)
            if not document_number:
                raise ValidationError(_('Debe especificar un numero de identificación.'))

            address = classdoc.Direccion(departamento=partner_id.state_id.dte_code,
                                         municipio=partner_id.res_municipality_id.dte_code,
                                         complemento=partner_id.street,
                                         )
            receiver = classdoc.Receptor(nombre=self.limit(self.partner_id.name, 150),
                                         tipoDocumento=partner_id.l10n_sv_identification_id.code,
                                         nrc=self.partner_id.vat,
                                         numDocumento=document_number,
                                         codActividad=partner_id.l10n_sv_activity_id.code,
                                         descActividad=partner_id.l10n_sv_activity_id.name,
                                         telefono=partner_id.phone or partner_id.mobile,
                                         correo=partner_id.email,
                                         direccion=address,
                                         codDomiciliado="1",
                                         codPais=partner_id.country_id.code,
                                         )
            return receiver
        else:
            return None

    def _construct_tax_excluded(self, price_with_taxes, amount_tax):
        """ Only used por FE """
        self.ensure_one()
        price_wo_taxes = price_with_taxes / (1 + amount_tax / 100)
        tax = price_with_taxes - price_wo_taxes
        return price_wo_taxes, tax

    def _construct_tax_excluded1(self, price, line):
        res = line.tax_ids.compute_all(price, product=line.product_id, partner=self.env['res.partner'])
        excluded = res['total_excluded']
        return excluded

    def _construct_tax_included(self, price, line):
        """ Only used por FE """
        taxes = line.tax_ids.filtered(lambda t: not t.tax_group_id.l10n_sv_billing_indicator)

        res = taxes.compute_all(price, product=line.product_id, partner=self.env['res.partner'])
        excluded = res['total_included']
        return excluded

    def _iterable_products_xml(self, lines):
        self.ensure_one()
        return lines

    def _gen_body_document_and_summary(self, cedoc, classdoc):
        """Product lines related values

        :param object cedoc: Instancia u objeto del Elemento raiz.
        :param object classdoc: Clase del tipo de documento.

        :returns: tuple (response, vals)
        """

        invoice = self.invoice_id
        body_document = classdoc.CuerpoDocumento()
        if self.l10n_sv_voucher_type_id.code not in ['01', '15']:
            tributes = classdoc.Tributos()

        tax_data = self.get_taxed_amount_data()
        total_taxed = sum(
            [
                tax_data["13_taxed_base"],
                tax_data["exempt_amount"],
            ]
        )
        # total_amount = sum(
        #     [
        #         tax_data["13_taxed_amount"],
        #         tax_data["0_taxed_amount"],
        #     ]
        # )
        # is_company_currency = self.is_company_currency()

        lines = self.invoice_id.invoice_line_ids
        if self.l10n_sv_voucher_type_id.code not in ['07']:
            for i, line in enumerate(
                    self._iterable_products_xml(lines).filtered(lambda l: (l.display_type == 'product'
                                                                           and l.quantity)).sorted(
                        "sequence"
                    ),
                    1,
            ):
                product_id = line.product_id
                product_name = product_id.name if product_id else (line.name or "S/N")
                quantity = abs(line.quantity)
                price_unit_untaxed = self._construct_tax_excluded1(line.price_unit, line)
                item = classdoc.Item(
                    numItem=i,
                    descripcion=self.limit(product_name, 80),
                    cantidad=quantity,
                )

                if self.l10n_sv_voucher_type_id.code in ['01']:
                    item.set_precioUni(line.price_total / line.quantity)
                elif self.l10n_sv_voucher_type_id.code not in ['15']:
                    item.set_precioUni(line.price_subtotal / line.quantity)
                elif self.l10n_sv_voucher_type_id.code in ['15']:
                    item.set_valorUni(price_unit_untaxed)
                    item.set_valor(price_unit_untaxed * item.get_cantidad())
                    item.set_depreciacion(0)

                if self.l10n_sv_voucher_type_id.code == '14':
                    item.set_compra(price_unit_untaxed * quantity)

                item_type = (2
                             if (product_id and product_id.type == "service")
                             else 1)
                if self.l10n_sv_voucher_type_id.code not in ['11', '15']:
                    item.set_tipoItem(item_type)
                if product_id.default_code:
                    item.set_codigo(self.limit(product_id.default_code, 20))

                if line.product_uom_id:
                    if not line.product_uom_id.dte_code:
                        raise ValidationError('La unidad de medida no tiene codigo para Hacienda.')
                    item.set_uniMedida(int(line.product_uom_id.dte_code))
                else:
                    item.set_uniMedida(59)

                if self.l10n_sv_voucher_type_id.code in ['04', '05', '06']:
                    item.set_numeroDocumento(self.invoice_id.l10n_sv_generation_code_ref)

                taxes = line.tax_ids

                # if not all([tax.l10n_sv_code for tax in taxes]):
                #     raise ValidationError(
                #         'Por favor configure los campos código para los impuesto.'
                #     )

                for t in taxes:
                    if self.l10n_sv_voucher_type_id.code not in ['01', '14', '15']:
                        item.add_tributos(t.l10n_sv_code)
                    if self.l10n_sv_voucher_type_id.code == '01':
                        item.set_ivaItem(line.price_total - line.price_subtotal)

                discount_amount = 0.00
                if line.discount > 0:
                    discount_amount = price_unit_untaxed * line.quantity * line.discount / 100
                    item.set_montoDescu(abs(discount_amount))

                if self.l10n_sv_voucher_type_id.code in ['01']:
                    base_line = abs(line.price_total)
                else:
                    base_line = abs(line.price_subtotal)

                subtotal_line = base_line - discount_amount

                if self.l10n_sv_voucher_type_id.code in ['01']:
                    if not item.get_ivaItem():
                        item.set_ventaExenta(subtotal_line)
                    else:
                        item.set_ventaGravada(subtotal_line)
                elif self.l10n_sv_voucher_type_id.code not in ['14', '15'] and not item.get_tributos():
                    item.set_ventaExenta(subtotal_line)
                elif self.l10n_sv_voucher_type_id.code not in ['14', '15'] and item.get_tributos():
                    item.set_ventaGravada(subtotal_line)
                if self.l10n_sv_voucher_type_id.code == '15':
                    item.set_tipoDonacion(int(product_id.l10n_sv_donation_type or 1))

                body_document.add_Item(item)
        else:
            self._gen_body_document_retention(cedoc, classdoc, body_document)

        cedoc.set_cuerpoDocumento(body_document)
        summary = classdoc.Resumen()

        if self.invoice_id.l10n_sv_voucher_type_id.code not in ['07']:
            summary.set_totalLetras(invoice.amount_total_words)
        else:
            summary.set_totalIVAretenidoLetras(invoice.amount_total_words)

        if self.invoice_id.l10n_sv_voucher_type_id.code not in ['07', '15']:
            summary.set_condicionOperacion(self.get_payment_type())

        if self.invoice_id.l10n_sv_voucher_type_id.code in ['01']:
            total_iva = 0.00
            for item in cedoc.get_cuerpoDocumento().get_Item():
                total_iva += item.get_ivaItem()

            summary.set_totalIva(abs(total_iva))

        if self.invoice_id.l10n_sv_voucher_type_id.code not in ['11', '14', '15'] and tax_data["exempt_amount"]:
            summary.set_totalExenta(abs(tax_data["exempt_amount"]))
        if tax_data["iva_withholding_amount"] and self.invoice_id.l10n_sv_voucher_type_id.code not in ['07', '14']:
            summary.set_ivaRete1(abs(tax_data["iva_withholding_amount"]))
        elif self.invoice_id.l10n_sv_voucher_type_id.code == '14':
            summary.set_reteRenta(abs(tax_data["iva_withholding_amount"]))
        elif self.invoice_id.l10n_sv_voucher_type_id.code == '07':
            summary.set_totalSujetoRetencion(abs(self.invoice_id.amount_untaxed_signed))
            summary.set_totalIVAretenido(abs(tax_data["iva_withholding_amount"]))

        if self.l10n_sv_voucher_type_id.code not in ['07'] and discount_amount:
            summary.set_totalDescu(abs(discount_amount))

        self.set_summary_additional_vals(summary, cedoc, classdoc)

        if total_taxed and self.invoice_id.l10n_sv_voucher_type_id.code in ['01']:
            total_subtotal = 0.00
            for item in cedoc.get_cuerpoDocumento().get_Item():
                total_subtotal += item.get_precioUni() * item.get_cantidad() - item.get_montoDescu()
            summary.set_totalGravada(abs(total_subtotal) - summary.get_totalExenta())
            summary.set_subTotalVentas(abs(total_subtotal))
            summary.set_subTotal(abs(total_subtotal))
            summary.set_montoTotalOperacion(abs(total_subtotal))
            summary.set_totalPagar(abs(total_subtotal) - summary.get_ivaRete1())
        else:
            if self.invoice_id.l10n_sv_voucher_type_id.code not in ['14', '15']:
                if self.invoice_id.l10n_sv_voucher_type_id.code == '11':
                    summary.set_totalGravada(abs(self.invoice_id.amount_untaxed_signed))
                elif self.invoice_id.l10n_sv_voucher_type_id.code != '07':
                    summary.set_totalGravada(abs(self.invoice_id.amount_untaxed_signed) - summary.get_totalExenta())
            if self.invoice_id.l10n_sv_voucher_type_id.code not in ['07', '11', '14', '15']:
                summary.set_subTotalVentas(abs(self.invoice_id.amount_untaxed_signed))
                summary.set_subTotal(abs(self.invoice_id.amount_untaxed_signed))
            if self.invoice_id.l10n_sv_voucher_type_id.code not in ['14', '15']:
                if self.invoice_id.l10n_sv_voucher_type_id.code == '11':
                    summary.set_montoTotalOperacion(abs(self.invoice_id.amount_total_signed))
                elif self.invoice_id.l10n_sv_voucher_type_id.code not in ['04', '07']:
                    summary.set_montoTotalOperacion(abs(self.invoice_id.amount_total_signed) + summary.get_ivaRete1())
                elif self.invoice_id.l10n_sv_voucher_type_id.code in ['04']:
                    summary.set_montoTotalOperacion(abs(self.invoice_id.amount_total_signed))
            if self.invoice_id.l10n_sv_voucher_type_id.code == '14':
                summary.set_totalCompra(abs(self.invoice_id.amount_total_signed) + summary.get_reteRenta())
                summary.set_subTotal(abs(self.invoice_id.amount_untaxed_signed))
            if self.invoice_id.l10n_sv_voucher_type_id.code not in ['04', '05', '06', '07', '15']:
                summary.set_totalPagar(abs(self.invoice_id.amount_total_signed))
            if self.invoice_id.l10n_sv_voucher_type_id.code in ['15']:
                summary.set_valorTotal(abs(self.invoice_id.amount_total_signed))
                exist_donation_cash = any([item.get_tipoDonacion() == 1 for item in cedoc.get_cuerpoDocumento().get_Item()])
                if exist_donation_cash:
                    pagos = classdoc.Pagos()
                    pago = classdoc.Pago(codigo="01",
                                         montoPago=summary.get_valorTotal(),
                                         )
                    pagos.add_Item(pago)
                    summary.set_pagos(pagos)

        if self.invoice_id.l10n_sv_voucher_type_id.code in ['11']:
            if not self.invoice_id.invoice_incoterm_id:
                raise ValidationError('No esta establecido el incoterm.')

            if not self.invoice_id.invoice_incoterm_id.code_dgii:
                raise ValidationError('El incoterm no tiene codigo establecido.')
            summary.set_codIncoterms(self.invoice_id.invoice_incoterm_id.code_dgii)
            summary.set_descIncoterms(self.invoice_id.invoice_incoterm_id.name)

        if self.l10n_sv_voucher_type_id.code not in ['01', '07', '11', '14', '15']:
            tax_info = defaultdict(dict)
            for tri in cedoc.get_cuerpoDocumento().get_Item():
                for tt in tri.get_tributos():
                    if tt not in tax_info:
                        tax_info[tt]['descripcion'] = ''
                        tax_info[tt]['valor'] = 0.00

                    account_tax = self.env["account.tax"].search([("l10n_sv_code", "=", tt)], limit=1)
                    value = round((tri.get_precioUni() * tri.get_cantidad() - tri.get_montoDescu()) * account_tax.amount / 100, 2)
                    tax_info[tt]['descripcion'] = SV_TAXES[account_tax.l10n_sv_code]
                    tax_info[tt]['valor'] += value

            for tt in tax_info:
                tribute = classdoc.Tributo(codigo=tt,
                                          descripcion=tax_info[tt]['descripcion'],
                                          valor=tax_info[tt]['valor'])
                tributes.add_Item(tribute)
            summary.set_tributos(tributes)

        cedoc.set_resumen(summary)

    def _gen_body_document_retention(self, cedoc, classdoc, body_document):
        lines = self.invoice_id.invoice_line_ids
        for i, line in enumerate(
                self._iterable_products_xml(lines).filtered(
                    lambda l: l.display_type == 'product' and l.quantity).sorted(
                    "sequence"
                ),
                1,
        ):
            product_id = line.product_id
            product_name = product_id.name if product_id else (line.name or "S/N")
            item = classdoc.Item(
                numItem=i,
                descripcion=self.limit(product_name, 80),
            )

            item.set_tipoDte("03")
            item.set_tipoDoc(1)
            document_number = self.get_document_number(self.partner_id)
            item.set_numDocumento(document_number)
            item.set_fechaEmision(self.invoice_id.create_date.strftime('%Y-%m-%d'))
            withholding_vals = self._get_item_withholding_vals(line)
            if withholding_vals["1_taxed_base"] or withholding_vals["1_taxed_amount"]:
                item.set_codigoRetencionMH('22')
                item.set_montoSujetoGrav(withholding_vals["1_taxed_base"])
                item.set_ivaRetenido(abs(withholding_vals["1_taxed_amount"]))
            elif withholding_vals["13_taxed_base"] or withholding_vals["13_taxed_amount"]:
                item.set_codigoRetencionMH('C4')
                item.set_montoSujetoGrav(withholding_vals["13_taxed_base"])
                item.set_ivaRetenido(abs(withholding_vals["13_taxed_amount"]))

            body_document.add_Item(item)

    def _get_item_withholding_vals(self, invoice_line):
        """ Returns invoice line withholding taxes values """

        iva_data = {
            "1_taxed_base": 0,
            "1_taxed_amount": 0,
            "13_taxed_base": 0,
            "13_taxed_amount": 0,
        }

        line_withholding_vals = invoice_line.tax_ids.compute_all(
            price_unit=invoice_line.price_unit,
            currency=invoice_line.currency_id,
            quantity=invoice_line.quantity,
            product=invoice_line.product_id,
            partner=invoice_line.move_id.partner_id,
            is_refund=True if invoice_line.move_id.move_type == "in_refund" else False,
        )

        for tax in line_withholding_vals["taxes"]:
            tax_id = self.env["account.tax"].browse(tax["id"])
            if tax_id.amount < 0 and tax_id.tax_group_id.l10n_sv_billing_indicator == "taxable":
                iva_data["1_taxed_base"] += tax["base"]
                iva_data["1_taxed_amount"] += tax["amount"]
            elif tax_id.amount < 0 and tax_id.tax_group_id.l10n_sv_billing_indicator == "taxable13":
                iva_data["13_taxed_base"] += tax["base"]
                iva_data["13_taxed_amount"] += tax["amount"]

        # withholding_vals = OrderedDict()
        # withhold_iva_1_base = abs(
        #     sum(
        #         tax["base"]
        #         for tax in line_withholding_vals["taxes"]
        #         if tax["amount"] < 0
        #         and self.env["account.tax"].browse(tax["id"]).tax_group_id.l10n_sv_billing_indicator == "taxable"
        #     )
        # )
        # withhold_iva_1_amount = abs(
        #     sum(
        #         tax["amount"]
        #         for tax in line_withholding_vals["taxes"]
        #         if tax["amount"] < 0
        #         and self.env["account.tax"].browse(tax["id"]).tax_group_id.l10n_sv_billing_indicator == "taxable"
        #     )
        # )
        #
        # # withholding_vals["MontoISRRetenido"] = itbis_withhold_amount
        # if withhold_iva_1_base:
        #     withholding_vals["montoSujetoGrav"] = withhold_iva_1_base
        # if withhold_iva_1_amount:
        #     withholding_vals["ivaRetenido"] = withhold_iva_1_amount
        # return withholding_vals
        return iva_data

    def set_summary_additional_vals(self, *args):
        """Set additional values to the summary.
        """
        pass

    def _add_related_document(self, cedoc, classdoc):
        """Informacion Referencia

                :param object cedoc: Instancia del Elemento raiz.
                :param object classdoc: Clase del tipo de documento.

                :returns: object cedoc
                """

        info_reference = classdoc.DocumentosRelacionado()
        related_doc = classdoc.DocumentoRelacionado()
        if self.invoice_id.l10n_sv_generation_code_ref:
            related_doc.set_numeroDocumento(self.invoice_id.l10n_sv_generation_code_ref)
        elif self.invoice_id.debit_origin_id.l10_sv_dte_id.l10n_sv_generation_code:
            generation_code_origin = self.invoice_id.debit_origin_id.l10_sv_dte_id.l10n_sv_generation_code
            related_doc.set_numeroDocumento(generation_code_origin)

        related_doc.set_tipoDocumento('03')
        related_doc.set_tipoGeneracion(int(self.invoice_id.l10n_sv_generation_type_ref or 1))
        related_doc.set_fechaEmision(self.invoice_id.l10n_sv_date_issue_ref.strftime('%Y-%m-%d'))
        info_reference.add_documentoRelacionado(related_doc)
        cedoc.set_documentoRelacionado(info_reference)

    def _add_other_document(self, cedoc, classdoc):
        """Other Documents

                :param object cedoc: Instancia del Elemento raiz.
                :param object classdoc: Clase del tipo de documento.

                :returns: object cedoc
                """

        others_document = classdoc.OtrosDocumentos()
        item = classdoc.OtroDocumento(codDocAsociado=1, descDocumento="Resoluciones", detalleDocumento="00000")
        others_document.add_Item(item)
        cedoc.set_otrosDocumentos(others_document)

    def _generate_barcode(self):
        env = '00' if self.company_id.l10n_sv_dte_mh_test_env else '01'
        url_params = {
            "ambiente": env,
            "codGen": self.l10n_sv_generation_code,
            "fechaEmi": self.date_issue.strftime('%Y-%m-%d'),
        }
        api_url = f'https://admin.factura.gob.sv/consultaPublica?{urls.url_encode(url_params)}'
        qr_code = pyqrcode.create(api_url)
        self.write({"l10n_sv_qr_code": qr_code.png_as_base64_str(scale=2),
                    "l10n_sv_electronic_stamp": api_url,
                    })

    def get_taxed_amount_data(self):
        """IVA taxed amount

        13% -- Most common
        0% -- Should be used on exported products

        """

        iva_data = {
            "total_taxed_amount": 0,
            "13_taxed_base": 0,
            "13_taxed_amount": 0,
            "0_taxed_base": 0,
            "0_taxed_amount": 0,
            "iva_withholding_amount": 0,
            "exempt_amount": 0,
            "tax_additional": 0,
        }

        tax_data = [
            line.tax_ids.compute_all(
                price_unit=line.price_subtotal,
                currency=line.currency_id,
                product=line.product_id,
                partner=line.move_id.partner_id,
                handle_price_include=True,
            )
            for line in self._iterable_products_xml(self.invoice_id.invoice_line_ids)
        ]

        iva_data["total_taxed_amount"] = sum(
            line["total_excluded"] for line in tax_data
        )
        for line_taxes in tax_data:
            for tax in line_taxes["taxes"]:
                if not tax["amount"]:
                    iva_data["exempt_amount"] += tax["base"]

                tax_id = self.env["account.tax"].browse(tax["id"])
                if tax_id.amount == 13:
                    iva_data["13_taxed_base"] += tax["base"]
                    iva_data["13_taxed_amount"] += tax["amount"]
                elif tax_id.amount == 0:
                    iva_data["0_taxed_base"] += tax["base"]
                    iva_data["0_taxed_amount"] += tax["amount"]
                elif tax_id.amount < 0 and tax_id.tax_group_id.l10n_sv_billing_indicator in ["taxable", "taxable10", "taxable13"]:
                    iva_data["iva_withholding_amount"] += tax["amount"]

            # Taxes exempt by omission.
            if not line_taxes["taxes"]:
                iva_data["exempt_amount"] += line_taxes["total_excluded"]

        return iva_data

    def get_payment_type(self):
        """
        Indicates the type of customer payment. Free delivery invoices (code 3)
        are not valid for Crédito Fiscal.

        1 - Al Contado
        2 - Crédito
        3 - Otros
        """
        if not self.invoice_id.invoice_payment_term_id and self.invoice_id.invoice_date_due:
            if (
                    self.invoice_id.invoice_date_due and self.invoice_id.invoice_date
            ) and self.invoice_id.invoice_date_due > self.invoice_id.invoice_date:
                return 2
            else:
                return 1
        elif not self.invoice_id.invoice_payment_term_id:
            return 1
        elif not self.invoice_id.invoice_payment_term_id == self.env.ref(
                "account.account_payment_term_immediate"
        ):
            return 2
        else:
            return 1

    def _prepare_msg_DTE_vals(self, data_dict):
        message = ("version: " + str(data_dict.get("version")) + "\n" +
                   "ambiente: " + str(data_dict.get("ambiente")) + "\n" +
                   "versionApp: " + str(data_dict.get("versionApp")) + "\n" +
                   "estado: " + data_dict.get("estado") + "\n" +
                   "codigoGeneracion: " + str(data_dict.get("codigoGeneracion")) + "\n" +
                   "selloRecibido: " + str(data_dict.get("selloRecibido")) + "\n" +
                   "fhProcesamiento: " + str(data_dict.get("fhProcesamiento")) + "\n" +
                   "clasificaMsg: " + str(data_dict.get("clasificaMsg")) + "\n" +
                   "codigoMsg: " + str(data_dict.get("codigoMsg")) + "\n" +
                   "descripcionMsg: " + str(data_dict.get("descripcionMsg")) + "\n" +
                   "observaciones: " + json.dumps(data_dict.get("observaciones"), ensure_ascii=False))
        return message

    # Annulation

    def action_annul_dte(self, **additional_values):
        company_id = self.company_id
        if not company_id.l10n_sv_mh_auth_pass or not company_id.partner_id.nit:
            return

        self.write({**dict(additional_values)})
        andte_doc = self._gen_annulation_doc()
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(b"{")
        andte_doc.export(file, 0, namespacedef_="", pretty_print=True)
        file.write(b'\n')
        file.close()
        json_name = "{}.json".format("AN" + self.name)
        args = 'mv ' + file.name
        args = args.split()
        signed_filename = "/tmp/" + json_name
        args.append(signed_filename)
        subprocess.run(args)
        xml_f1 = open(signed_filename, 'r', encoding="utf-8")
        json_file1 = xml_f1.read()
        xml_f = open(signed_filename, 'rb')
        json_file = xml_f.read()
        json_encoded = bytes(json_file)
        self.write({"json_andte_file": base64.b64encode(json_encoded),
                    "json_andte_file_name": json_name,
                    })

        xml_f.close()
        hacienda_api = HaciendaApi(company_id=self.company_id)
        json_dict = json.loads(json_file1)
        response_json = hacienda_api.generate_signature(json_dict)
        if response_json.get('status') == 'OK':
            signed_file = response_json.get('body')
            if signed_file:
                json_signed = signed_file
                _logger.info("##### ANDTE FIRMADO: " + signed_filename)
                self.write({"json_andte_signed": json_signed,
                            })

        response = hacienda_api.anular_dte(self)
        if response.status_code == 200:
            response_json = response.json()
            self.write({'l10n_sv_dte_send_state': "invalidated"})
            self.invoice_id._message_log(body=_("Invalidate Stamp: %s", response_json['selloRecibido']))
            return True
        elif response.status_code == 400:
            response_json = response.json()
            document_vals = {"andte_dgii_message_ids": [(0, False, {
                'version': response_json.get("version"),
                'ambiente': response_json.get("ambiente"),
                'versionApp': response_json.get("versionApp"),
                'estado': response_json.get("estado"),
                'fhProcesamiento': json.dumps(response_json.get("fhProcesamiento")),
                'descripcionMsg': json.dumps(response_json.get("descripcionMsg")),
                'observaciones': json.dumps(response_json.get("observaciones")),
            })]}
            self.write(document_vals)
            return False
        return True

    def _gen_annulation_doc(self):
        """
            :returns: obj InvalidacionDTE.
            """

        def get_document(classdoc):
            """
                """
            document_number = self.get_document_number(self.partner_id)
            l10n_sv_voucher_type = self.l10n_sv_voucher_type_id.code
            document = classdoc.Documento(tipoDte=l10n_sv_voucher_type,
                                          codigoGeneracion=self.l10n_sv_generation_code,
                                          selloRecibido=self.l10n_sv_receipt_stamp,
                                          numeroControl=self.name,
                                          fecEmi=self.date_issue.strftime(L10N_SV_DATE_FORMAT),
                                          tipoDocumento=self.partner_id.l10n_sv_identification_id.code,
                                          numDocumento=document_number,
                                          nombre=self.partner_id.name,
                                          telefono=self.partner_id.mobile or self.partner_id.phone,
                                          correo=self.partner_id.email,
                                          )
            return document

        company_id = self.company_id
        partner_id = self.company_id.partner_id
        invoice_user_id = (
                        self.invoice_id.l10n_sv_responsible_annulation_id
                        or self.invoice_id.partner_id.user_id
                        or self.env.user
                        )

        invoice_partner_id = invoice_user_id.partner_id
        if not invoice_partner_id.l10n_sv_identification_id:
            raise ValidationError(_('The Salesperson has not defined an identification type.'))
        invoice_partner_document_number = self.get_document_number(invoice_partner_id)
        if not invoice_partner_document_number:
            raise ValidationError(_('The Salesperson has not defined an identification number.'))

        env = '00' if company_id.l10n_sv_dte_mh_test_env else '01'
        now = datetime.now(pytz.timezone('America/El_Salvador'))
        now = now.replace(microsecond=0)
        classdoc = ANDTE
        identification = classdoc.Identificacion(version=2,
                                                 ambiente=env,
                                                 codigoGeneracion=self.invoice_id.l10n_sv_generate_uuid(),
                                                 fecAnula=now.strftime(L10N_SV_DATE_FORMAT),
                                                 horAnula=now.strftime(L10N_SV_HOUR_FORMAT),
                                                 )
        sender = classdoc.Emisor(nit=partner_id.nit,
                                 nombre=self.limit(self.company_id.name, 150),
                                 tipoEstablecimiento=self.company_id.l10n_sv_establishment_type,
                                 nomEstablecimiento=self.l10n_sv_terminal_id.location_id.name,
                                 codEstable=self.l10n_sv_terminal_id.location_id.code,
                                 codPuntoVenta=self.l10n_sv_terminal_id.code,
                                 telefono=self.company_id.phone or self.company_id.mobile,
                                 correo=self.company_id.email,
                                 )
        document = get_document(classdoc)
        reason = classdoc.Motivo(tipoAnulacion=int(self.l10n_sv_cancellation_type),
                                 motivoAnulacion=self.l10n_sv_cancellation_reason,
                                 nombreResponsable=invoice_user_id.name,
                                 tipDocResponsable=invoice_partner_id.l10n_sv_identification_id.code,
                                 numDocResponsable=invoice_partner_document_number,
                                 nombreSolicita=invoice_user_id.name,
                                 tipDocSolicita=invoice_partner_id.l10n_sv_identification_id.code,
                                 numDocSolicita=invoice_partner_document_number,
                                 )
        andte_doc = classdoc.InvalidacionDTE(identificacion=identification,
                                             emisor=sender,
                                             documento=document,
                                             motivo=reason,
                                             )

        return andte_doc

    # Contingency

    def action_send_contingency(self, **additional_values):
        company_id = self.company_id
        if not company_id.l10n_sv_mh_auth_pass or not company_id.partner_id.nit:
            return

        codte_doc = self._gen_contingency_doc()
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(b"{")
        codte_doc.export(file, 0, namespacedef_="", pretty_print=True)
        file.write(b'\n')
        file.close()
        json_name = "{}.json".format(self.name)
        args = 'mv ' + file.name
        args = args.split()
        signed_filename = "/tmp/" + json_name
        args.append(signed_filename)
        subprocess.run(args)
        xml_f1 = open(signed_filename, 'r', encoding="utf-8")
        json_file1 = xml_f1.read()
        xml_f = open(signed_filename, 'rb')
        json_file = xml_f.read()
        json_encoded = bytes(json_file)
        self.write({"json_codte_file": base64.b64encode(json_encoded),
                    "json_codte_file_name": json_name,
                    })
        xml_f.close()
        hacienda_api = HaciendaApi(company_id=self.company_id)
        json_dict = json.loads(json_file1)
        response_json = hacienda_api.generate_signature(json_dict)
        if response_json.get('status') == 'OK':
            signed_file = response_json.get('body')
            if signed_file:
                json_signed = signed_file
                _logger.info("##### CODTE FIRMADO: " + signed_filename)
                self.write({"json_codte_signed": json_signed,
                            })

        response = hacienda_api.contingency_dte(self)
        if response.status_code == 200:
            self.write({**dict(additional_values)})
            return True
        elif response.status_code == 400:
            response_json = response.json()
            document_vals = {"codte_dgii_message_ids": [(0, False, {
                'estado': response_json.get("estado"),
                'fechaHora': json.dumps(response_json.get("fechaHora")),
                'mensaje': json.dumps(response_json.get("mensaje")),
                'observaciones': json.dumps(response_json.get("observaciones")),
            })]}
            self.write(document_vals)
            return False
        return True

    def _gen_contingency_doc(self):
        """
            :returns: obj ContingenciaDTE.
            """

        def get_detail_dte(classdoc):
            """
                """
            body_document = classdoc.DetalleDTE()
            lines = self.invoice_id.invoice_line_ids
            if self.l10n_sv_voucher_type_id.code not in ['07']:
                for i, line in enumerate(
                        self._iterable_products_xml(lines).filtered(
                            lambda l: l.display_type == 'product' and l.quantity).sorted(
                            "sequence"
                        ),
                        1,
                ):
                    item = classdoc.Item(
                        noItem=i,
                        codigoGeneracion=self.l10n_sv_generation_code,
                        tipoDoc=self.l10n_sv_voucher_type_id.code,
                    )
                    body_document.add_Item(item)

            return body_document

        company_id = self.company_id
        partner_id = self.company_id.partner_id
        if self.invoice_id.move_type in ('out_invoice', 'out_refund', 'out_receipt'):
            invoice_user_id = self.invoice_id.invoice_user_id
        else:
            invoice_user_id = self.invoice_id.create_uid
        invoice_partner_id = invoice_user_id.partner_id
        if not invoice_partner_id.l10n_sv_identification_id:
            raise ValidationError(_('The Salesperson has not defined an identification type.'))

        invoice_partner_document_number = self.get_document_number(invoice_partner_id)
        if not invoice_partner_document_number:
            raise ValidationError(_('The Salesperson has not defined an identification number.'))
        env = '00' if company_id.l10n_sv_dte_mh_test_env else '01'
        now = datetime.now(pytz.timezone('America/El_Salvador'))
        now = now.replace(microsecond=0)
        classdoc = CODTE
        identification = classdoc.Identificacion(version=3,
                                                 ambiente=env,
                                                 codigoGeneracion=self.invoice_id.l10n_sv_generate_uuid(),
                                                 fTransmision=now.strftime(L10N_SV_DATE_FORMAT),
                                                 hTransmision=now.strftime(L10N_SV_HOUR_FORMAT),
                                                 )
        sender = classdoc.Emisor(nit=partner_id.nit,
                                 nombre=self.limit(self.company_id.name, 150),
                                 tipoEstablecimiento=self.company_id.l10n_sv_establishment_type,
                                 nomEstablecimiento=self.l10n_sv_terminal_id.location_id.name,
                                 nombreResponsable=invoice_user_id.name,
                                 tipoDocResponsable=invoice_partner_id.l10n_sv_identification_id.code,
                                 numeroDocResponsable=invoice_partner_document_number,
                                 codEstable=self.l10n_sv_terminal_id.location_id.code,
                                 codPuntoVenta=self.l10n_sv_terminal_id.code,
                                 telefono=self.company_id.phone or self.company_id.mobile,
                                 correo=self.company_id.email,
                                 )
        detail = get_detail_dte(classdoc)
        reason = classdoc.Motivo(tipoContingencia=1,
                                 hFin=now.strftime(L10N_SV_HOUR_FORMAT),
                                 hInicio=now.strftime(L10N_SV_HOUR_FORMAT),
                                 fInicio=now.strftime(L10N_SV_DATE_FORMAT),
                                 fFin=now.strftime(L10N_SV_DATE_FORMAT),
                                 motivoContingencia="ERROR MH",
                                 )
        codte_doc = classdoc.ContingenciaDTE(identificacion=identification,
                                             emisor=sender,
                                             detalleDTE=detail,
                                             motivo=reason,
                                             )

        return codte_doc

    def get_document_number(self, partner_id):
        document_number = False
        if not partner_id.l10n_sv_identification_id:
            return document_number

        if partner_id.l10n_sv_identification_code == '36':
            document_number = partner_id.nit
        elif partner_id.l10n_sv_identification_code == '13':
            document_number = partner_id.dui
        elif partner_id.l10n_sv_identification_code == '02':
            document_number = partner_id.residential_card
        elif partner_id.l10n_sv_identification_code == '04':
            document_number = partner_id.passport
        elif partner_id.l10n_sv_identification_code == '37':
            document_number = partner_id.other

        return document_number.replace("-", "") if document_number else False

    def is_l10n_sv_partner(self):
        return self.partner_id.country_id and self.partner_id.country_id == self.env.ref("base.sv")

    def is_company_currency(self):
        return self.currency_id == self.company_id.currency_id

    @staticmethod
    def limit(literal, limit):
        return (literal[:limit - 3] + '...') if len(literal) > limit else literal

    @staticmethod
    def _str_to_datetime(date):
        tz_cr = pytz.timezone("America/El_Salvador")
        hora_actual = datetime.now(tz_cr).time()
        dt = datetime.combine(date, hora_actual)
        return tz_cr.localize(dt)

    def _l10n_sv_check_documents_for_send(self):
        """ Ensure the current records are eligible for sent to Hacienda.

                """
        failed_documents = self.filtered(
            lambda o: (not o.company_id.l10n_sv_mh_auth_pass or not o.company_id.partner_id.nit))
        if failed_documents:
            invoices_str = ", ".join(failed_documents.mapped('name'))
            raise UserError(_("Invoices %s not eligible to sent .", invoices_str))

        documents = self
        return documents

    # ===== CRONs =====

    @api.model
    def cron_l10n_sv_invoices_to_sent(self, max_doc=10):
        """Busca los ecf q estan pendientes por enviar."""

        documents = self.search([('invoice_id', '!=', False),
                                 ('json_file', '!=', False),
                                 ('l10n_sv_dte_send_state', 'in', ['signed_pending'])], order='id asc', limit=max_doc)
        for doc in documents:
            doc.action_send_to_hacienda()

    @api.model
    def _send_mail(self, max_mails=10, max_dias=1):
        """Envia email al cliente. De forma masiva (cron) o para un solo registro (Bton Send Email).

            """

        def _set_attachment_data(doc, email_template, voucher_type_name):
            # Se agregan los documentos nuevamente en vista de que los metodos anteriores fallaron
            # Adjuntos
            ir_attachment = self.env['ir.attachment'].sudo()
            json_vals = {'name': str(doc.json_file_name),
                         'datas': doc.json_file1,
                         'res_id': doc.id,
                         'res_model': self._name,
                         'type': 'binary',
                         }
            attachment_xml_file = ir_attachment.create(json_vals)
            attachment_ids = []
            if attachment_xml_file:
                attachment_ids.append(attachment_xml_file.id)

            if attachment_ids:
                email_template.attachment_ids = [Command.set(attachment_ids)]
                email_template.subject = "{{ object.company_id.name }} Factura (Ref {{ object.name or 'n/a' }})"
                email_template.with_context(type='binary', default_type='binary').send_mail(
                    doc.invoice_id.id, raise_exception=False, force_send=True)

                # Se eliminan los archivos creados previamente para no generar basura
                attachment_xml_file.unlink()
                email_template.attachment_ids = [Command.clear()]
                doc.l10n_sv_state_mail = 'sent'
                doc.message_post(subject='Email', body=f'{voucher_type_name} enviada')

        if self:
            documents = self
        else:
            date_origin = datetime.now() - timedelta(days=max_dias)
            documents = self.search([
                ('l10n_sv_dte_send_state', '=', 'delivered_accepted'),
                ('create_date', '>=', date_origin),
                ('l10n_sv_state_mail', 'not in', ['sent', 'not_mail'])], order='id', limit=max_mails)

        _logger.info('\n\n %r \n\n', documents)
        if not documents:
            return

        for doc in documents:
            voucher_type_name = doc.l10n_sv_voucher_type_id and doc.l10n_sv_voucher_type_id.name or 'Factura'
            if doc.invoice_id and doc.partner_id and doc.partner_id.email:
                email_template = self.env.ref(
                    'account.email_template_edi_invoice', False)
                if email_template:
                    email_template.attachment_ids = [Command.clear()]
                else:
                    _logger.warning('El template de factura de email no existe')
                    continue

                _set_attachment_data(doc, email_template, voucher_type_name)
            else:
                doc.l10n_sv_state_mail = 'not_mail'
                doc.message_post(subject='Email', body=f'{voucher_type_name} no enviado, la empresa no tiene email')


class DTEDocumentANDTE(models.Model):
    _name = 'l10n_sv.dte.andte.message.detail'
    _description = 'ECF Document GDII Message Detail'
    _order = 'id desc'

    version = fields.Char()
    ambiente = fields.Char()
    versionApp = fields.Char()
    estado = fields.Char()
    codigoGeneracion = fields.Text()
    selloRecibido = fields.Text()
    fhProcesamiento = fields.Text()
    descripcionMsg = fields.Text()
    observaciones = fields.Text()


class DTEDocumentCODTE(models.Model):
    _name = 'l10n_sv.dte.codte.message.detail'
    _description = 'ECF Document GDII Message Detail'
    _order = 'id desc'

    estado = fields.Char()
    fechaHora = fields.Text()
    selloRecibido = fields.Text()
    mensaje = fields.Text()
    observaciones = fields.Text()
