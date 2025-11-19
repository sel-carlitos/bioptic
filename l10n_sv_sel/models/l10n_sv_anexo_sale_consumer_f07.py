# -*- coding: utf-8 -*-

from odoo import fields, models


class L10nSvAnexoSaleConsumer(models.Model):
    _name = "l10n_sv.anexo.sale.consumer"
    _description = "Anexo F07 - Linea Ventas de Consumidor Final"
    _order = "sequence"

    anexo_id = fields.Many2one(
        "l10n_sv.anexo_f07",
        required=True,
        ondelete="cascade",
        index=True,
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
    )
    tipo_documento = fields.Char(
        string="Tipo Documento",
        required=True,
    )
    numero_resolucion = fields.Char(string="Número Resolución", size=100)
    numero_serie = fields.Char(
        string="Número Serie",
        size=100,
    )
    numero_control_interno_del = fields.Char(
        string="Nro Control Interno (DEL)",
        size=100,
    )
    numero_control_interno_al = fields.Char(string="Nro Control Interno (AL)", size=100)
    numero_documento_del = fields.Char(
        string="Número Documento (DEL)",
        size=100,
    )
    numero_documento_al = fields.Char(
        string="Número Documento (AL)",
        size=100,
    )
    n_cash_register = fields.Char(
        string="Nro Caja Registradora",
        size=100,
    )
    ventas_exentas = fields.Monetary(
        string="Ventas Exentas",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    ventas_in_exenta_no_proporcionalidad = fields.Monetary(
        string="Ventas Internas Exenta No Sujeta a Proporcionalidad",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    ventas_no_sujetas = fields.Monetary(
        string="Ventas No Sujetos",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    ventas_gravadas_locales = fields.Monetary(
        string="Ventas Gravadas Locales",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    exportaciones_ca = fields.Monetary(
        string="Exportaciones C.A",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    exportaciones_fuera_ca = fields.Monetary(
        string="Exportaciones Fuera C.A",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    exportaciones_servicio = fields.Monetary(
        string="Exportaciones Servicios",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    ventas_zna_franca_dpa = fields.Monetary(
        string="Ventas ZNA, Franca, DPA tasa cero",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    ventas_terceros_no_domiciliados = fields.Monetary(
        string="Ventas a Terceros No Domiciliados",
        digits=(16, 2),
        default=0.0,
        currency_field="currency_id",
    )
    total_ventas = fields.Monetary(
        string="Total Ventas",
        digits=(16, 2),
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    tipo_operacion_renta = fields.Char(
        default="1",
    )
    tipo_ingreso_renta = fields.Char(
        default="3",
    )
    numero_anexo = fields.Integer(
        string="Número Anexo",
        default=2,
    )
    snapshot = fields.Text(
        string="Snapshot",
        readonly=True,
    )
