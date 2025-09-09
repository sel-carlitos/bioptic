# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from .Invoice import Invoice, InvoiceLine
from odoo.exceptions import UserError, ValidationError
import json
import logging
_logger = logging.getLogger(__name__)

L10N_SV_VOUCHER_TYPE_MAP = {
    '03': 'FacturaElectronica',
    '05': 'NotaCreditoElectronica',
    '06': 'NotaDebitoElectronica',
    # 'TiqueteElectronico': '04',
}


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _create_document_from_attachment(self, attachment_ids):
        """ Create the invoices from files."""
        if not self:
            self = self.env['account.journal'].browse(self._context.get("default_journal_id"))
        move_type = self._context.get("default_move_type", "entry")
        if not self:
            if move_type in self.env['account.move'].get_sale_types(include_receipts=True):
                journal_type = "sale"
            elif move_type in self.env['account.move'].get_purchase_types(include_receipts=True):
                journal_type = "purchase"
            else:
                raise UserError(_("The journal in which to upload the invoice is not specified."))

            self = self.env['account.journal'].search([
                *self.env['account.journal']._check_company_domain(self.env.company),
                ('type', '=', journal_type),
                ('l10n_sv_fiscal_journal', '=', False),
            ], limit=1)

        attachments = self.env['ir.attachment'].sudo().browse(attachment_ids)
        if not attachments:
            raise UserError(_("No attachment was provided"))

        if not self:
            raise UserError(_("No journal found. Please must be create a jornal %s not fiscal.") % journal_type)

        if move_type not in ["in_invoice", "in_refund"]:
            raise UserError(
                "Esta accion solo es permitida para diarios de compra-reembolso.")

        # As we are coming from the journal, we assume that each attachments
        # will create an invoice with a tentative to enhance with EDI / OCR..
        all_invoices = self.env['account.move']
        for attachment in attachments:
            if attachment.mimetype not in ['application/json', 'text/plain']:
                raise UserError(_("The uploaded file is not supported. Bust be XML file."))

            try:
                bytes_result = attachment.raw
                json_dict = json.loads(bytes_result)
                identificacion = json_dict.get('identificacion')
                dte_type = identificacion.get('tipoDte')
            except Exception as e:
                raise ValidationError(e)

            if dte_type is None:
                raise ValidationError(_("Could not find document type."))

            if dte_type == '03':
                # docu = FE.parseString(attachment.raw, silence=True)
                voucher_type_txt = L10N_SV_VOUCHER_TYPE_MAP[dte_type]
            elif dte_type == '05':
                # docu = NC.parseString(attachment.raw, silence=True)
                voucher_type_txt = L10N_SV_VOUCHER_TYPE_MAP[dte_type]
            elif dte_type == '06':
                # docu = ND.parseString(attachment.raw, silence=True)
                voucher_type_txt = L10N_SV_VOUCHER_TYPE_MAP[dte_type]
            else:
                _logger.info("Tipo de comprobante desconocido: " + dte_type)
                continue
                # raise ValidationError(_("Tipo de comprobante desconocido: " + tipo_xml))

            if move_type == "in_invoice":
                # company_id = self.company_id
                # receptor = docu.get_Receptor()
                emisor = json_dict.get('emisor')
                # if receptor and receptor.get_Identificacion().get_Numero() != company_id.vat:
                #     raise ValidationError(
                #         "El archivo esta dirigido a la identificacion: {} que no coincide con la identificacion de la compañia {}".format(
                #             receptor.get_Identificacion().get_Numero(), self.env.company.vat))
                #
                # emisor = docu.get_Emisor()
                # identification_type = emisor.get_Identificacion().get_Tipo()
                # ident_number = emisor.get_Identificacion().get_Numero()
                # tin_type = self.env['ce.identification.type'].search([('code', '=', identification_type)])
                #
                # if not tin_type:
                #     raise ValidationError(_("Identification Type: " + identification_type + " not recognized"))

                domain = [('nit', '=', emisor.get('nit')), ('vat', '=', emisor.get('nrc'))]
                partner_id = self.env['res.partner'].search(domain, limit=1)

                if not partner_id:
                    partner_id = self.l10n_sv_create_partner_from_doc(emisor)
            if move_type == "in_refund":
                emisor = json_dict.get('emisor')
                # identification_type = emisor.get_Identificacion().get_Tipo()
                # ident_number = emisor.get_Identificacion().get_Numero()
                # tin_type = self.env['ce.identification.type'].search([('code', '=', identification_type)])
                #
                # if not tin_type:
                #     raise ValidationError(_("Identification Type: " + identification_type + " not recognized"))

                domain = [('nit', '=', emisor.get('nit')), ('vat', '=', emisor.get('nrc'))]
                partner_id = self.env['res.partner'].search(domain, limit=1)

            invoice = self.l10n_sv_create_invoice(json_dict, partner_id, dte_type, voucher_type_txt)
            all_invoices |= invoice
            invoice.with_context(
                account_predictive_bills_disable_prediction=True,
                no_new_invoice=True,
            ).message_post(attachment_ids=attachment.ids)
            attachment.sudo().write({'res_model': 'account.move', 'res_id': invoice.id})

        return all_invoices

    @api.model
    def l10n_sv_create_partner_from_doc(self, partner):
        """ Crea el partner a partir de la informacion del JSON."""

        EconomicActivity = self.env['l10n_sv.economic.activity']
        economic_activity_id = EconomicActivity.search([('code', '=', partner.get('codActividad'))], limit=1)
        if not economic_activity_id:
            raise ValidationError(_("Economic Activity not found: " + partner.get('codActividad')))

        direccion = partner.get('direccion', {})
        state = direccion.get('departamento')
        if state:
            state_id = self.env['res.country.state'].search([('dte_code', '=', state)], limit=1)

        municipality = direccion.get('municipio')
        if municipality and state_id:
            municipality_id = self.env['res.municipality'].search([('dte_code', '=', municipality),
                                                                   ('state_id', '=', state_id.id)], limit=1)
        if partner.get('nit', ''):
            identification_type_id = self.env["l10n_sv.identification.type"].search([('code', '=', '36')], limit=1)

        partner_vals = {
            'name': partner.get("nombre"),
            'l10n_sv_activity_id': economic_activity_id.id,
            'l10n_sv_commercial_name': partner['nombreComercial'] if partner.get('nombreComercial', '') else False,
            'l10n_sv_identification_id': identification_type_id.id if partner.get('nit', '') else False,
            'vat': partner.get('nrc') if partner.get('nrc', '') else False,
            'nit': partner.get('nit') if partner.get('nit', '') else False,
            'phone': str(partner['telefono']) if partner.get('telefono') else '',
            'email': str(partner['correo']) if partner.get('correo') else '',
            'street': direccion.get('complemento') if direccion else '',
            # 'country_id': country_id.id,
            'state_id': state_id.id if state else None,
            'res_municipality_id': municipality_id.id if municipality else None,
            'is_company': True if partner.get('nrc', '') else False
        }

        new_partner = self.env['res.partner'].create(partner_vals)
        return new_partner

    @api.model
    def l10n_sv_create_get_product(self, lineadetalle, partner_id, company_id, currency_id):
        ProductProduct = self.env['product.product']
        product_name = lineadetalle.get('descripcion')
        # product_code = ""
        # barcode = ""
        # default_code = ""

        # args = [('partner_id', '=', partner_id.id),
        #         '|',
        #         ('product_name', '=', product_name)]

        # for codigo_comercial in lineadetalle.get_CodigoComercial():
        #     codigo_tipo = codigo_comercial.get_Tipo()
        #     codigo_value = codigo_comercial.get_Codigo().strip()
        #
        #     if codigo_tipo == '01':
        #         product_code = codigo_value
        #         args.append(('product_code', '=', product_code))
        #     elif codigo_tipo == '02':  # codigo del comprador
        #         default_code = codigo_value
        #     elif codigo_tipo == '03':  # Barcode
        #         barcode = codigo_value
        #     elif codigo_tipo == '04' and not default_code:  # codigo de uso interno
        #         default_code = codigo_value
        #     elif codigo_tipo == '99' and not default_code:
        #         default_code = codigo_value
        #
        # if not product_code:
        #     del (args[1])

        products = []
        # first try to get the product by searching using supplier_id
        # product_name or product_code
        # if not products and partner_id:
        #     suppliers = self.env['product.supplierinfo'].search(args)
        #     if suppliers:
        #         products = ProductProduct.search([('seller_ids', 'in', suppliers.ids)], limit=1)
        #
        # # Product not found by supplier
        # if not products and barcode:
        #     products = ProductProduct.search([('barcode', '=', barcode)], limit=1)
        #
        # if not products and default_code:
        #     products = ProductProduct.search([('default_code', '=', default_code)], limit=1)

        if not products and product_name:
            products = ProductProduct.search([('name', '=', product_name)], limit=1)
            if not products:
                products = ProductProduct.search([('name', 'ilike', product_name)], limit=1)
        if not products:
            price_unit = lineadetalle.get_PrecioUnitario()
            journal_type = self.type
            vals = {
                'name': product_name,
                'type': 'consu',
                'company_id': company_id.id,
                'sale_ok': False,
            }
            if journal_type == "sale":
                vals['list_price'] = price_unit
            if journal_type == "purchase":
                vals['standard_price'] = price_unit

            uom_code_id = self.env['uom.uom'].search([('dte_code', '=', lineadetalle.get('uniMedida'))])
            if not uom_code_id:
                uom_code_id = self.env['uom.uom'].search([('dte_code', '=', '59')])  # should always exist in DB

            # if uom_code_id.ce_service:
            #     vals['detailed_type'] = 'service'
            vals['uom_id'] = uom_code_id.id
            vals['uom_po_id'] = uom_code_id.id

            # if barcode:
            #     vals['barcode'] = barcode
            #     vals['default_code'] = barcode

            impuestos = lineadetalle.get('tributos')
            supplier_taxes_id = []
            for impl in impuestos:
                imp = self.env['account.tax'].search([('l10n_sv_code', '=', impl),
                                                      ('type_tax_use', '=', 'purchase'),
                                                      ('company_id', '=', company_id.id)
                                                      ])

                if imp:
                    supplier_taxes_id.append(imp[0].id)

            if len(supplier_taxes_id) > 0:
                vals['supplier_taxes_id'] = [(6, 0, supplier_taxes_id)]

            supplierinfo = {
                'partner_id': partner_id.id,
                'product_name': product_name,
                'price': price_unit,
                'currency_id': currency_id.id,
                'min_qty': 1,
            }

            # if product_code:
            #     supplierinfo['product_code'] = product_code

            vals['seller_ids'] = [(0, 0, supplierinfo)]
            products = ProductProduct.create(vals)

        return products

    def l10n_sv_get_invoice_line_account(self, type, product, fpos, company):
        accounts = product.product_tmpl_id.get_product_accounts(fpos)
        if type in ('out_invoice', 'out_refund'):
            return accounts['income']
        return accounts['expense']

    def l10n_sv_create_invoice(self, docu, partner_id, tipo, voucher_type_txt, **kwargs):
        invoice_vals = self._l10n_sv_prepare_invoice_model(docu, partner_id, tipo, voucher_type_txt)
        invoice_vals['journal_id'] = self.id
        invoice_vals.update(kwargs)
        invoice_id = self.env['account.move'].create(invoice_vals)
        return invoice_id

    def _l10n_sv_prepare_invoice_model(self, docu, partner_id, tipo, voucher_type_txt):
        move_type = self._context.get("default_move_type", "in_invoice")
        company_id = self.company_id
        invoice_type = move_type
        if tipo == '03':
            voucher_type_id = self.env.ref('l10n_sv_dte.voucher_03')
        elif tipo == '05':
            voucher_type_id = self.env.ref('l10n_sv_dte.voucher_05')
            invoice_type = 'in_refund'
        else:
            voucher_type_id = self.env.ref('l10n_sv_dte.voucher_06')

        identificacion = docu.get('identificacion')
        invoice_vals = {
            'move_type': invoice_type,
            'ref': identificacion.get('codigoGeneracion') if invoice_type in ('in_invoice', 'in_refund') else False,
            'partner_id': partner_id.id,
            'invoice_date': identificacion.get("fecEmi"),
            'company_id': company_id.id,
            # 'narration': 'Plazo de credito %s dias. Medio de pago: %s ' % (plazo_credito, medio_pago),
            # 'xml_amount_tax': float(docu.get_ResumenFactura().get_TotalImpuesto()),
            # 'xml_amount_total': float(docu.get_ResumenFactura().get_TotalComprobante()),
            'l10n_sv_voucher_type_id': voucher_type_id.id,
            'l10n_sv_generation_code': identificacion.get('codigoGeneracion'),
            'l10n_sv_document_number': identificacion.get('numeroControl'),
        }

        invoice_line = self._l10n_sv_gen_model_invoice_line(docu, partner_id)
        invoice_vals['invoice_line_ids'] = [(0, 0, line.PrepareInvoiceLine()) for line in invoice_line]
        return invoice_vals

    def _l10n_sv_gen_model_invoice_line(self, docu, partner_id):
        """Crea las lineas de factura.

            :param object docu: Instancia del Elemento raiz.
            """
        move_type = self._context.get("default_move_type", "in_invoice")
        company_id = self.company_id
        invoice_type = move_type
        invoice = Invoice()
        body_document = docu.get('cuerpoDocumento')
        for l in body_document:
            product_name = l.get('descripcion')
            default_product_from_xml = self.env['ir.config_parameter'].sudo().get_param(
                'l10n_sv_dte_receiver.l10n_sv_create_product_from_xml')
            line_taxes = []
            if l.get('tributos'):
                for i in l.get('tributos'):
                    l10n_sv_code = i
                    search_params = [('l10n_sv_code', '=', l10n_sv_code),
                                     ('type_tax_use', '=', 'sale' if move_type == 'out_invoice' else 'purchase'),
                                     ('company_id', '=', company_id.id),
                                     ('country_id', '=', self.env.ref("base.sv").id),
                                     ]

                    tax_id = self.env['account.tax'].search(search_params)
                    # if not tax_id:
                    #     journal_type = 'sale' if invoice_type == 'out_invoice' else 'purchase'
                    #     _logger.info(
                    #         "Tax not found in system: " + i.get_Codigo() + " with tarifa: " + str(
                    #             i.get_Tarifa()))
                    #
                    #     if i.get_Codigo() in ('99', '05'):
                    #         _logger.info(
                    #             'Impuesto con codigo (' + i.get_Codigo()
                    #             + ') no se encuentra en el sistema, favor crearlo antes de importar. '
                    #               'Este impuesto es configurado como monto fijo y puede indicar 0.0 en dicho monto, '
                    #               'el valor sera el que venga en la factura de venta.')
                    #     _logger.info(
                    #         'Impuesto de ' + journal_type + ' con codigo (' + i.get_Codigo() + ') con tarifa="' + str(
                    #             i.get_Tarifa()) + '" no se encuentra en el sistema, favor crearlo antes de importar')
                    #
                    #     raise ValidationError(_(f"Tax not found in system {journal_type}: {i.get_Codigo()} "
                    #                             f"with amount: {str(i.get_Tarifa())} in company active."))

                    line_taxes.append(tax_id[0].id)

            invoice_line = InvoiceLine(
                name=product_name,
                # total=l.get_MontoTotalLinea(),
                quantity=float(l.get('cantidad')),
                price=float(l.get('precioUni')),
                tax_ids=line_taxes,
            )

            if default_product_from_xml:
                product_id = self.l10n_sv_create_get_product(l, partner_id, company_id, company_id.currency_id)
                product_account = self.l10n_sv_get_invoice_line_account(invoice_type, product_id, None, company_id)
                invoice_line.product_id = product_id.id
                invoice_line.product_uom_id = product_id.uom_id.id
                invoice_line.account_id = product_account.id if product_account else None

            total_amount_discount = l.get('montoDescu', 0)
            if total_amount_discount > 0:
                price_subtotal = float(l.get('cantidad') * l.get('precioUni'))
                discount_percent = round((total_amount_discount / price_subtotal) * 100, 2)
                if discount_percent > 0:
                    invoice_line.discount = discount_percent

            _logger.info(invoice_line)
            invoice.addLine(invoice_line)

        return invoice.getLines()
