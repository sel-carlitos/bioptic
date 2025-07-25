from odoo import _, models
from odoo.exceptions import UserError


class ir_asset(models.Model):
    _inherit = 'ir.asset'

    def unlink(self):
        for rec in self:
            if rec.name == 'kits_custom_fonts' and not self._context.get('kits_is_delete'):
                raise UserError(_('kits_custom_fonts – This asset should not be deleted.'))
        return super().unlink()
