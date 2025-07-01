# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import models, fields, _


class LeapProductCatalogue(models.Model):
    _name = 'leap.product.catalogue'
    _description = 'Product Catalogue'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char('Catalogue Name', default="Product Catalogue")
    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self: self.env.company, ondelete="restrict")
    category_ids = fields.Many2many('product.category', string="Categories")
    activity_ids = fields.One2many('mail.activity', 'res_id', 'Activities', auto_join=True, groups="base.group_user", )  # For Chatter

    def get_attachments(self):
        return self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self.id)])

    def _find_catalogue_mail_template(self):
        self.ensure_one()
        return self.env.ref('l4l_product_catalogue.l4l_mail_template_product_catalogue', raise_if_not_found=False)

    def compose_product_catalogue_mail(self, mail_template):
        self.ensure_one()
        attachments = self.get_attachments()
        ctx = {
            'default_model': self._name,
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
            'model_description': _('Product Catalogue'),
            'default_attachment_ids': [(6, 0, attachments.ids)],
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_product_catalogue_send(self):
        mail_template = self._find_catalogue_mail_template()
        return self.compose_product_catalogue_mail(mail_template)

    def action_view_product_catalogue(self):
        document_list = self.get_attachments()
        action = self.env.ref('base.action_attachment').read()[0]
        form_view = [(self.env.ref('l4l_product_catalogue.l4l_view_attachment_extend_product_catalogue_form').sudo().id, 'form')]
        action['domain'] = [('res_model', '=', self._name), ('res_id', '=', self.id)]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.id}

        if len(document_list) > 0:
            if 'views' in action:
                action['views'] = [(state, view) for state, view in action['views'] if view != 'form'] + form_view
        elif len(document_list) == 0:
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

