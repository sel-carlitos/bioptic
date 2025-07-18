# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

import base64
import io

from odoo import models
from odoo.tools.pdf import PdfFileWriter, PdfFileReader, NameObject, createStringObject


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        if self._get_report(report_ref).report_name != 'l4l_product_catalogue.l4l_report_product_catalogue':
            return result
        orders = self.env['generate.leap.product.catalogue'].browse(res_ids)
        for order in orders:
            initial_stream = result[order.id]['stream']
            if initial_stream:
                has_header = bool(order.catalogue_header)
                has_footer = bool(order.catalogue_footer)
                writer = PdfFileWriter()
                if has_header:
                    self._add_pages_to_writer(writer, base64.b64decode(order.catalogue_header))
                self._add_pages_to_writer(writer, initial_stream.getvalue())
                if has_footer:
                    self._add_pages_to_writer(writer, base64.b64decode(order.catalogue_footer))
                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                result[order.id].update({'stream': stream})
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
