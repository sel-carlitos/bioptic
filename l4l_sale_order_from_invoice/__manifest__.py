# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': "Create Sale Order from Invoice",
    'category': 'Accounting/Accounting',
    'version': '18.0.1.0',
    'sequence': 1,
    'summary': """Create Sale Order from Invoice, Create Sale Order in Invoice, Create Sale Order, Create SO, Sale Order, Invoice, Account, Sales, Sale.""",
    'description': """In Odoo There is no Option to Reverse Process Like User can Create Sale Order from the Invoice so This Plugin will Help to Create Sale Order from Customer Invoice.""",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['sale', 'account'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': True,
    'images' : ['static/description/banner.gif'],
    'license': 'OPL-1',
    'price': '10.99',
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/UFp23WRFzAI',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
