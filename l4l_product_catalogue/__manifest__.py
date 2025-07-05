# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': "Generate Product Catalogue",
    'category': 'Extra Tools',
    'version': '18.0.1.0',
    'summary': """Product Catalogue, Product, Multiple Products, Odoo Product Catalogue Generator, Products, Customizable Catalogue, Catalogue, Catalogue Styling Options, Multi-Currency Catalogue Printing, Product Catalogue Send By Email, Catalogue Customization, Dynamic Product Catalogue Creation, Catalogue Management, Product Catalogue Design Tool, Website, E-Commerce, Catalogue of Product, Mail, Send By Mail, Product View, Catalogue Templates, Generate Product Catalogue, Send Product Catalogue to Customer, Product Catalogue Style, Various Styles, Catalogue Layout Customization, Catalogue Printing Options, Product Presentation, Product Showcase, L4L, Leap, 4, Logic, Leap4Logic""",
    'description': """The Customizable Product Catalogue Maker in Odoo Helps User to Easily Create and Customize Product Catalogues to Fit Their Needs. It Has a Simple Interface and Lots of Options to Customize. This Makes It Easy to Create Nice-Looking Catalogues to Share with Customers.""",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['mail', 'account', 'product', 'sale_management', 'website_sale', 'website'],
    'data': [
        'security/res_groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_templates.xml',
        'report/catalogue_style_1.xml',
        'report/catalogue_style_2.xml',
        'report/catalogue_style_3.xml',
        'report/catalogue_style_4.xml',
        'report/catalogue_style_5.xml',
        'report/report_product_catalogue.xml',
        'wizard/generate_product_catalogue_wizard_view.xml',
        'views/main_menu_view.xml',
        'views/leap_product_catalogue_view.xml',
        'views/attachments_extend_views.xml',
    ],
    'application': True,
    'installation': True,
    'license': 'OPL-1',
    'price': '25.99',
    'currency': 'USD',
    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/uxNOl4E9c78',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
