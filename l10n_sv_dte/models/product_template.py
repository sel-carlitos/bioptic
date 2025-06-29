# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    l10n_sv_donation_type = fields.Selection([('1', 'Efectivo'), ('2', 'Bien'), ('3', 'Servicio')], string="Tipo de Donación")
