import base64
import io
import os
import shutil
import zipfile

from odoo import SUPERUSER_ID, http, registry, tools
from odoo.api import Environment

from odoo.addons.web.controllers.database import Database


class KitsDatabase(Database):
    @http.route('/web/database/duplicate', type='http', auth='none', methods=['POST'], csrf=False)
    def duplicate(self, master_pwd, name, new_name, neutralize_database=False):
        try:
            response = super().duplicate(master_pwd, name, new_name, neutralize_database=neutralize_database)
            self.kits_create_db_folder_and_change_attachment(new_name, name)
            return response
        except Exception:
            return response

    @http.route('/web/database/drop', type='http', auth='none', methods=['POST'], csrf=False)
    def drop(self, master_pwd, name):
        try:
            self.kits_delete_db_name_folder(name)
            response = super().drop(master_pwd, name)
            return response
        except Exception:
            return response

    def kits_create_db_folder_and_change_attachment(self, new_name, old_name):
        try:
            db_name = new_name
            with registry(db_name).cursor() as cr:
                env = Environment(cr, SUPERUSER_ID, {})
                module = (
                    env['ir.module.module']
                    .sudo()
                    .search([('state', '=', 'installed'), ('name', '=', 'kits_all_in_one_custom_layout')])
                )
                if module:
                    addons_path = os.path.join(tools.config['data_dir'], 'addons')
                    list_folders = os.listdir(addons_path)
                    if len(list_folders):
                        inner_folder_path = os.path.join(addons_path, list_folders[0])
                        new_path = os.path.join(
                            inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name + '/fonts'
                        )

                    os.makedirs(new_path, exist_ok=True)
                    env['ir.config_parameter'].sudo().set_param(
                        'kits_custom_report_font.kits_font_folder_path', new_path
                    )
                    existing_fonts = env['custom.font.style'].sudo().search([])
                    for font in existing_fonts:
                        font = font.sudo()
                        binary_content = font.file
                        font_path = new_path
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

                    attachment = env['ir.attachment'].sudo().search([('name', '=', 'kits_custom_fonts.scss')], limit=1)
                    if attachment:
                        scss_content = base64.b64decode(attachment.datas).decode('utf-8', errors='ignore')
                        updated_content = scss_content.replace(
                            f'/kits_base_all_in_one_custom_layout/static/src/{old_name}/fonts/#{{$type}}.ttf',
                            f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.ttf',
                        )
                        updated_content = updated_content.replace(
                            f'/kits_base_all_in_one_custom_layout/static/src/{old_name}/fonts/#{{$type}}.otf',
                            f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.otf',
                        )
                        updated_content = updated_content.replace(
                            f'/kits_base_all_in_one_custom_layout/static/src/{old_name}/fonts/#{{$type}}.woff',
                            f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.woff',
                        )
                        updated_content = updated_content.replace(
                            f'/kits_base_all_in_one_custom_layout/static/src/{old_name}/fonts/#{{$type}}.woff2',
                            f'/kits_base_all_in_one_custom_layout/static/src/{db_name}/fonts/#{{$type}}.woff2',
                        )
                        attachment.sudo().write(
                            {'datas': base64.b64encode(updated_content.encode('utf-8')), 'mimetype': 'text/scss'}
                        )
        except Exception:
            pass

    def kits_delete_db_name_folder(self, db_name):
        try:
            with registry(db_name).cursor() as cr:
                env = Environment(cr, SUPERUSER_ID, {})
                module = (
                    env['ir.module.module']
                    .sudo()
                    .search([('state', '=', 'installed'), ('name', '=', 'kits_all_in_one_custom_layout')])
                )
                if module:
                    addons_path = os.path.join(tools.config['data_dir'], 'addons')
                    list_folders = os.listdir(addons_path)
                    if len(list_folders):
                        inner_folder_path = os.path.join(addons_path, list_folders[0])
                        db_folder = os.path.join(
                            inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name
                        )
                        if os.path.exists(db_folder):
                            shutil.rmtree(db_folder)
        except Exception:
            pass
