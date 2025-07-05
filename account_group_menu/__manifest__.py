# Copyright 2018 Forest and Biomass Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Group Menu',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': "Adds menu entries for Account Group and Tax Group",
    'author': "Forest and Biomass Romania, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/account-financial-tools',
    'depends': [
        'account',
        'stock_account',
    ],
    'data': [
        'data/admin_group_data.xml',
        'security/res_groups.xml',
        'views/menu.xml',
        'views/res_config_settings.xml',
        'views/account_bank_statement.xml',
        'views/account_group.xml',
        'views/account_move_line.xml',
        'views/account_tag.xml',
        'views/account_tax_group.xml',
        'views/product_category.xml',
    ],
    'demo': [
        'demo/account_group.xml',
        'demo/account_tax_group.xml'
    ],
    'installable': True,
}
