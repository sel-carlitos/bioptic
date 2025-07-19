# -*- coding: utf-8 -*-
{
    'name': "POS Invoice Print Without Download",
    'summary': """The module allows you to print invoice without download in POS.""",
    'license': 'LGPL-3',
    'version': '18.0.1.0.0',
    'depends': ['l10n_sv_dte_pos'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'models/static/src/overrides/components/payment_screen/payment_screen.js',
        ],
    },
}
