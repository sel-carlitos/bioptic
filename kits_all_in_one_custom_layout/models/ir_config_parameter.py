from odoo import _, models
from odoo.exceptions import UserError


class ir_config_parameter(models.Model):
    _inherit = 'ir.config_parameter'

    def unlink(self):
        for rec in self:
            if rec.key == 'kits_custom_report_font.kits_font_folder_path' and not self._context.get('kits_is_delete'):
                raise UserError(
                    _('kits_custom_report_font.kits_font_folder_path – This parameter should not be deleted.')
                )
        return super().unlink()
