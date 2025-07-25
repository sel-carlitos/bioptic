import base64
import io
import os
import shutil
import zipfile

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class custom_font_style(models.Model):
    _name = 'custom.font.style'
    _description = 'Custom font'

    url_date = fields.Date(string='Date')
    file = fields.Binary('Upload File', attachment=False)
    file_name = fields.Char('File Name')
    css_line = fields.Char('CSS Line')

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list.get('file_name'):
            rec_exists = self.env['custom.font.style'].search([('file_name', '=', vals_list.get('file_name'))])
            if rec_exists:
                raise UserError(_('This font already exists.'))

        res = super().create(vals_list)
        selection_value = None
        if res.file_name:
            selection_value = res.file_name.split('.')[0].replace('_', ' ')

        binary_content = res.file
        font_path = self.env['ir.config_parameter'].sudo().get_param('kits_custom_report_font.kits_font_folder_path')
        if res.file_name:
            font_new_path = os.path.join(font_path, res.file_name.split('.')[0])
            zip_data = base64.b64decode(binary_content)
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
            font_file_names = []
            for file_name in zip_file.namelist():
                full_path = os.path.join(font_new_path, file_name)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                if (
                    file_name.endswith('.ttf')
                    or file_name.endswith('.otf')
                    or file_name.endswith('.woff')
                    or file_name.endswith('.woff2')
                ):
                    font_file_names.append(file_name)
                    with open(full_path, 'wb') as output_file:
                        output_file.write(zip_file.read(file_name))

            if len(font_file_names) == 0:
                if os.path.exists(font_new_path):
                    shutil.rmtree(font_new_path)
                raise UserError(
                    _(
                        'The uploaded ZIP file does not contain any valid font files. Please upload a ZIP that includes at least one supported font format such as .ttf, .otf, .woff, or .woff2.'
                    )
                )

            attachment = self.env['ir.attachment'].search([('name', '=', 'kits_custom_fonts.scss')], limit=1)

            if attachment:
                current_content = base64.b64decode(attachment.datas).decode('utf-8', errors='ignore')
                font_type = font_file_names[0].split('.')[0]
                new_content = (
                    f"@include custom-font-pair('{selection_value}', '{res.file_name.split('.')[0]}/{font_type}');\n"
                )
                updated_content = f'{current_content}\n{new_content}'
                res.css_line = new_content
                attachment.write({'datas': base64.b64encode(updated_content.encode('utf-8')), 'mimetype': 'text/scss'})
            self.env['ir.qweb'].clear_caches()
            return res
        else:
            raise UserError(_('Please upload a ZIP file before proceeding.'))

    def unlink(self):
        for record in self:
            if record.file_name:
                selection_value = record.file_name.split('.')[0].replace('_', ' ')

                company_using_font = self.env['res.company'].search([('font', '=', selection_value)])
                if not company_using_font:
                    font_path = (
                        self.env['ir.config_parameter']
                        .sudo()
                        .get_param('kits_custom_report_font.kits_font_folder_path')
                    )
                    # Remove the directory
                    font_new_path = os.path.join(font_path, record.file_name.split('.')[0])
                    if os.path.exists(font_new_path):
                        shutil.rmtree(font_new_path)

                    attachment = (
                        self.env['ir.attachment'].sudo().search([('name', '=', 'kits_custom_fonts.scss')], limit=1)
                    )

                    if attachment:
                        scss_content = base64.b64decode(attachment.datas).decode('utf-8')
                        updated_content = '\n'.join(
                            [line for line in scss_content.splitlines() if record.css_line.strip() not in line.strip()]
                        )
                        attachment.write(
                            {'datas': base64.b64encode(updated_content.encode('utf-8')), 'mimetype': 'text/scss'}
                        )
                else:
                    raise UserError(
                        _(
                            f"The font '{selection_value}' is currently in use by Configure your document layout cannot be deleted."
                        )
                    )
        return super().unlink()
