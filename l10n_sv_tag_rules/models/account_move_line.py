from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.constrains("tax_ids")
    def _check_tax_type_consistency_compute(self):
        self._check_tax_type_consistency()

    # @api.onchange("tax_ids")
    # def _check_tax_type_consistency_onchange(self):
    #     self._check_tax_type_consistency()

    def _check_tax_type_consistency(self):
        for line in self:
            types = set(line.tax_ids.mapped("type_operation_line"))
            # Solo uno de los tres tipos principales puede coexistir
            main_types = types.intersection({"no_sujeto", "exento", "gravado"})
            if len(main_types) > 1:
                raise ValidationError(
                    _(
                        "Una línea no puede tener impuestos de tipo No Sujeto, Exento y Gravado al mismo tiempo."
                    )
                )
            # Validar relaciones indebidas
            if "iva_retenido" in types and {"otros"} & types:
                raise ValidationError(
                    _(
                        "Una línea con retención no puede tener impuestos de tipo FOVIAL o CONTRANS."
                    )
                )
