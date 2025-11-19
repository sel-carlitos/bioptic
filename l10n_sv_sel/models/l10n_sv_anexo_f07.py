# -*- coding: utf-8 -*-
import base64
import hashlib
import io
import json
import re

from odoo import api, fields, models


class L10nSvAnexoF07(models.Model):
    _name = "l10n_sv.anexo_f07"
    _description = "Anexo F07 - Cabecera"
    _order = "date_from desc"

    name = fields.Char(
        string="Nombre",
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    date_from = fields.Date(
        string="Desde",
        required=True,
        index=True,
    )
    date_to = fields.Date(
        string="Hasta",
        required=True,
        index=True,
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("replaced", "Reemplazado"),
            ("cancelled", "Anulado"),
        ],
        default="draft",
        required=True,
    )
    sale_line_ids = fields.One2many(
        "l10n_sv.anexo.sale.taxpayer",
        "anexo_id",
        string="Líneas Ventas Contribuyentes",
        copy=True,
    )
    sale_consumer_line_ids = fields.One2many(
        "l10n_sv.anexo.sale.consumer",
        "anexo_id",
        string="Líneas Ventas Consumidor Final",
        copy=True,
    )
    csv_anexo_sale_taxpayer_file = fields.Binary('File', readonly=True)
    csv_anexo_sale_taxpayer_filename = fields.Char('Nombre Archivo')

    note = fields.Text(string="Notas")

    @api.depends("sale_line_ids")
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.sale_line_ids)

    @api.depends()
    def _compute_totals(self):
        for rec in self:
            rec.total_base = 0.0
            rec.total_impuesto = 0.0
            rec.total_monto = 0.0

    def name_get(self):
        res = []
        for r in self:
            name = (
                r.name
                or f"F07/{r.company_id.vat or r.company_id.name}/{r.date_from}_{r.date_to}"
            )
            res.append((r.id, name))
        return res

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not record.name:
            record.name = f"F07/{record.company_id.vat or record.company_id.name}/{record.date_from}_{record.date_to}"
        return record

    def action_generate_sale_contrib(self):
        return self._action_generate_sale()

    def action_generate_sale_consu_final(self):
        self.sale_consumer_line_ids.unlink()
        query = """
            WITH params AS (
                SELECT
                    %s::int AS company_id,
                    %s::date AS date_from,
                    %s::date AS date_to
                ),
            filtered_moves AS (
                SELECT
                    am.id                      AS move_id,
                    am.invoice_date::date      AS invoice_date,
                    am.move_type               AS move_type,
                    am.state                   AS move_state,
                    am.l10_sv_dte_id           AS l10_sv_dte_id,
                    am.l10n_sv_voucher_type_id AS l10n_sv_voucher_type_id,
                    lvt.code                   AS code
                FROM account_move am
                    JOIN l10n_sv_voucher_type lvt ON lvt.id = am.l10n_sv_voucher_type_id
                    JOIN params p ON true
                WHERE
                    am.company_id = p.company_id
                    AND am.invoice_date >= p.date_from
                    AND am.invoice_date <= p.date_to
                    AND am.state = 'posted'
                    AND am.move_type = 'out_invoice'
                    AND am.l10n_sv_dte_send_state = 'delivered_accepted'
                    AND lvt.code = '01'
                ),
            gravado_line_sum AS (
                SELECT
                    aml.move_id,
                    SUM(aml.credit) AS sum_credit
                FROM account_move_line aml
                JOIN filtered_moves fm ON fm.move_id = aml.move_id
                LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                WHERE
                    aml.parent_state = 'posted'
                    AND aml.display_type = 'product'
                    AND tax.type_operation_line = 'gravado'
                GROUP BY aml.move_id
                ),
            exento_line_sum AS (
                SELECT
                    aml.move_id,
                    SUM(aml.credit) AS sum_credit
                FROM account_move_line aml
                JOIN filtered_moves fm ON fm.move_id = aml.move_id
                LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                WHERE
                    aml.parent_state = 'posted'
                    AND aml.display_type = 'product'
                    AND tax.type_operation_line = 'exento'
                GROUP BY aml.move_id
                ),
            no_suj_line_sum AS (
                SELECT
                    aml.move_id,
                    SUM(aml.credit) AS sum_credit
                FROM account_move_line aml
                JOIN filtered_moves fm ON fm.move_id = aml.move_id
                LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                WHERE
                    aml.parent_state = 'posted'
                    AND aml.display_type = 'product'
                    AND tax.type_operation_line = 'no_sujeto'
                GROUP BY aml.move_id
                )

            SELECT
                fm.invoice_date                                   AS invoice_date,
                code                                              AS code,
                MIN(dte.name)                                     AS primer_dte_del_dia,
                MAX(dte.name)                                     AS ultimo_dte_del_dia,
                COALESCE(SUM(exento.sum_credit), 0.00)            AS exento,
                COALESCE(SUM(no_sujeto.sum_credit), 0.00)         AS no_sujeto,
                COALESCE(SUM(gravado.sum_credit), 0.00)           AS gravado,
                COUNT(DISTINCT fm.move_id)                        AS cantidad_dte
            FROM filtered_moves fm
                LEFT JOIN gravado_line_sum gravado ON gravado.move_id = fm.move_id
                LEFT JOIN exento_line_sum exento   ON exento.move_id = fm.move_id
                LEFT JOIN no_suj_line_sum no_sujeto ON no_sujeto.move_id = fm.move_id
                LEFT JOIN l10n_sv_dte_document dte ON dte.id = fm.l10_sv_dte_id
            GROUP BY fm.invoice_date, code
            ORDER BY fm.invoice_date;
        """
        params = (self.company_id.id, self.date_from, self.date_to)
        self.env.cr.execute(query, params)
        datas = self.env.cr.fetchall()
        vals = []
        seq = 1
        for data in datas:
            vals.append(
                (
                    0,
                    0,
                    {
                        "sequence": seq,
                        "fecha_emision": data[0],
                        "clase_documento": "4",
                        "tipo_documento": data[1],
                        "numero_resolucion": "N/A",
                        "numero_serie": "N/A",
                        "numero_control_interno_del": "N/A",
                        "numero_control_interno_al": "N/A",
                        "numero_documento_del": data[2],
                        "numero_documento_al": data[3],
                        "n_cash_register": "",
                        "ventas_exentas": data[4],
                        "ventas_no_sujetas": data[5],
                        "ventas_gravadas_locales": data[6],
                        "numero_anexo": "02",
                        "anexo_id": self.id,
                    },
                )
            )
            seq += 1

        if vals:
            self.write({"sale_consumer_line_ids": vals})
        return self

    def _action_generate_sale(self):
        self.sale_line_ids.unlink()

        domain = [
            ("company_id", "=", self.env.company.id),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
            ("state", "=", "posted"),
            ("move_type", "in", ["out_invoice", "out_refund"]),
            ("l10n_sv_dte_send_state", "=", "delivered_accepted"),
            ("l10n_sv_voucher_type_id.code", "in", ["03", "05"]),
        ]
        query = """
            WITH params AS (
                SELECT
                    %s::int AS company_id,
                    %s::date AS date_from,
                    %s::date AS date_to
                ),
            filtered_moves AS (
                SELECT
                    am.id                      AS move_id,
                    am.invoice_date::date      AS invoice_date,
                    am.move_type               AS move_type,
                    am.state                   AS move_state,
                    am.l10_sv_dte_id           AS l10_sv_dte_id,
                    am.l10n_sv_voucher_type_id AS l10n_sv_voucher_type_id,
                    lvt.code                   AS code,
                    am.partner_id              AS partner_id
                FROM account_move am
                    JOIN l10n_sv_voucher_type lvt ON lvt.id = am.l10n_sv_voucher_type_id
                    JOIN params p ON true
                WHERE
                    am.company_id = p.company_id
                    AND am.invoice_date >= p.date_from
                    AND am.invoice_date <= p.date_to
                    AND am.state = 'posted'
                    AND am.move_type in ('out_invoice', 'out_refund')
                    AND am.l10n_sv_dte_send_state = 'delivered_accepted'
                    AND lvt.code in ('03', '05', '06')
                ),
                gravado_line_sum AS (
                    SELECT
                        aml.move_id,
                        SUM(aml.credit) AS sum_credit
                    FROM account_move_line aml
                    JOIN filtered_moves fm ON fm.move_id = aml.move_id
                    LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                    LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                    WHERE
                        aml.parent_state = 'posted'
                        AND aml.display_type = 'product'
                        AND tax.type_operation_line = 'gravado'
                    GROUP BY aml.move_id
                    ),
                exento_line_sum AS (
                SELECT
                    aml.move_id,
                    SUM(aml.credit) AS sum_credit
                FROM account_move_line aml
                JOIN filtered_moves fm ON fm.move_id = aml.move_id
                LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                WHERE
                    aml.parent_state = 'posted'
                    AND aml.display_type = 'product'
                    AND tax.type_operation_line = 'exento'
                GROUP BY aml.move_id
                ),
                no_suj_line_sum AS (
                SELECT
                    aml.move_id,
                    SUM(aml.credit) AS sum_credit
                FROM account_move_line aml
                JOIN filtered_moves fm ON fm.move_id = aml.move_id
                LEFT JOIN account_move_line_account_tax_rel rel ON rel.account_move_line_id = aml.id
                LEFT JOIN account_tax tax ON tax.id = rel.account_tax_id
                WHERE
                    aml.parent_state = 'posted'
                    AND aml.display_type = 'product'
                    AND tax.type_operation_line = 'no_sujeto'
                GROUP BY aml.move_id
                )

                SELECT
                    fm.move_id                                        AS move_id,
                    fm.invoice_date                                   AS invoice_date,
                    fm.code                                           AS code,
                    dte.l10n_sv_generation_code                       AS generation_code,
                    dte.name                                          AS num_resol,
                    partner.nit                                       AS nit,
                    partner.dui                                       AS dui,
                    partner.vat                                       AS vat,
                    partner.name                                      AS partner_name,
                    itype.code                                        AS indentification_code,
                    COALESCE(gravado.sum_credit, 0.00)                AS gravado,
                    COALESCE(exento.sum_credit, 0.00)                 AS exento,
                    COALESCE(no_sujeto.sum_credit, 0.00)              AS no_sujeto,
                    partner.name                                      AS partner_name,
                    fm.move_type                                      AS move_type
                FROM filtered_moves fm
                    LEFT JOIN gravado_line_sum     gravado      ON gravado.move_id = fm.move_id
                    LEFT JOIN exento_line_sum      exento       ON exento.move_id = fm.move_id
                    LEFT JOIN no_suj_line_sum      no_sujeto    ON no_sujeto.move_id = fm.move_id
                    LEFT JOIN l10n_sv_dte_document dte          ON dte.id = fm.l10_sv_dte_id
                    LEFT JOIN res_partner          partner      ON partner.id = fm.partner_id
                    LEFT JOIN l10n_sv_identification_type itype ON itype.id = partner.l10n_sv_identification_id
        """
        params = (self.company_id.id, self.date_from, self.date_to)
        self.env.cr.execute(query, params)
        datas = self.env.cr.fetchall()
        moves = self.env["account.move"].search(domain)
        vals = []
        seq = 1
        for move in datas:
            id = move[0]
            move_id = self.env["account.move"].search([('id', '=', id)])
            tax_iva = move_id.tax_totals['subtotals'][0]['tax_groups'][0]['tax_amount_currency'] if move_id.tax_totals['subtotals'][0]['tax_groups'][0]['group_name'] else 0.0
            sign = -1.0 if move[15] == "out_refund" else 1.0
            fecha = move[1].strftime("%d/%m/%Y") if move[1] else ""

            type_op_income = "3"
            type_ingreso_renta = "3"
            if move[11] > 0.0:
                if move[12] > 0.0:
                    type_op_income = "4"
                else:
                    type_op_income = "1"
            elif move[12] > 0.0:
                type_op_income = "2"

            vals.append(
                (
                    0,
                    0,
                    {
                        "sequence": seq,
                        "fecha_emision": fecha,
                        "clase_documento": "4"
                        if move.move_type == "out_invoice"
                        else "1",
                        "tipo_documento": getattr(
                            move.l10n_sv_voucher_type_id, "code", ""
                        ),
                        "numero_resolucion": move[5],
                        "numero_serie": move[4],
                        "numero_documento": move[3],
                        "nit_nrc_cliente": move[6] if not move[7] else '',
                        "nombre_cliente": move[9],
                        "ventas_exentas": move[12],
                        "ventas_no_sujetas": move[13],
                        "ventas_gravadas_locales": move[11],
                        "debito_fiscal": tax_iva,
                        "total_ventas": '',
                        "dui_cliente": move[7] if not move[6] else '',
                        "numero_anexo": 1,
                        "partner_id": False,
                        "tipo_operacion_renta": type_op_income,
                        "tipo_ingreso_renta": type_ingreso_renta,
                        "snapshot": json.dumps(
                            {
                                "move_id": move.id,
                                "move_name": move.name,
                                "invoice_number": getattr(
                                    move, "invoice_number", move.name
                                ),
                                "date": fecha,
                            }
                        ),
                        'move_id': '',
                        "anexo_id": self.id,
                    },
                )
            )
            seq += 1

        if vals:
            self.write({"sale_line_ids": vals})
        return self

    def action_export_csv(self, separator=",", encoding="utf-8"):
        for anexo in self:
            buf = io.StringIO()
            headers = [
                "fecha_emision",
                "clase_documento",
                "tipo_documento",
                "numero_resolucion",
                "numero_serie",
                "numero_documento",
                "numero_control_interno",
                "nit_nrc_cliente",
                "nombre_cliente",
                "ventas_exentas",
                "ventas_no_sujetas",
                "ventas_gravadas_locales",
                "debito_fiscal",
                "ventas_terceros_no_domiciliados",
                "debito_fiscal_terceros",
                "total_ventas",
                "dui_cliente",
                "tipo_operacion_renta",
                "tipo_ingreso_renta",
                "numero_anexo",
            ]
            buf.write(separator.join(headers) + "\n")
            for ln in anexo.sale_line_ids.sorted("sequence"):
                row = []
                for col in headers:
                    val = getattr(ln, col, "")
                    if col in [
                        "ventas_exentas",
                        "ventas_no_sujetas",
                        "ventas_gravadas_locales",
                        "debito_fiscal",
                        "ventas_terceros_no_domiciliados",
                        "debito_fiscal_terceros",
                        "total_ventas",
                    ]:
                        row.append(f"{(val or 0.0):.2f}")
                    else:
                        text = val or ""
                        text = re.sub(r"[\r\n]+", " ", str(text)).strip()
                        row.append(text)
                buf.write(separator.join(row) + "\n")
            data = buf.getvalue().encode(encoding)
            fname = f"{anexo.name}_ventas.csv"
            attach = self.env["ir.attachment"].create(
                {
                    "name": fname,
                    "type": "binary",
                    "datas": base64.b64encode(data),
                    "mimetype": "text/csv",
                    "res_model": "l10n_sv.anexo_f07",
                    "res_id": anexo.id,
                }
            )
            checksum = hashlib.md5(data).hexdigest()
        return True

    def action_export_txt(self, separator="|", encoding="utf-8"):
        for anexo in self:
            buf = io.StringIO()
            for ln in anexo.sale_line_ids.sorted("sequence"):
                values = []
                cols = [
                    "fecha_emision",
                    "clase_documento",
                    "tipo_documento",
                    "numero_resolucion",
                    "numero_serie",
                    "numero_documento",
                    "numero_control_interno",
                    "nit_nrc_cliente",
                    "nombre_cliente",
                    "ventas_exentas",
                    "ventas_no_sujetas",
                    "ventas_gravadas_locales",
                    "debito_fiscal",
                    "ventas_terceros_no_domiciliados",
                    "debito_fiscal_terceros",
                    "total_ventas",
                    "dui_cliente",
                    "tipo_operacion_renta",
                    "tipo_ingreso_renta",
                    "numero_anexo",
                ]
                for col in cols:
                    val = getattr(ln, col, "")
                    if col in [
                        "ventas_exentas",
                        "ventas_no_sujetas",
                        "ventas_gravadas_locales",
                        "debito_fiscal",
                        "ventas_terceros_no_domiciliados",
                        "debito_fiscal_terceros",
                        "total_ventas",
                    ]:
                        values.append(f"{(val or 0.0):.2f}")
                    else:
                        text = val or ""
                        text = re.sub(r"[\r\n\|]+", " ", str(text)).strip()
                        values.append(text)
                buf.write(separator.join(values) + "\n")
            data = buf.getvalue().encode(encoding)
            fname = f"{anexo.name}_ventas.txt"
            attach = self.env["ir.attachment"].create(
                {
                    "name": fname,
                    "type": "binary",
                    "datas": base64.b64encode(data),
                    "mimetype": "text/plain",
                    "res_model": "l10n_sv.anexo_f07",
                    "res_id": anexo.id,
                }
            )
            checksum = hashlib.md5(data).hexdigest()
        return True

    def get_code_generation_per_day(self):
        query = """
            SELECT
                invoice_date,
                MIN(document_num) AS primer_dte_del_dia,
                MAX(document_num) AS ultimo_dte_del_dia,
                COUNT(*) AS cantidad_dte
            FROM (
            SELECT
                am.id                      AS move_id,
                am.invoice_date::date      AS invoice_date,
                am.company_id              AS company_id,
                am.partner_id              AS partner_id,
                am.l10_sv_dte_id           AS l10_sv_dte_id,
                am.l10n_sv_voucher_type_id AS l10n_sv_voucher_type_id,
                am.l10n_sv_dte_send_state  AS l10n_sv_dte_send_state,
                am.move_type               AS move_type,
                am.state                   AS state,
                dte.l10n_sv_generation_code AS document_num
            FROM account_move am
            JOIN l10n_sv_voucher_type lvt ON lvt.id = am.l10n_sv_voucher_type_id
            JOIN l10n_sv_dte_document dte ON dte.id = am.l10_sv_dte_id
            WHERE
                am.company_id = %s
                AND am.invoice_date >= %s
                AND am.invoice_date <= %s
                AND am.state = 'posted'
                AND am.move_type = 'out_invoice'
                AND am.l10n_sv_dte_send_state = 'delivered_accepted'
                AND lvt.code = '01'
            )
            GROUP BY invoice_date
            ORDER BY invoice_date;
        """
