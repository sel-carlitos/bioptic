from odoo import fields, models


class res_company(models.Model):
    _inherit = 'res.company'

    def kits_get_selection_value(self):
        selection_values = [
            ('Lato', 'Lato'),
            ('Roboto', 'Roboto'),
            ('Open_Sans', 'Open Sans'),
            ('Montserrat', 'Montserrat'),
            ('Oswald', 'Oswald'),
            ('Raleway', 'Raleway'),
            ('Tajawal', 'Tajawal'),
        ]
        custom_font_recs = self.env['custom.font.style'].search([])
        if custom_font_recs:
            for rec in custom_font_recs:
                selection_value = rec.file_name.split('.')[0].replace('_', ' ')
                selection_values.append((selection_value, selection_value))
        return selection_values

    font = fields.Selection(selection=kits_get_selection_value, default='Lato')
    header_background_image = fields.Binary('Header Background Image')
    header_image_file_name = fields.Char(string='File Name')
    report_font_scale = fields.Selection(
        [
            ('-5', '-5'),
            ('-4', '-4'),
            ('-3', '-3'),
            ('-2', '-2'),
            ('-1', '-1'),
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Font Size Scale',
        default='0',
    )

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
