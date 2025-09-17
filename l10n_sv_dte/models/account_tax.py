# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
SV_TAXES = {"20": "Impuesto al Valor Agregado 13%",
            "D1":"FOVIAL ($0.20 Ctvs. por galón)",
            "C8": "COTRANS ($0.10 Ctvs. por galón)",
            "C3": "Impuesto al Valor Agregado (exportaciones) 0%",
        }


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _get_l10n_sv_tax_code(self):
        """ Return the list of IVA taxes rates and codes required by Hacienda. """
        return [
            ("20", "Impuesto al Valor Agregado 13%"),
            ("C3", "Impuesto al Valor Agregado (exportaciones) 0%"),
            ("59", "Turismo: por alojamiento (5%)"),
            ("71", "Turismo: salida del país por vía aérea $7.00"),
            ("D1", "FOVIAL ($0.20 Ctvs. por galón)"),
            ("C8", "COTRANS ($0.10 Ctvs. por galón)"),
            ("D5", "Otras tasas casos especiales"),
            ("D4", "Otros impuestos casos especiales"),
        ]

    l10n_sv_code = fields.Selection(string="Código de impuesto", selection="_get_l10n_sv_tax_code",
                                    help="CAT- 15: Código de tributos")
    # l10n_sv_iva_withholding_code = fields.Selection(string="IVA Withholding Code",
    #                                                 selection=[('22', 'Retención IVA 1%'),
    #                                                            ('C4', 'Retención IVA 13%'),
    #                                                            ('C9', 'Otras retenciones IVA casos especiales'),
    #                                                            ])
