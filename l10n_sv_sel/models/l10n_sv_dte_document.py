from collections import defaultdict

from odoo import models
from odoo.exceptions import ValidationError

from odoo.addons.l10n_sv_dte.models import CCFE, FE
from odoo.addons.l10n_sv_dte.models.account_tax import SV_TAXES
from odoo.addons.l10n_sv_dte.models.l10n_sv_dte_document import L10N_SV_INCOTERMS_MAP


class DTEDocument(models.Model):
    _inherit = 'l10n_sv.dte.document'

    def _construct_tax_excluded(self, price_with_taxes, amount_tax):
        self.ensure_one()
        price_wo_taxes = price_with_taxes / (1 + amount_tax / 100)
        tax = price_with_taxes - price_wo_taxes
        return price_wo_taxes, tax

    def _gen_body_document_and_summary(self, cedoc, classdoc):
        """Product lines related values

        :param object cedoc: Instancia u objeto del Elemento raiz.
        :param object classdoc: Clase del tipo de documento.

        :returns: tuple (response, vals)
        """
        invoice = self.invoice_id
        classdoc = FE if self.l10n_sv_voucher_type_id.code == '01' else classdoc
        body_document = classdoc.CuerpoDocumento()
        if self.l10n_sv_voucher_type_id.code not in ['15']:
            tributes = classdoc.Tributos()

        tax_data = self.get_taxed_amount_data()
        total_taxed = sum(
            [
                tax_data['13_taxed_base'],
                tax_data['exempt_amount'],
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
        total_discount = 0.00
        if self.l10n_sv_voucher_type_id.code not in ['07']:
            for i, line in enumerate(
                self._iterable_products_xml(lines)
                .filtered(lambda line: line.display_type == 'product' and line.quantity)
                .sorted('sequence'),
                1,
            ):
                iva_tax_total = 0.00
                subtotal_line_with_iva = 0.00
                subtotal_line_without_iva = line.price_subtotal
                for tax_subtotal in line.tax_totals['subtotals']:
                    for tax_group in tax_subtotal['tax_groups']:
                        tax_group_id = self.env['account.tax.group'].search(
                            [('id', '=', tax_group['id'])],
                            limit=1,
                        )
                        if tax_group_id.l10n_sv_code == '20':
                            iva_tax_total = tax_group['tax_amount_currency']
                            subtotal_line_with_iva = (
                                tax_group['base_amount_currency'] + tax_group['tax_amount_currency']
                            )
                tax_amount = sum(line.tax_ids.mapped('amount'))
                product_id = line.product_id
                product_name = product_id.name if product_id else (line.name or 'S/N')
                quantity = abs(line.quantity)
                price_unit_untaxed = self._construct_tax_excluded(line.price_unit, tax_amount)
                item = classdoc.Item(
                    numItem=i,
                    descripcion=self.limit(product_name, 80),
                    cantidad=quantity,
                )

                if self.l10n_sv_voucher_type_id.code in ['01']:
                    price_unit = (subtotal_line_with_iva or subtotal_line_without_iva) / line.quantity
                    item.set_precioUni(price_unit)
                elif self.l10n_sv_voucher_type_id.code not in ['15']:
                    item.set_precioUni(price_unit_untaxed[0])
                elif self.l10n_sv_voucher_type_id.code in ['15']:
                    item.set_valorUni(price_unit_untaxed[0])
                    item.set_valor(price_unit_untaxed[0] * item.get_cantidad())
                    item.set_depreciacion(0)

                if self.l10n_sv_voucher_type_id.code == '14':
                    item.set_compra(price_unit_untaxed[0] * quantity)

                item_type = 2 if (product_id and product_id.type == 'service') else 1
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
                        if t.l10n_sv_code != '20':
                            item.add_tributos(t.l10n_sv_code)
                        item.set_ivaItem(iva_tax_total)

                discount_amount = 0.00
                if line.discount > 0:
                    discount_amount = (price_unit_untaxed[0] * line.quantity) * line.discount / 100
                    item.set_montoDescu(abs(discount_amount))
                    total_discount += discount_amount

                if self.l10n_sv_voucher_type_id.code in ['01']:
                    base_line = abs(subtotal_line_with_iva)
                else:
                    base_line = abs(subtotal_line_without_iva)

                subtotal_line = base_line

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

        if self.invoice_id.l10n_sv_voucher_type_id.code not in ['11', '14', '15'] and tax_data['exempt_amount']:
            summary.set_totalExenta(abs(tax_data['exempt_amount']))

        if tax_data['iva_withholding_amount'] and self.invoice_id.l10n_sv_voucher_type_id.code not in ['07', '14']:
            summary.set_ivaRete1(abs(tax_data['iva_withholding_amount']))
        elif self.invoice_id.l10n_sv_voucher_type_id.code == '14':
            summary.set_reteRenta(abs(tax_data['iva_withholding_amount']))
        elif self.invoice_id.l10n_sv_voucher_type_id.code == '07':
            summary.set_totalSujetoRetencion(abs(self.invoice_id.amount_untaxed_signed))
            summary.set_totalIVAretenido(abs(tax_data['iva_withholding_amount']))

        if self.l10n_sv_voucher_type_id.code not in ['07'] and total_discount:
            summary.set_totalDescu(abs(total_discount))

        self.set_summary_additional_vals(summary, cedoc, classdoc)

        if total_taxed and self.invoice_id.l10n_sv_voucher_type_id.code in ['01']:
            total_prueba = 0.00
            for item in cedoc.get_cuerpoDocumento().get_Item():
                total_prueba += item.get_precioUni() * item.get_cantidad() - item.get_montoDescu()
            summary.set_totalGravada(abs(total_prueba) - summary.get_totalExenta())
            summary.set_subTotalVentas(abs(total_prueba))
            summary.set_subTotal(abs(total_prueba) - summary.get_totalDescu())
            summary.set_montoTotalOperacion(abs(invoice.amount_total) - summary.get_totalDescu())
            summary.set_totalPagar(abs(invoice.amount_total) - summary.get_ivaRete1() - summary.get_totalDescu())
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

        if self.invoice_id.l10n_sv_voucher_type_id.code in ['11']:
            summary.set_codIncoterms(self.invoice_id.l10n_sv_incoterm)
            summary.set_descIncoterms(L10N_SV_INCOTERMS_MAP[self.invoice_id.l10n_sv_incoterm])

        if self.l10n_sv_voucher_type_id.code not in ['07', '11', '14', '15']:
            tax_info = defaultdict(dict)
            tax_totals = invoice.tax_totals
            for subtotals_tax in tax_totals['subtotals']:
                for tax_group in subtotals_tax['tax_groups']:
                    tax_group_id = self.env['account.tax.group'].search(
                        [('id', '=', tax_group['id'])],
                        limit=1,
                    )
                    if self.l10n_sv_voucher_type_id.code == '01' and tax_group_id.l10n_sv_code == '20':
                        continue
                    tax_info[tax_group_id.l10n_sv_code]['descripcion'] = SV_TAXES[tax_group_id.l10n_sv_code]
                    tax_info[tax_group_id.l10n_sv_code]['valor'] = tax_group['tax_amount_currency']

            for tt in tax_info:
                tribute = CCFE.Tributo(codigo=tt, descripcion=tax_info[tt]['descripcion'], valor=tax_info[tt]['valor'])
                tributes.add_Item(tribute)
            summary.set_tributos(tributes)

        cedoc.set_resumen(summary)

    def get_document_number(self, partner_id):
        """Return document number for a partner.
        Falls back to VAT if no local identification is found.
        """
        if not partner_id.l10n_sv_identification_id:
            return partner_id.vat or None
        return super().get_document_number(partner_id)
