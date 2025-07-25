import base64
import io
import os
import subprocess
import zipfile

from odoo import http, models, tools


class ir_module_module(models.Model):
    _inherit = 'ir.module.module'

    def button_immediate_upgrade(self):
        old_path = self.env['ir.config_parameter'].sudo().get_param('kits_custom_report_font.kits_font_folder_path')
        addons_path = os.path.join(tools.config['data_dir'], 'addons')
        list_folders = os.listdir(addons_path)
        db_name = http.request.db
        if len(list_folders):
            inner_folder_path = os.path.join(addons_path, list_folders[0])
            new_path = os.path.join(
                inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name + '/fonts'
            )

        if old_path != new_path:
            if not os.path.exists(inner_folder_path + '/kits_base_all_in_one_custom_layout'):
                subprocess.run(['chmod', '-R', '777', inner_folder_path], check=True)
                module_path = os.path.dirname(os.path.abspath(__file__))
                cleaned_string = module_path.replace('/models', '', 1)
                source_folder = os.path.join(cleaned_string, 'base_module/kits_base_all_in_one_custom_layout')
                if os.path.exists(source_folder):
                    subprocess.run(
                        ['cp', '-r', source_folder, inner_folder_path + '/'], check=True, capture_output=True, text=True
                    )
                    module_static_path = os.path.join(
                        inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name + '/fonts'
                    )
                    os.makedirs(module_static_path, exist_ok=True)
                    self.env['ir.config_parameter'].sudo().set_param(
                        'kits_custom_report_font.kits_font_folder_path', module_static_path
                    )
                    self.kits_create_font_and_record(module_static_path, db_name)
                    update_wizard_rec = self.env['base.module.update'].sudo().create({})
                    update_wizard_rec.sudo().update_module()

            elif not os.path.exists(inner_folder_path + '/kits_base_all_in_one_custom_layout/static/src/' + db_name):
                module_static_path = os.path.join(
                    inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name + '/fonts'
                )
                os.makedirs(module_static_path, exist_ok=True)
                self.env['ir.config_parameter'].sudo().set_param(
                    'kits_custom_report_font.kits_font_folder_path', module_static_path
                )
                self.kits_create_font_and_record(module_static_path, db_name)

            else:
                self.env['ir.config_parameter'].sudo().set_param(
                    'kits_custom_report_font.kits_font_folder_path', new_path
                )

        res = super().button_immediate_upgrade()
        return res

    def kits_create_font_and_record(self, module_static_path, db_name):
        os.makedirs(module_static_path, exist_ok=True)
        self.env['ir.config_parameter'].sudo().set_param(
            'kits_custom_report_font.kits_font_folder_path', module_static_path
        )
        existing_fonts = self.env['custom.font.style'].sudo().search([])
        attachment_values = ''
        for font in existing_fonts:
            binary_content = font.file
            font_path = module_static_path

            if font.file_name and binary_content:
                font_new_path = os.path.join(font_path, font.file_name.split('.')[0])
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

                selection_value = font.file_name.split('.')[0].replace('_', ' ')
                font_type = font_file_names[0].split('.')[0]
                new_content = (
                    f"@include custom-font-pair('{selection_value}', '{font.file_name.split('.')[0]}/{font_type}');\n"
                )
                attachment_values += f'\n{new_content}'
                font.css_line = new_content

        ttfpath = f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.ttf'
        otfpath = f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.otf'
        woffpath = f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.woff'
        woff2path = f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.woff2'
        scss_content = f"""
            @mixin custom-font($family, $type, $weight, $style) {{
                @font-face {{
                    font-family: $family;
                    src: url("{woffpath}") format('woff'),
                        url("{woff2path}") format('woff2'),
                        url("{ttfpath}") format('truetype'),
                        url("{otfpath}") format('opentype');
                    font-weight: $weight;
                    font-style: $style;
                }}
            }}

            @mixin custom-font-pair($family, $type) {{
                @include custom-font($family, $type, 400, normal);
            }}
            {attachment_values}
        """
        attachment = self.env['ir.attachment'].sudo().search([('name', '=', 'kits_custom_fonts.scss')])

        if attachment:
            attachment.sudo().write({'datas': base64.b64encode(scss_content.encode('utf-8')), 'mimetype': 'text/scss'})
        else:
            attachment = (
                self.env['ir.attachment']
                .sudo()
                .create(
                    {
                        'name': 'kits_custom_fonts.scss',
                        'datas': base64.b64encode(scss_content.encode('utf-8')),
                        'mimetype': 'text/scss',
                        'url': '/kits/web/content/kits_custom_fonts.scss',
                    }
                )
            )
