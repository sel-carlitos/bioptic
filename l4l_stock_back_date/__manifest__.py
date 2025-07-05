# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': 'Stock Back Date',
    'category': 'Stock',
    'version': '18.0.1.0',
    'summary': 'BackDate in Stock, Set BackDate in Stock, Stock, Sale, Sale Order, Purchase, Purchase Order, Inventory, Transfer, Invoice',
    'description': "The standard Vanilla Odoo does not support backdating transactions. However, with the introduction of this module, users gain the flexibility to modify the scheduled date to a past date. Consequently, all associated documents, such as stock movements and journal entries linked to deliveries or shipments, will reflect the selected date. This enhancement allows for greater adaptability in managing transactional timelines within the Odoo system.                             The Standard Vanilla Odoo does not Support Backdating Transactions. However, with the Introduction of This Module, Users Gain the Flexibility to Modify the Scheduled Date to a Past Date. Consequently, All Associated Documents, Such as Stock Movements and Journal Entries Linked to Deliveries or Shipments, Will Reflect the Selected Date. This Enhancement Allows for Greater Adaptability in Managing Transactional Timelines Within the Odoo System.",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['stock', 'stock_account'],
    'data': [
        'views/res_config_views.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',    
    "price": '11.99',
    "currency": "USD",
    "live_test_url": 'https://youtu.be/yWnPR8NSGI8',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
