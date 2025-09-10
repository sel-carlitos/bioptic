# -*- coding: utf-8 -*-
{
    'name': "El Salvador - POS",
    'countries': ['sv'],
    'summary': """
        Incorpora funcionalidades de facturación con NCF al POS.
        """,
    'license': 'LGPL-3',
    'category': 'Localization',
    'version': '18.0.1.0.0',
    'depends': ['l10n_sv_dte', 'point_of_sale'],
    'data': [
        'data/data.xml',
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
        'views/l10n_sv_dte_document_views.xml',
        'wizard/l10n_sv_dte_move_cancel_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_sv_dte_pos/static/src/app/**/*',
        ],
    },
}
