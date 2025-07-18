# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request
import base64


class GenerateLeapProductCatalogue(models.TransientModel):
    _name = 'generate.leap.product.catalogue'
    _description = 'Wizard For Generate Product Catalogue'
    _rec_name = 'name'

    name = fields.Char('Catalogue Name', default="Product Catalogue")
    catalogue_type = fields.Selection([('product', 'Product'), ('category', 'Category')], string='Product Filter By',
                                    default='product')
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company, ondelete="restrict")
    currency_id = fields.Many2one(comodel_name='res.currency', default=lambda self: self.env.company.currency_id.id,
                                  ondelete="restrict")
    product_ids = fields.Many2many('product.product', string="Products", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    category_ids = fields.Many2many('product.category', string="Categories")
    image_size = fields.Selection([('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], string='Image Size',
                                  default='small')
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', string="Pricelist", check_company=True,
                                   ondelete="restrict")
    show_product_link = fields.Boolean(string='Product Link', default=True)
    show_image = fields.Boolean(string='Image', default=True)
    show_internal_reference = fields.Boolean(string='Internal Reference', default=True)
    show_category = fields.Boolean(string='Print Category', default=True)
    show_uom = fields.Boolean(string='UOM', default=True)
    show_price = fields.Boolean(string='Price', default=True)
    show_description = fields.Boolean(string='Description', default=True)
    catalogue_style = fields.Selection(
        [('style_1', 'Style 1'), ('style_2', 'Style 2'), ('style_3', 'Style 3'), ('style_4', 'Style 4'),
         ('style_5', 'Style 5')],
        string='Catalogue Template', default='style_1')
    box_per_row = fields.Selection([('2', '2 Box'), ('3', '3 Box'), ('4', '4 Box')], string='Print Box Per Row',
                                   default='2')
    send_catalogue = fields.Boolean(string='Send Catalogue')
    partner_ids = fields.Many2many('res.partner', string='Customers', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    description_fields = fields.Many2one('ir.model.fields',
                                         domain="[('model_id', '=', 'product.product'), ('ttype', 'in', ['char', 'text'])]",
                                         string='Description Field', help='Choose the product description field')
    template_id = fields.Many2one("mail.template", string='Load Template',
                                  domain="[('model_id', '=', 'leap.product.catalogue')]")

    # Header and footer fields
    catalogue_header = fields.Binary(string="Header pages",
                                     help="Please upload the PDF with the header pages to be printed before the product catalog")
    catalogue_header_name = fields.Char()
    catalogue_footer = fields.Binary(string="Footer pages",
                                     help="Please upload the PDF with the footer pages to be printed after the product catalog")
    catalogue_footer_name = fields.Char()


    def get_categories(self):
        categories = self.category_ids
        if not categories:
            categories = self.env['product.category'].search([])
        return categories

    def get_all_product(self):
        products = self.env['product.product']
        if self.catalogue_type == 'product':
            if self.product_ids:
                products = self.env['product.product'].browse(self.product_ids.ids)
            else:
                products = self.env['product.product'].search(
                    ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])
        elif self.catalogue_type == 'category':
            categories = self.get_categories()
            products = self.env['product.product'].search(
                ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id),
                 ('categ_id', 'in', categories.ids)])
        if not products:
            raise ValidationError(_("No Products Found!"))
        return products

    @api.constrains('name', 'catalogue_type', 'category_ids', 'product_ids')
    def check_all_product(self):
        for record in self:
            record.get_all_product()

    @api.onchange('catalogue_style', 'show_price')
    def onchange_catalogue_styles(self):
        for record in self:
            if record.catalogue_style in ('style_3', 'style_5'):
                record.show_image = True

    @api.onchange('company_id')
    def onchange_company_id(self):
        for record in self:
            record.product_ids = False
            record.pricelist_id = False
            record.partner_ids = False

    def get_product_image(self, product):
        image_sizes = {
            'small': 'image_128',
            'medium': 'image_256',
            'large': 'image_512'
        }
        if self.catalogue_style != 'style_1':
            image_sizes = {key: 'image_1920' for key in image_sizes}
        return getattr(product, image_sizes.get(self.image_size, 'image_256'), False)

    def get_product_unit_price(self, product):
        self.ensure_one()
        today_date = fields.Date.today()
        quantity = 1.0
        uom = product.uom_id
        if not self.pricelist_id:
            pricelist_rule = self.env['product.pricelist.item']
        else:
            pricelist_rule = self.pricelist_id._get_product_rule(
                product,
                quantity,
                uom=product.uom_id,
                date=today_date,
            )
        pricelist_rule = self.env['product.pricelist.item'].browse(pricelist_rule)
        price = pricelist_rule._compute_price(product, quantity, uom, today_date, currency=self.currency_id)
        return price

    def get_data(self):
        all_products = self.get_all_product()
        product_info_list = []
        for index, product in enumerate(all_products.sudo()):
            product_values = {
                'sr_no': index + 1,
                'name': product.display_name,
            }

            if self.show_image:
                product_image = self.get_product_image(product)
                product_values.update({'image': product_image})

            if self.show_internal_reference:
                product_values.update({'internal_reference': product.default_code, })

            if self.show_category:
                product_values.update({'category': product.categ_id.name if self.catalogue_style in (
                    'style_1', 'style_4', 'style_5') else product.categ_id.display_name})

            if self.show_uom:
                product_values.update({'uom': product.uom_id.name})

            if self.show_product_link and product.website_url:
                try:
                    url = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + product.website_url
                except Exception as url_error:
                    raise ValidationError(_(url_error))
                product_values.update({'product_url': url})

            if self.show_price:
                product_price = self.get_product_unit_price(product)
                product_values.update({'product_price': product_price})

            if self.show_description:
                field_name = str(self.description_fields.name) if self.description_fields and self.description_fields.name else ''
                description_value = getattr(product, field_name, '')
                product_values.update({'description': description_value})

            product_info_list.append(product_values)
        return product_info_list

    def create_catalogue(self):
        try:
            pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('l4l_product_catalogue.l4l_action_report_product_catalogue', self.ids)
            b64_pdf = base64.b64encode(pdf[0])
            catalogue_id = self.env['leap.product.catalogue'].create({
                'name': _(self.name),
                'company_id': self.company_id.id,
                'category_ids': [(6, 0, self.get_categories().ids if self.catalogue_type == 'category' else [])],
            })
            if catalogue_id:
                self.env['ir.attachment'].create({
                    'name': _(self.name),
                    'type': 'binary',
                    'datas': b64_pdf,
                    'res_model': 'leap.product.catalogue',
                    'res_id': catalogue_id.id,
                    'mimetype': 'application/octet-stream'
                })
                return catalogue_id
        except Exception as error_message:
            raise ValidationError(_(error_message))

    def button_print_product_catalogue(self):
        self.get_data()
        self.create_catalogue()
        return self.env.ref('l4l_product_catalogue.l4l_action_report_product_catalogue').report_action(self)

    def button_send_product_catalogue_to_customers(self):
        self.get_data()
        catalogue_id = self.create_catalogue()
        if catalogue_id:
            template = self.template_id
            partner_ids = ', '.join(map(str, self.partner_ids.ids))
            attachments = catalogue_id.get_attachments()
            template.write({'partner_to': partner_ids})
            template.send_mail(catalogue_id.id, force_send=True, email_values={
                        'attachment_ids': [(6, 0, [attachments.id])]})

# vim:expandtab:smartcd indent:tabstop=4:softtabstop=4:shiftwidth=4:
