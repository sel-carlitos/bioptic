# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class L10nSvIdentificationType(models.Model):
    _name = "l10n_sv.identification.type"
    _description = "Tipo de documento de identificación del Receptor"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    notes = fields.Text()
