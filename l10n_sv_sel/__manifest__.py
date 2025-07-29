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
    ],
    'data': [
        'views/account_move.xml',
        'views/account_tax_group.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
