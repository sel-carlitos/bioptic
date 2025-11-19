# -*- coding: utf-8 -*-
import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class L10nSvAnexoSaleTaxpayer(models.Model):
    _name = "l10n_sv.anexo.sale.taxpayer"
    _description = "Anexo F07 - Linea Ventas de Contribuyentes"
    _order = "sequence"

    anexo_id = fields.Many2one(
        "l10n_sv.anexo_f07",
        required=True,
        index=True,
        readonly=True,
    )
    sequence = fields.Integer(
        string="Orden",
    )
    fecha_emision = fields.Char(
        string="Fecha Emisión",
        required=True,
    )
    clase_documento = fields.Char(
        string="Clase Documento",
        required=True,
        readonly=True,
    )
    tipo_documento = fields.Char(
        string="Tipo Documento",
        required=True,
        readonly=True,
    )
    numero_resolucion = fields.Char(
        string="Número Resolución",
        size=100,
        readonly=True,
    )
    numero_serie = fields.Char(
        string="Número Serie",
        size=100,
        readonly=True,
    )
    numero_documento = fields.Char(
        string="Número Documento",
        size=100,
        readonly=True,
    )
    numero_control_interno = fields.Char(
        string="Nro Control Interno",
        size=100,
        readonly=True,
    )
    nit_nrc_cliente = fields.Char(
        string="NIT/NRC Cliente",
        size=14,
    )
    nombre_cliente = fields.Char(
        string="Nombre Cliente",
        size=255,
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    ventas_exentas = fields.Monetary(
        string="Ventas Exentas",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    ventas_no_sujetas = fields.Monetary(
        string="Ventas No Sujetos",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    ventas_gravadas_locales = fields.Monetary(
        string="Ventas Gravadas Locales",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    debito_fiscal = fields.Monetary(
        string="Débito Fiscal",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    ventas_terceros_no_domiciliados = fields.Monetary(
        string="Ventas a Terceros No Domiciliados",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    debito_fiscal_terceros = fields.Monetary(
        string="Débito Fiscal Terceros",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    total_ventas = fields.Monetary(string="Total Ventas", digits=(16, 2), readonly=True)
    dui_cliente = fields.Char(string="DUI Cliente", size=9, readonly=True)
    tipo_operacion_renta = fields.Char(default="1", readonly=True)
    tipo_ingreso_renta = fields.Char(
        default="3",
        readonly=True,
    )
    numero_anexo = fields.Integer(string="Número Anexo", default=1)
    move_line_id = fields.Many2one(
        "account.move.line",
        string="Linea contable origen",
        ondelete="set null",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        ondelete="set null",
    )
    move_id = fields.Many2one(
        "account.move",
        string="Account Move",
        readonly=True,
    )
    snapshot = fields.Text(
        string="Snapshot",
        readonly=True,
    )

    @api.constrains("nit_nrc_cliente", "dui_cliente", "fecha_emision")
    def _check_cliente_identifiers_and_date(self):
        for rec in self:
            if rec.nit_nrc_cliente and rec.dui_cliente:
                raise ValidationError(
                    _("Los campos NIT/NRC y DUI no pueden estar ambos completos.")
                )
            if (
                rec.dui_cliente
                and rec.dui_cliente.strip()
                and len(re.sub(r"\D", "", rec.dui_cliente)) != 9
            ):
                raise ValidationError(_("DUI debe tener 9 dígitos (sin guiones)."))
            if (
                rec.nit_nrc_cliente
                and rec.nit_nrc_cliente.strip()
                and len(re.sub(r"\D", "", rec.nit_nrc_cliente)) > 14
            ):
                raise ValidationError(_("NIT/NRC no puede exceder 14 caracteres."))
            if rec.fecha_emision:
                try:
                    d = datetime.strptime(rec.fecha_emision, "%d/%m/%Y").date()
                except Exception:
                    raise ValidationError(
                        _("fecha_emision debe tener formato DD/MM/AAAA.")
                    )
                if rec.anexo_id and (
                    d < rec.anexo_id.date_from or d > rec.anexo_id.date_to
                ):
                    raise ValidationError(
                        _("La fecha de emisión debe pertenecer al rango del anexo.")
                    )
