import base64
import os
import shutil
import subprocess

from odoo import _, http, tools
from odoo.exceptions import UserError


def kits_pre_init_hook(env):
    kits_report_module_list = ['kits_custom_report_font', 'kits_custom_report_layout', 'kits_report_font_setting']
    modules = (
        env['ir.module.module'].sudo().search([('state', '=', 'installed'), ('name', 'in', kits_report_module_list)])
    )
    if modules:
        number = 1
        error_msg = 'Before installing this module, please ensure that the following modules are uninstalled:'
        for module in modules:
            error_msg += '\n' + str(number) + '. ' + module.shortdesc
            number += 1
        raise UserError(_(error_msg))
    make_css_and_attachment(env)


def kits_post_init_hook(env):
    update_wizard_rec = env['base.module.update'].sudo().create({})
    update_wizard_rec.sudo().update_module()


def kits_uninstall_hook(env):
    font_recs = env['custom.font.style'].sudo().search([])
    if font_recs:
        try:
            font_recs.unlink()
        except Exception as err:
            raise UserError(_('Before uninstalling the module, please select the default Odoo font.')) from err
    attachment = env['ir.attachment'].sudo().search([('name', '=', 'kits_custom_fonts.scss')])
    if attachment:
        attachment.sudo().with_context(kits_is_delete=True).unlink()
    asset = env['ir.asset'].sudo().search([('name', '=', 'kits_custom_fonts')])
    if asset:
        asset.sudo().with_context(kits_is_delete=True).unlink()
    config_param = (
        env['ir.config_parameter'].sudo().search([('key', '=', 'kits_custom_report_font.kits_font_folder_path')])
    )
    if config_param:
        config_param.sudo().with_context(kits_is_delete=True).unlink()
    base_module = (
        env['ir.module.module']
        .sudo()
        .search([('state', '=', 'installed'), ('name', '=', 'kits_base_all_in_one_custom_layout')])
    )
    if base_module:
        base_module.sudo().button_uninstall()

    addons_path = os.path.join(tools.config['data_dir'], 'addons')
    list_folders = os.listdir(addons_path)
    if len(list_folders):
        inner_folder_path = os.path.join(addons_path, list_folders[0])
        db_name = http.request.db
        db_folder = os.path.join(inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name)
        if os.path.exists(db_folder):
            shutil.rmtree(db_folder)


def make_css_and_attachment(env):
    db_name = http.request.db
    addons_path = os.path.join(tools.config['data_dir'], 'addons')
    if os.path.exists(addons_path):
        list_folders = os.listdir(addons_path)
        if len(list_folders):
            inner_folder_path = os.path.join(addons_path, list_folders[0])
            subprocess.run(['chmod', '-R', '777', inner_folder_path], check=True)
            module_path = os.path.dirname(os.path.abspath(__file__))
            source_folder = os.path.join(module_path, 'base_module/kits_base_all_in_one_custom_layout')
            if os.path.exists(source_folder):
                try:
                    if not os.path.exists(inner_folder_path + '/kits_base_all_in_one_custom_layout'):
                        subprocess.run(
                            ['cp', '-r', source_folder, inner_folder_path + '/'],
                            check=True,
                            capture_output=True,
                            text=True,
                        )

                    module_static_path = os.path.join(
                        inner_folder_path, 'kits_base_all_in_one_custom_layout/static/src/' + db_name + '/fonts'
                    )
                    os.makedirs(module_static_path, exist_ok=True)
                    env['ir.config_parameter'].sudo().set_param(
                        'kits_custom_report_font.kits_font_folder_path', module_static_path
                    )

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
                    """
                    attachment = env['ir.attachment'].sudo().search([('name', '=', 'kits_custom_fonts.scss')])

                    if attachment:
                        attachment.write({'datas': base64.b64encode(scss_content.encode('utf-8'))})
                    else:
                        attachment = (
                            env['ir.attachment']
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

                    env['ir.asset'].create(
                        {
                            'name': 'kits_custom_fonts',
                            'bundle': 'web.report_assets_common',
                            'path': attachment.url,
                        }
                    )

                except subprocess.CalledProcessError as e:
                    print(f'Error copying files: {e}')
