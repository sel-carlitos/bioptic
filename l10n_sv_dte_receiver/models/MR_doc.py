# -*- coding: utf-8 -*-
from odoo.addons.l10n_cr_invoice.models import MR
from odoo.addons.l10n_cr_invoice.models.ce_document import L10N_CR_DATE_FORMAT
from odoo.exceptions import UserError
from datetime import datetime
import pytz
import logging
_logger = logging.getLogger(__name__)


class MR_DOC:

    def __init__(self, state_inv_supplier, xml_amount_total, xml_amount_tax, partner_id, company_id, ref,
                 economic_activity_id):
        self.state_inv_supplier = state_inv_supplier
        self.xml_amount_total = xml_amount_total
        self.xml_amount_tax = xml_amount_tax
        self.partner_id = partner_id
        self.company_id = company_id
        self.ref = ref
        self.economic_activity_id = economic_activity_id

    def gen_mr_doc(self, terminal_id, state_inv_supplier_dict):
        """ Retorna la instancia del elemento raiz de MR.

            :returns: obj de MensajeReceptor
            """

        now = datetime.now(pytz.timezone("America/Costa_Rica")).strftime(L10N_CR_DATE_FORMAT)

        if not terminal_id:
            return

        try:
            sequence = {
                '05': terminal_id.sequence_cace,
                '06': terminal_id.sequence_capce,
                '07': terminal_id.sequence_crce,
            }
            voucher_type = ''
            if self.state_inv_supplier == '1':  # accepted
                voucher_type = '05'
            elif self.state_inv_supplier == '2':  # partially accepted
                voucher_type = '06'
            elif self.state_inv_supplier == '3':  # denied
                voucher_type = '07'

            consecutive = "%s%s%s%s" % (
                terminal_id.location_id.code,
                terminal_id.code,
                voucher_type,
                sequence[voucher_type].next_by_id())

        except Exception as e:
            raise UserError("Error al obtener Numeración Consecutiva: \n %s" % e)

        mr_doc = MR.MensajeReceptor(Clave=self.ref,
                                    NumeroCedulaEmisor=self.partner_id.vat.replace('-', ''),
                                    FechaEmisionDoc=now,
                                    Mensaje=int(self.state_inv_supplier),
                                    NumeroCedulaReceptor=int(self.company_id.vat.replace('-', '')),
                                    NumeroConsecutivoReceptor=consecutive,
                                    DetalleMensaje=state_inv_supplier_dict[self.state_inv_supplier],
                                    CodigoActividad=self.economic_activity_id.code,
                                    )
        if self.xml_amount_tax:
            mr_doc.set_MontoTotalImpuesto(self.xml_amount_tax)

        mr_doc.set_TotalFactura(self.xml_amount_total)
        return mr_doc
