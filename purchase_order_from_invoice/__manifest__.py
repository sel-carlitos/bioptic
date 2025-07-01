# -*- coding: utf-8 -*-

{
    'name': "Create Purchase Order from Invoice",
    'category': 'Accounting/Accounting',
    'version': '18.0.1.0',
    'sequence': 1,
    'summary': """Create Purchase Order from Invoice, Create Purchase Order in Invoice, Create Purchase Order, Create PO, Purchase Order, Invoice, Account, Purchases, Purchase.""",
    'description': """In Odoo There is no Option to Reverse Process Like User can Create Purchase Order from the Invoice so This Plugin will Help to Create Purchase Order from Customer Invoice.""",
    'author': 'Carlos Melgar',
    'depends': ['purchase', 'account'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': True,
    'images' : ['static/description/banner.gif'],
    'license': 'OPL-1',
}
