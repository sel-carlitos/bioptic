{
    'name': 'El Salvador - Localization Improvements',
    'license': 'OPL-1',
    'summary': """
        Enhancements and adjustments to El Salvador's localization to ensure Odoo's integration aligns with the country's tax regulations and business practices.
    """,
    'author': 'Sistemas en Linea',
    'website': 'https://www.sistemas-en-linea.com',
    'maintainer': 'Sistemas en Linea',
    'category': 'Customizations',
    'version': '18.0.0.0.1',
    'depends': [
        'base',
        'account',
        'l10n_sv_dte',
        'stock',
        'sale_stock',
        'l10n_sv_tag_rules',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/groups_tax.xml',
        'data/account_tags.xml',
        'report/report_invoice.xml',
        'views/account_account_tag_views.xml',
        'views/account_move.xml',
        'views/account_tax_group.xml',
        'views/annex_report_f07.xml',
    ],
    'post_init_hook': 'update_group_tax',
    'installable': True,
    'auto_install': False,
    'application': False,
}
