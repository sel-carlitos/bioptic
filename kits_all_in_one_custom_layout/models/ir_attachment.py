from odoo import _, models
from odoo.exceptions import UserError


class ir_attachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        for rec in self:
            if rec.name == 'kits_custom_fonts.scss' and not self._context.get('kits_is_delete'):
                raise UserError(_('kits_custom_fonts.scss – This attachment should not be deleted.'))
        return super().unlink()
