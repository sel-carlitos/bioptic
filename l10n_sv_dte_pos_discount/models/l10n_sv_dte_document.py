# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DTEDocument(models.Model):
	_inherit = "l10n_sv.dte.document"

	def _iterable_products_xml(self, lines):
		# EXTENDS 'l10n_sv_dte'
		res = super()._iterable_products_xml(lines)
		config_id = self.order_id.config_id
		# if self.order_id and self.order_id.config_id.module_pos_discount and self.order_id.config_id.discount_product_id:
		if self.order_id and config_id.module_pos_discount and config_id.discount_product_id:
			# pos_discount_product_id = self.order_id.config_id.discount_product_id
			pos_discount_product_id = config_id.discount_product_id
			return res.filtered(lambda l: l.product_id.id != pos_discount_product_id.id)

		return res

	def set_summary_additional_vals(self, summary, *args):
		# EXTENDS 'l10n_sv_dte'

		res = super().set_summary_additional_vals(summary, *args)
		total_discount = 0.00
		config_id = self.order_id.config_id
		# if self.order_id and self.order_id.config_id.module_pos_discount and self.order_id.config_id.discount_product_id:
		if self.order_id and config_id.module_pos_discount and config_id.discount_product_id:
			# pos_discount_product_id = self.order_id.config_id.discount_product_id
			pos_discount_product_id = config_id.discount_product_id
			for line in self.order_id.lines:
				if line.product_id.id == pos_discount_product_id.id:
					total_discount += line.price_subtotal

		if total_discount:
			# Add the total discount to the existing total discounts
			summary.set_totalDescu(summary.get_totalDescu() + abs(total_discount))
			summary.set_descuExenta(summary.get_descuExenta() + abs(total_discount))

		return res
