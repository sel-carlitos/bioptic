from odoo import api, fields, models


class base_document_layout(models.TransientModel):
    _inherit = 'base.document.layout'

    header_background_image = fields.Binary(
        related='company_id.header_background_image', string='Header Background Image', readonly=False
    )
    header_image_file_name = fields.Char(
        related='company_id.header_image_file_name', string='File Name', readonly=False
    )
    is_img_header_layout = fields.Boolean(compute='kits_get_layout_info', string='Is Custom Layout')
    report_font_scale = fields.Selection(related='company_id.report_font_scale', readonly=False)

    @api.depends(
        'report_layout_id',
        'logo',
        'font',
        'primary_color',
        'secondary_color',
        'report_header',
        'report_footer',
        'layout_background',
        'layout_background_image',
        'company_details',
        'header_background_image',
        'report_font_scale',
    )
    def _compute_preview(self):
        return super()._compute_preview()

    def default_get(self, fields_list):
        ctx = dict(self.env.context)
        ctx.update({'kits_on_open_layout': True})
        self.env.context = ctx
        return super().default_get(fields_list)

    @api.depends('report_layout_id')
    def kits_get_layout_info(self):
        for layout in self:
            custom_layout_list = [
                self.env.ref('kits_all_in_one_custom_layout.report_layout_diagonal').id,
                self.env.ref('kits_all_in_one_custom_layout.report_layout_curved').id,
                self.env.ref('kits_all_in_one_custom_layout.report_layout_abstract').id,
            ]
            if layout.report_layout_id.id in custom_layout_list:
                layout.is_img_header_layout = True
            else:
                layout.is_img_header_layout = False

    @api.onchange('report_layout_id')
    def kits_remove_uploded_bg_image(self):
        if not self._context.get('kits_on_open_layout'):
            self.header_background_image = False

    def get_custom_font_size(self):
        layout_key = self.external_report_layout_id.key
        report_font_size = 15
        if layout_key in ['web.external_layout_striped', 'web.external_layout_bold', 'web.external_layout_standard']:
            report_font_size = 16
        kits_font_scale = int(self.report_font_scale)
        filtered_font_size = report_font_size
        if kits_font_scale > 0:
            filtered_font_size = report_font_size + kits_font_scale
        elif kits_font_scale < 0:
            filtered_font_size = report_font_size + kits_font_scale
        return filtered_font_size
